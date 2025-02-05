import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import ta
import plotly.graph_objects as go
from datetime import datetime, timedelta
from tqdm import tqdm

class StockTradingStrategy:
    def __init__(self, symbol, start_date='2010-01-01', pred_days=30, expected_return=0.1, investment_start_date=None):
        self.symbol = symbol
        self.start_date = start_date
        self.pred_days = pred_days
        self.data = None
        self.model = None
        self.expected_return = expected_return
        self.investment_start_date = investment_start_date
        
    def get_data(self):
        """Download stock data from Yahoo Finance"""
        self.data = yf.download(self.symbol, start=self.start_date)
        self.data.columns = self.data.columns.droplevel(1)  # Remove 'Ticker' level
        self.data = self.data.rename_axis(None, axis=1)  # Remove column axis name
        
    def add_technical_indicators(self):
        """Add technical indicators for traditional analysis"""
        # Moving averages
        self.data['SMA20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA50'] = self.data['Close'].rolling(window=50).mean()
        
        # RSI
        self.data['RSI'] = ta.momentum.RSIIndicator(self.data['Close']).rsi()
        
        # MACD
        macd = ta.trend.MACD(self.data['Close'])
        self.data['MACD'] = macd.macd()
        self.data['MACD_signal'] = macd.macd_signal()
        
        # Bollinger Bands
        bb = ta.volatility.BollingerBands(self.data['Close'])
        self.data['BB_upper'] = bb.bollinger_hband()
        self.data['BB_lower'] = bb.bollinger_lband()
        
    def generate_traditional_signals(self):
        """Generate trading signals based on traditional technical analysis"""
        self.data['Traditional_Signal'] = 0
        
        # Golden/Death Cross
        self.data.loc[self.data['SMA20'] > self.data['SMA50'], 'Traditional_Signal'] = 1
        self.data.loc[self.data['SMA20'] < self.data['SMA50'], 'Traditional_Signal'] = -1
        
        # RSI overbought/oversold
        self.data.loc[self.data['RSI'] > 70, 'Traditional_Signal'] = -1
        self.data.loc[self.data['RSI'] < 30, 'Traditional_Signal'] = 1

    def predict_future_prices(self, days=30):
        """Predict future prices using both traditional and ML methods"""
        last_price = self.data['Close'].iloc[-1]
        future_dates = pd.date_range(start=self.data.index[-1] + timedelta(days=1), periods=days)
        
        # Traditional prediction using SMA trends
        traditional_trend = (self.data['SMA20'].iloc[-1] - self.data['SMA20'].iloc[-20]) / 20
        traditional_preds = [last_price]
        for i in range(days):
            traditional_preds.append(traditional_preds[-1] + traditional_trend)
            
        # ML prediction
        if self.model is not None:
            ml_trend = self.get_current_signal('ml')
            ml_preds = [last_price]
            avg_daily_change = self.data['Returns'].mean()
            for i in range(days):
                if ml_trend == 1:
                    ml_preds.append(ml_preds[-1] * (1 + abs(avg_daily_change)))
                else:
                    ml_preds.append(ml_preds[-1] * (1 - abs(avg_daily_change)))
                    
            return future_dates, traditional_preds[1:], ml_preds[1:]
        return future_dates, traditional_preds[1:], None

    def calculate_expected_returns(self, predictions, initial_price):
        """Calculate expected returns for each prediction period"""
        return [(price - initial_price) / initial_price for price in predictions]
        
    def prepare_ml_features(self):
        """Prepare features for machine learning model"""
        self.data['Returns'] = self.data['Close'].pct_change()
        self.data['Target'] = (self.data['Returns'].shift(-1) > 0).astype(int)
        
        features = ['Returns', 'RSI', 'MACD', 'MACD_signal']
        
        # Drop NaN values after creating all features
        self.data = self.data.dropna()
        
        X = self.data[features]
        y = self.data['Target']
        
        # Remove last row since target will be NaN
        X = X[:-1]
        y = y[:-1]
        
        return X, y
        
    def train_ml_model(self):
        """Train LightGBM model"""
        progress_text = "Training machine learning model..."
        my_bar = st.progress(0, text=progress_text)

        X, y = self.prepare_ml_features()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        self.model = lgb.LGBMClassifier(random_state=42)
        
        # Training with progress bar
        total_iterations = 100  # LightGBM default iterations
        for i in tqdm(range(total_iterations)):
            if i == 0:
                self.model.fit(X_train, y_train)
            my_bar.progress((i + 1) / total_iterations, text=progress_text)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        my_bar.empty()
        return accuracy
        
    def get_current_signal(self, strategy='traditional'):
        """Get current trading signal based on selected strategy"""
        if strategy == 'traditional':
            return self.data['Traditional_Signal'].iloc[-1]
        elif strategy == 'ml':
            latest_features = self.data[['Returns', 'RSI', 'MACD', 'MACD_signal']].iloc[-1:]
            return self.model.predict(latest_features)[0]

    def calculate_investment_return(self, investment_start_date):
        """Calculate investment return from investment start date"""
        investment_start_date = pd.to_datetime(investment_start_date)
        if not self.data.empty and investment_start_date in self.data.index:
            start_price = self.data.loc[investment_start_date]['Close']
            current_price = self.data['Close'].iloc[-1]
            actual_return = (current_price - start_price) / start_price
            return actual_return, start_price
        return None, None

def main():
    st.title('Stock Trading Strategy Analysis')
    
    # Sidebar inputs
    st.sidebar.header('Input Parameters')
    symbol = st.sidebar.text_input('Stock Symbol (e.g., AAPL)', 'AAPL')
    start_date = st.sidebar.date_input('Start Date', datetime.now() - timedelta(days=365))
    strategy = st.sidebar.selectbox('Select Strategy', ['Traditional', 'Machine Learning'])
    pred_days = st.sidebar.slider('Prediction Days', 5, 90, 30)
    expected_return = st.sidebar.slider('Expected Return (%)', 0, 100, 10) / 100
    investment_start = st.sidebar.date_input('Investment Start Date', datetime.now() - timedelta(days=180))
    
    # Action buttons
    col1, col2, col3 = st.sidebar.columns(3)
    analyze_button = col1.button('Analyze')
    refresh_button = col2.button('Refresh Data')
    clear_button = col3.button('Clear')
    
    if clear_button:
        st.experimental_rerun()
        
    if analyze_button or refresh_button:
        # Initialize and prepare data
        trader = StockTradingStrategy(symbol, start_date.strftime('%Y-%m-%d'), pred_days, 
                                    expected_return, investment_start.strftime('%Y-%m-%d'))
        trader.get_data()
        trader.add_technical_indicators()
        trader.generate_traditional_signals()
        
        # Create tabs
        tab1, tab2 = st.tabs(["Price Analysis", "Return Analysis"])
        
        with tab1:
            # Display basic stock info
            st.header(f'Analysis for {symbol}')
            current_price = trader.data['Close'].iloc[-1]
            st.write(f"Current Price: ${current_price:.2f}")
            
            # Strategy specific analysis
            if strategy == 'Traditional':
                signal = trader.get_current_signal('traditional')
                signal_text = "BUY" if signal == 1 else "SELL" if signal == -1 else "HOLD"
                
                # Technical Analysis Report
                st.subheader('Technical Analysis Report')
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("RSI", f"{trader.data['RSI'].iloc[-1]:.2f}")
                    st.metric("SMA20", f"{trader.data['SMA20'].iloc[-1]:.2f}")
                with col2:
                    st.metric("MACD", f"{trader.data['MACD'].iloc[-1]:.2f}")
                    st.metric("SMA50", f"{trader.data['SMA50'].iloc[-1]:.2f}")
                
            else:  # Machine Learning
                accuracy = trader.train_ml_model()
                signal = trader.get_current_signal('ml')
                signal_text = "BUY" if signal == 1 else "SELL"
                
                st.subheader('Machine Learning Model Report')
                st.metric("Model Accuracy", f"{accuracy:.2%}")
            
            # Display signal
            st.subheader('Current Trading Signal')
            st.markdown(f"<h1 style='text-align: center; color: {'green' if signal_text == 'BUY' else 'red'};'>{signal_text}</h1>", unsafe_allow_html=True)
            
            # Get future predictions
            future_dates, trad_preds, ml_preds = trader.predict_future_prices(pred_days)
            
            # Plot interactive chart with predictions
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(x=trader.data.index, y=trader.data['Close'],
                                    mode='lines', name='Close Price'))
            fig.add_trace(go.Scatter(x=trader.data.index, y=trader.data['SMA20'],
                                    mode='lines', name='SMA20'))
            fig.add_trace(go.Scatter(x=trader.data.index, y=trader.data['SMA50'],
                                    mode='lines', name='SMA50'))
            
            # Predictions
            fig.add_trace(go.Scatter(x=future_dates, y=trad_preds,
                                    mode='lines', line=dict(dash='dash'),
                                    name='Traditional Prediction'))
                                    
            if ml_preds is not None:
                fig.add_trace(go.Scatter(x=future_dates, y=ml_preds,
                                        mode='lines', line=dict(dash='dash'),
                                        name='ML Prediction'))
            
            fig.update_layout(title=f'{symbol} Price History and Predictions',
                             xaxis_title='Date',
                             yaxis_title='Price',
                             height=600)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display predicted values
            st.subheader('Predicted Closing Prices')
            st.write("Traditional Strategy Prediction (Next Day):")
            st.write(f"${trad_preds[0]:.2f}")
            if ml_preds is not None:
                st.write("ML Strategy Prediction (Next Day):")
                st.write(f"${ml_preds[0]:.2f}")
        
        with tab2:
            st.header('Return Analysis')
            
            # Calculate actual return from investment start date
            actual_return, start_price = trader.calculate_investment_return(investment_start)
            if actual_return is not None:
                st.metric("Current Return", f"{actual_return:.2%}")
                st.metric("Expected Return", f"{expected_return:.2%}")
                return_diff = actual_return - expected_return
                st.metric("Return Difference", f"{return_diff:.2%}")
                
                # Calculate expected returns for predictions
                trad_returns = trader.calculate_expected_returns(trad_preds, start_price)
                if ml_preds is not None:
                    ml_returns = trader.calculate_expected_returns(ml_preds, start_price)
                
                # Create return prediction chart
                fig_returns = go.Figure()
                
                # Add expected return target line
                fig_returns.add_hline(y=expected_return, line_dash="dash", line_color="red",
                                    annotation_text="Expected Return Target")
                
                # Add traditional strategy returns
                fig_returns.add_trace(go.Scatter(x=future_dates, y=trad_returns,
                                               mode='lines', name='Traditional Strategy Returns'))
                                               
                if ml_preds is not None:
                    fig_returns.add_trace(go.Scatter(x=future_dates, y=ml_returns,
                                                   mode='lines', name='ML Strategy Returns'))
                
                fig_returns.update_layout(title=f'{symbol} Expected Returns from Investment Start',
                                        xaxis_title='Date',
                                        yaxis_title='Return (%)',
                                        height=400)
                
                st.plotly_chart(fig_returns, use_container_width=True)
                
                # Display return predictions for specific periods
                st.subheader('Expected Returns by Period')
                periods = [5, 10, 30]
                for period in periods:
                    if period <= len(trad_returns):
                        st.metric(f"Traditional {period}-Day Return", 
                                f"{trad_returns[period-1]:.2%}")
                        if ml_preds is not None:
                            st.metric(f"ML {period}-Day Return",
                                    f"{ml_returns[period-1]:.2%}")

if __name__ == '__main__':
    main()
