import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt 
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense, LSTM


df = pd.read_csv('./S4248SM144NCEN.csv', index_col= 'DATE', parse_dates=True)
df.index.freq = 'MS'

df.info()
df.columns= ['Sales']
df.head()
df.plot(figsize=(16,8))



train = df.iloc[:316]
test= df.iloc[316:]
test= test[0:12]
test.info()

scaler = MinMaxScaler()
scaler.fit(train)

scaled_train = scaler.transform(train)
scaled_test = scaler.transform(test) 

n_input = 12
n_feature = 1

train_generator = TimeseriesGenerator(scaled_train,scaled_train,length=n_input, batch_size=1)

model = Sequential()

model.add(LSTM(256, activation='relu', input_shape= (n_input, n_feature), return_sequences=True))
model.add(LSTM(256, activation='relu', return_sequences=True))
model.add(LSTM(256, activation='relu', return_sequences=True))
model.add(LSTM(256, activation='relu', return_sequences=True))
model.add(LSTM(256, activation='relu', return_sequences=False))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

model.summary()

model.fit_generator(train_generator,epochs= 50)

my_loss= model.history.history['loss']
plt.plot(range(len(my_loss)),my_loss)

first_eval_batch = scaled_train[-12:]

first_eval_batch
first_eval_batch = first_eval_batch.reshape((1,n_input,n_feature))
model.predict(first_eval_batch)

##Forecast Using RNN Model
#holding my predictions
test_predictions = []
# last n_input points from the training set
first_eval_batch = scaled_train[-n_input:]
# reshape this to the format RNN wants (same format as TimeseriesGeneration)
current_batch = first_eval_batch.reshape((1,n_input,n_feature))
#how far into the future will I forecast?
for i in range(len(test)):
    
    # One timestep ahead of historical 12 points
    current_pred = model.predict(current_batch)[0]
    
    #store that prediction
    test_predictions.append(current_pred)######
    
    # UPDATE current batch o include prediction
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]], axis= 1)


#print(test_predictions)
true_predictions = scaler.inverse_transform(test_predictions)
#print(true_predictions)

test['Predictions'] =true_predictions
print(test.head())


test.plot(figsize=(12,8))

