import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
# Importing the dataset
path_to_data = os.path.join(this_directory,'breast-cancer-old.csv')

dataset = pd.read_csv('breast_cancer/breast-cancer-old.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

print(X)
print(y)

for column_index,column in enumerate(X[:,0]):
    low,high = column.split('-')
    number = (int(low) + int(high))/2
    X[column_index,0] = number

for column_index,column in enumerate(X[:,2]):
    low,high = column.split('-')
    low = low.strip('"')
    high = high.strip('"')
    number = (int(low) + int(high))/2
    X[column_index,2] = number


# Encode binary independent variables
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:,4] = le.fit_transform(X[:,4])
X[:,6] = le.fit_transform(X[:,6])
X[:,8] = le.fit_transform(X[:,8])

# Encode categories for chestpaintype, restingecg, stslope
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1,3,7])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

print(X)

y = le.fit_transform(y)

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

model_accuracy_new = []
accuracy_new = []
model_metrics_new_way = []

number_of_runs = 1
for run_index in range(number_of_runs):
    history = ann.fit(X_train, y_train, epochs=15)
    model_accuracy = history.history['accuracy'][-1]
    model_loss = history.history['loss'][-1]
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
    model_metrics_new_way.append([model_accuracy, model_loss, loss, accuracy])

for run in model_metrics_new_way:
    for index,metric in enumerate(run):
        if index == 0:
            model_accuracy_new.append(metric)
        elif index == 3:
            accuracy_new.append(metric)
        else:
            continue

model_accuracy_new_mean = sum(model_accuracy_new)/len(model_accuracy_new)
accuracy_new_mean = sum(accuracy_new)/len(accuracy_new)

print(f'The mean of the model accuracy for the new method is: {model_accuracy_new_mean}')
print(f'The mean of the accuracy for the new method is: {accuracy_new_mean}')

for layer in ann.layers:
    print(layer.output_shape)

print(ann.get_weights())
variable_index = 0
for index,array in enumerate(ann.get_weights()):
    if index == 0:
        for input_node in array:
            sum_of_weights = 0  
            for weight in input_node:
                sum_of_weights = 0  
                sum_of_weights = sum_of_weights + abs(weight)
            print(f'Variable number {variable_index} has an importance of {sum_of_weights}.')
            variable_index = variable_index + 1
    else:
        continue

1/0