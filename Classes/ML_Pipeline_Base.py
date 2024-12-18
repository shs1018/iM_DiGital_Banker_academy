from sklearn.compose import ColumnTransformer 
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer # 결측치 처리 관련
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

# StratifiedKFold : 분류 작업 할 때
# KFold : 수치 작업 할 때
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, StratifiedKFold, KFold

from scipy.stats import uniform, randint
from sklearn.metrics import mean_squared_error


class ModelPipeline:
    def __init__(self, model, param_distributions, preprocessor, fold_num):
        self.model = model
        self.param_distributions = param_distributions
        self.preprocessor = preprocessor
        self.random_search = None
        self.best_model = None
        self.fold_num = fold_num
        
    def which_kfold(fold_num):
        Straitified_Kfold = StratifiedKFold(n_splits=fold_num,random_state=42,shuffle=True)
        K_fold = KFold(n_splits=fold_num,random_state=42,shuffle=True)
        return Straitified_Kfold, K_fold

    def create_pipeline(self):
        pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),  # 전처리 라인 적용
            ('regressor', self.model(random_state=42))  # 회귀 모델 적용
        ])
        
        Straitified_Kfold = StratifiedKFold(n_splits=5,random_state=42,shuffle=True)

        # RandomizedSearchCV를 사용한 하이퍼파라미터 튜닝
        self.random_search = RandomizedSearchCV(
            estimator=pipeline,
            param_distributions=self.param_distributions,
            n_iter=50,  # 시도 횟수
            cv=Straitified_Kfold,  # 교차 검증
            scoring='neg_mean_squared_error',  # 평가 지표
            random_state=42,
            n_jobs=-1  # 가용한 모든 코어 사용
        )
        
    def fit(self, X_train, y_train):
        self.random_search.fit(X_train, y_train)
        self.best_model = self.random_search.best_estimator_
        return self.best_model

    def get_score(self, X_tr, X_val, y_tr, y_val):
        tr_pred = self.best_model.predict(X_tr)
        val_pred = self.best_model.predict(X_val)
        tr_score = np.sqrt(mean_squared_error(y_tr, tr_pred))
        val_score = np.sqrt(mean_squared_error(y_val, val_pred))
        return f"train: {tr_score}, validation: {val_score}"