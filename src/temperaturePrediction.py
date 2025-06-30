import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

class TemperaturePrediction:
    def __init__(self, file_path, component_type):
        self.df = pd.read_csv(file_path)
        self.component_type = component_type
        self.resistor = self.df[self.df['器件类型'] == component_type].reset_index(drop=True)
    
    def create_dataset(self, dataset, look_back=10):
        X, y = [], []
        for i in range(len(dataset)-look_back):
            X.append(dataset[i:i+look_back, 0])
            y.append(dataset[i+look_back, 0])
        return np.array(X), np.array(y)

    def train_and_predict(self, feature_name, look_back=10, epochs=20, batch_size=32):
        data = self.resistor[[feature_name]].values
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data)
        
        X, y = self.create_dataset(data_scaled, look_back)
        X = X.reshape((X.shape[0], X.shape[1], 1))

        model = Sequential([
            LSTM(50, input_shape=(look_back, 1)),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
        
        pred = model.predict(X)
        pred_inv = scaler.inverse_transform(pred)
        y_inv = scaler.inverse_transform(y.reshape(-1, 1))
        r2 = r2_score(y_inv, pred_inv)
        
        return y_inv, pred_inv, r2

    def plot_predictions(self, true_values, predicted_values, title):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(10, 5))
        plt.scatter(range(len(true_values)), true_values, label=f'{title} True', color='blue', s=15)
        plt.plot(predicted_values, label=f'{title} Predicted', color='orange')
        plt.legend()
        plt.title(f'{self.component_type}{title}预测')
        plt.show()

    def evaluate(self, temperature_type='中心温度(℃)'):
        y_temp, pred_temp, r2_temp = self.train_and_predict(temperature_type)
        print(f"{temperature_type} R^2分数: {r2_temp:.4f}")
        self.plot_predictions(y_temp, pred_temp, temperature_type)