import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

dataset = pd.read_csv('heart.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

print(X)
print(y)

# Encode binary independent variables
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:,1] = le.fit_transform(X[:,1])
X[:,8] = le.fit_transform(X[:,8])

# Encode categories for chestpaintype, restingecg, stslope
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [2,6,10])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

print(X)

# Split into training and testing datasets

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

# Apply scaler

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

ann = tf.keras.models.Sequential()

ann.add(tf.keras.layers.Dense(units=6, activation="relu"))

ann.add(tf.keras.layers.Dense(units=6, activation="relu"))

ann.add(tf.keras.layers.Dense(units=1, activation="sigmoid"))

ann.compile(optimizer='adam' , loss='binary_crossentropy' , metrics=['accuracy'])

ann.fit(X_train,y_train,batch_size=32, epochs=100)

loss, accuracy = ann.evaluate(X_test, y_test)

print(accuracy)
print()
print(loss)

y_pred = ann.predict(X_test)
y_pred = (y_pred > 0.5)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)

1/0