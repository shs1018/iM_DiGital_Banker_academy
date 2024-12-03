import datetime

import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras import Model, Sequential

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanAbsoluteError

from tensorflow.keras.layers import Dense, Conv1D, LSTM, Reshape, RNN, LSTMCell

import warnings
warnings.filterwarnings('ignore')

class DataWindow():
    def __init__(self, 
                 input_width, label_width, shift,
                 train_df = train_df, val_df = val_df, test_df = test_df,
                 label_columns = None):
        
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df

        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in enumerate(label_columns)}
        self.column_indices = {name: i for i, name in enumerate(train_df.columns)}

        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift

        self.total_window_size = input_width + shift

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.label_width

        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

    def split_to_inputs_labels(self, features):
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]

        if self.label_columns is not None:
            labels = tf.stack(
                [labels[:,:,self.column_indices[name]] for name in self.label_columns],
                axis = -1
            )
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])

        return inputs, labels
    
    def plot(self, model= None, plot_col = 'traffic_volume', max_subplots = 3):
        inputs, labels = self.sample_batch

        plt.figure(figsize = (12,8))
        plot_col_index = self.column_indices[plot_col]
        max_n = min(max_subplots, len(inputs))

        for n in range(max_n):
            plt.subplot(3, 1, n+1)
            plt.ylabel(f'{plot_col} [scaled]')
            plt.plot(self.input_indices, inputs[n, :, plot_col_index],
                     label='Inputs', marker='.', zorder=-10)

            if self.label_columns:
              label_col_index = self.label_columns_indices.get(plot_col, None)
            else:
              label_col_index = plot_col_index

            if label_col_index is None:
              continue

            plt.scatter(self.label_indices, labels[n, :, label_col_index],
                        edgecolors='k', marker='s', label='Labels', c='green', s=64)
            if model is not None:
              predictions = model(inputs)
              plt.scatter(self.label_indices, predictions[n, :, label_col_index],
                          marker='X', edgecolors='k', label='Predictions',
                          c='red', s=64)

            if n == 0:
              plt.legend()

        plt.xlabel('Time(h)')

    def make_dataset(self, data):
       data = np.array(data, dtype = np.float32)
       ds = tf.keras.preprocessing.timeseries_dataset_from_array(
          data = data,
          targets = None,
          sequence_length = self.total_window_size,
          sequence_stride = 1,
          shuffle = True,
          batch_size = 32
       )

       ds = ds.map(self.split_to_inputs_labels)
       return ds
    
    @property
    def train(self):
       return self.make_dataset(self.train_df)
    
    @property
    def val(self):
       return self.make_dataset(self.test_df)
    
    @property
    def test(self):
       return self.make_dataset(self.test_df)
    
    @property
    def sample_batch(self):
        result = getattr(self, '_sample_batch', None)
        if result is None:
           result = next(iter(self.train))
           self._sample_batch = result
        return result
    
def compile_and_fit(model, window, patience = 3, max_epochs = 50):
    
    early_stopping = EarlyStopping(monitor = 'val_loss',
                                   patience = patience,
                                   mode = 'min')
    
    model.compile(loss = MeanSquaredError(),
                  optimizer = Adam(),
                  metrics = [MeanAbsoluteError()])
    
    history = model.fit(window.train,
                        epochs = max_epochs,
                        validation_data = window.val,
                        callbacks = [early_stopping])
    
    return history

single_step_window = DataWindow(input_width = 1, label_width = 1, shift = 1, label_columns = ['traffic_volume'])
wide_window = DataWindow(input_width = 24, label_width = 24, shift = 1, label_columns = ['traffic_volume'])

mae_val = [0.083, 0.068, 0.033]
mae_test = [0.081, 0.068, 0.029]

lstm_model = Sequential([
    LSTM(32, return_sequences = True),
    Dense(units = 1)
])

history = compile_and_fit(lstm_model, wide_window)

val_performance = {}
performance = {}

val_performance['LSTM'] = lstm_model.evaluate(wide_window.val)
performance['LSTM'] = lstm_model.evaluate(wide_window.test, verbose = 0)


multi_window = DataWindow(input_width = 24, label_width = 24, shift = 24, label_columns=['traffic_volume'])

ms_mae_val = [0.352, 0.347, 0.088, 0.078]
ms_mae_test = [0.347, 0.341, 0.076, 0.064]

ms_lstm_model = Sequential([
    LSTM(32, return_sequences=True),
    Dense(1, kernel_initializer=tf.initializers.zeros)
])

history = compile_and_fit(ms_lstm_model, multi_window)

ms_val_performance = {}
ms_performance = {}

ms_val_performance['LSTM'] = ms_lstm_model.evaluate(multi_window.val)
ms_val_performance["LSTM"] = ms_lstm_model.evaluate(multi_window.test, verbose = 0)

mo_single_step_window = DataWindow(input_width= 1, label_width = 1, shift = 1, label_columns=['temp','traffic_volume'])
mo_wide_window = DataWindow(input_width=24, label_width=24, shift = 1, label_columns = ['temp', 'traffic_volume'])

mo_mae_val = [0.048, 0.039, 0.023]
mo_mae_test = [0.047, 0.036, 0.020]

mo_lstm_model = Sequential([
    LSTM(32, return_sequences=True),
    Dense(units = 2)
])

history = compile_and_fit(mo_lstm_model, mo_wide_window)

mo_val_performance = {}
mo_performance = {}

mo_val_performance['LSTM'] = mo_lstm_model.evaluate(mo_wide_window.val)
mo_performance['LSTM'] = mo_lstm_model.evaluate(mo_wide_window.test, verbose = 0)

