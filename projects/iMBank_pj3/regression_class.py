import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold, KFold
from sklearn.metrics import mean_squared_error, r2_score

class Regression_Model_Pipeline:
    def __init__(self,
                 model = RandomForestRegressor,
                 numeric_features = None,
                 categorial_features = None):
        
        """
        Regression 모델을 위한 파이프라인 클래스
        
        Parameters:
        - model: 사용할 회귀 모델 (기본값: RandomForestRegressor)
        - numeric_features: 수치형 특성 리스트
        - categorical_features: 범주형 특성 리스트
        """

        self.model = model
        self.numeric_features = numeric_features or []
        self.categorial_features = categorial_features or []

        self.preprocessor = self._create_preprocessor()

        self.param_distributions = {
            'regressor__n_estimators': [500, 800, 1000],
            'regressor__max_depth': [None, 30, 40, 50],
            'regressor__min_samples_split': [5, 10, 15],
            'regressor__min_samples_leaf': [1, 2, 4]
        }

        self.pipeline = self._create_pipeline()

    def _create_preprocessor(self):
        """
        데이터 전처리기 생성
        """

        numeric_transformer = Pipeline(steps = [
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorial_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown = 'ignore'))
        ])

        preprocessor = ColumnTransformer(transformers=[
            ('num', numeric_transformer, self.numeric_features),
            ('cat', categorial_transformer, self.categorial_features)
        ])

        return preprocessor
    
    def _create_pipeline(self):
        """
        모델 파이프라인 생성
        """
        pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('regressor', self.model(random_state=42))
        ])

        return pipeline
    
    def fit_and_evaluate(self, X, y, test_size = 0.2):
        """
        모델 학습 및 평가
        """

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        random_search = RandomizedSearchCV(
            estimator=self.pipeline,
            param_distributions= self.param_distributions,
            n_iter= 50,
            cv = KFold(n_splits=5, shuffle = True, random_state=42),
            scoring='neg_mean_squared_error',
            random_state=42,
            n_jobs=-1
        )

        random_search.fit(X_train, y_train)

        best_model = random_search.best_estimator_

        y_pred_train = best_model.predict(X_train)
        y_pred_test = best_model.predict(X_test)

        train_mse = mean_squared_error(y_train, y_pred_train)
        test_mse = mean_squared_error(y_test, y_pred_test)

        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)

        #결과
        print("최고의 하이퍼 파라미터 RandomTreeRegressor 모델은:", random_search.best_params_)
        print(f"Train MSE: {train_mse:.4f}")
        print(f"Test MSE: {test_mse:.4f}")
        print(f"Train R2: {train_r2:.4f}")
        print(f"Test R2: {test_r2:.4f}")

        return best_model