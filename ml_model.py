import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import joblib
import os
from typing import Tuple, Optional

class LSTMModel:
    def __init__(self, sequence_length: int = 60, lstm_units: list = [100, 50], dropout_rate: float = 0.3):
        self.sequence_length = sequence_length
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.model: Optional[keras.Model] = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model_path = "lstm_model.h5"
        self.scaler_path = "scaler.pkl"
    
    def create_model(self, input_shape: Tuple[int, int]):
        model = keras.Sequential()
        
        model.add(keras.layers.LSTM(
            units=self.lstm_units[0],
            return_sequences=True if len(self.lstm_units) > 1 else False,
            input_shape=input_shape
        ))
        model.add(keras.layers.Dropout(self.dropout_rate))
        
        if len(self.lstm_units) > 1:
            for units in self.lstm_units[1:]:
                model.add(keras.layers.LSTM(units=units, return_sequences=False))
                model.add(keras.layers.Dropout(self.dropout_rate))
        
        model.add(keras.layers.Dense(units=25))
        model.add(keras.layers.Dense(units=1))
        
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        self.model = model
        return model
    
    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        data = df[['open', 'high', 'low', 'close', 'volume']].values
        scaled_data = self.scaler.fit_transform(data)
        
        X, y = [], []
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i-self.sequence_length:i])
            y.append(scaled_data[i, 3])
        
        return np.array(X), np.array(y)
    
    def train(self, df: pd.DataFrame, epochs: int = 50, batch_size: int = 32):
        if len(df) < self.sequence_length + 100:
            print(f"Insufficient data for training. Need at least {self.sequence_length + 100} rows, got {len(df)}")
            return
        
        X, y = self.prepare_data(df)
        
        if self.model is None:
            self.create_model(input_shape=(X.shape[1], X.shape[2]))
        
        self.model.fit(X, y, batch_size=batch_size, epochs=epochs, validation_split=0.2, verbose=0)
        
        self.model.save(self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print("Model trained and saved successfully")
    
    def load_model(self):
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = keras.models.load_model(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            return True
        return False
    
    def predict(self, df: pd.DataFrame) -> float:
        if self.model is None:
            if not self.load_model():
                return 0.0
        
        if len(df) < self.sequence_length:
            return 0.0
        
        last_sequence = df[['open', 'high', 'low', 'close', 'volume']].tail(self.sequence_length).values
        
        scaled_sequence = self.scaler.transform(last_sequence)
        X = np.array([scaled_sequence])
        
        prediction = self.model.predict(X, verbose=0)[0][0]
        
        current_price = df['close'].iloc[-1]
        dummy_array = np.zeros((1, 5))
        dummy_array[0, 3] = prediction
        predicted_price = self.scaler.inverse_transform(dummy_array)[0, 3]
        
        price_change_percent = ((predicted_price - current_price) / current_price) * 100
        
        return price_change_percent
    
    def create_pretrained_model(self):
        if not os.path.exists(self.model_path):
            print("Creating simple pre-trained model...")
            dummy_data = {
                'open': np.random.uniform(100, 200, 200),
                'high': np.random.uniform(100, 200, 200),
                'low': np.random.uniform(100, 200, 200),
                'close': np.random.uniform(100, 200, 200),
                'volume': np.random.uniform(1000000, 5000000, 200)
            }
            df = pd.DataFrame(dummy_data)
            self.train(df, epochs=3, batch_size=32)
            print("Pre-trained model created and saved")
        else:
            print("Using existing model")

lstm_model = LSTMModel()
