# Fixed dependencies - do not remove or change.
import pytest
import pandas as pd
import numpy as np
import os
import tensorflow as tf

# Import data

def import_local_data(file_path):
    """This function needs to import the data file into collab and return a pandas dataframe
    """
    raw_df = pd.read_csv(file_path)


    return raw_df

this_directory = os.path.abspath(os.path.dirname(__file__))

local_file_path = os.path.join(this_directory,'breast-cancer.csv')
path_to_data = 'breast-cancer.csv'

# Dont change
raw_data = import_local_data(local_file_path)
print(raw_data)

# Split your data so that you can test the effectiveness of your model
x = raw_data.iloc[:, :-1].values
y = raw_data.iloc[:, -1].values

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

def preprocess_training_data(x):
    """
    This function should process the training data and store any features required in the class
    I need to turn 
    """
    # This for loop is replacing the age ranges with an average of the high and low values of the range
    for column_index,column in enumerate(x[:,0]):
        low,high = column.split('-')
        number = (int(low) + int(high))/2
        x[column_index,0] = number

    # The LabelEncoder here is turning the breast and irradiat variables into 0's and 1's
    x[:,6] = le.fit_transform(x[:,6])
    x[:,8] = le.fit_transform(x[:,8])

    # Here I will attempt to fix index 2 and 3, so that they no longer have months but the original values, then take the average as with age (index 0)      
    fixed = True

    if fixed == True:  
        for column_index,column in enumerate(x[:,2]):
            if 'May' in column:
                fixed_column = column.replace('Oct','10')
                x[column_index,2] = fixed_column
            if 'Sep' in column:
                fixed_column = column.replace('Sep','9')
                x[column_index,2] = fixed_column
            if 'Oct' in column:
                fixed_column = column.replace('Oct','10')
                x[column_index,2] = fixed_column
        for column_index,column in enumerate(x[:,3]):
            if 'Nov' in column:
                fixed_column = column.replace('Nov','11')
                x[column_index,3] = fixed_column
            if 'May' in column:
                fixed_column = column.replace('May','5')
                x[column_index,3] = fixed_column
            if 'Aug' in column:
                fixed_column = column.replace('Aug','9')
                x[column_index,3] = fixed_column
            if 'Dec' in column:
                fixed_column = column.replace('Dec','12')
                x[column_index,3] = fixed_column
        for column_index,column in enumerate(x[:,2]):
            low,high = column.split('-')
            number = (int(low) + int(high))/2
            x[column_index,2] = number
        for column_index,column in enumerate(x[:,3]):
            low,high = column.split('-')
            number = (int(low) + int(high))/2
            x[column_index,3] = number

    # Here I am using OneHotEncoder to turn the remaining categories into their own binary variables
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    # For index 4, I should really set yes to 1, no to 0, and ? to -1 rather than using OneHotEncoder
    
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1,4,6,7])], remainder='passthrough')
    training_df = np.array(ct.fit_transform(x))
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    training_df = sc.fit_transform(training_df)
    processed_df = training_df

    return processed_df
x_processed = preprocess_training_data(x)
from sklearn.model_selection import train_test_split
x_train_processed, x_test_processed, y_train, y_test = train_test_split(x_processed, y, test_size = 0.2, random_state = 1)
y_train = le.fit_transform(y_train)
y_test = le.fit_transform(y_test)
# was not sure where to encode the dependent variables, so I did it here

class Module4_Model:
    
    def __init__(self):
        self.model = None
        
    def preprocess_training_data(self, training_df):
        """
        This function should process the training data and store any features required in the class
        I need to turn 
        """
        # This for loop is replacing the age ranges with an average of the high and low values of the range
        for column_index,column in enumerate(training_df[:,0]):
            low,high = column.split('-')
            number = (int(low) + int(high))/2
            training_df[column_index,0] = number

        # The LabelEncoder here is turning the breast and irradiat variables into 0's and 1's
        training_df[:,6] = le.fit_transform(training_df[:,6])
        training_df[:,8] = le.fit_transform(training_df[:,8])

        # Here I will attempt to fix index 2 and 3, so that they no longer have months but the original values, then take the average as with age (index 0)      
        fixed = True

        if fixed == True:  
            for column_index,column in enumerate(training_df[:,2]):
                if 'May' in column:
                    fixed_column = column.replace('Oct','10')
                    training_df[column_index,2] = fixed_column
                if 'Sep' in column:
                    fixed_column = column.replace('Sep','9')
                    training_df[column_index,2] = fixed_column
                if 'Oct' in column:
                    fixed_column = column.replace('Oct','10')
                    training_df[column_index,2] = fixed_column
            for column_index,column in enumerate(training_df[:,3]):
                if 'Nov' in column:
                    fixed_column = column.replace('Nov','11')
                    training_df[column_index,3] = fixed_column
                if 'May' in column:
                    fixed_column = column.replace('May','5')
                    training_df[column_index,3] = fixed_column
                if 'Aug' in column:
                    fixed_column = column.replace('Aug','9')
                    training_df[column_index,3] = fixed_column
                if 'Dec' in column:
                    fixed_column = column.replace('Dec','12')
                    training_df[column_index,3] = fixed_column
            for column_index,column in enumerate(training_df[:,2]):
                low,high = column.split('-')
                number = (int(low) + int(high))/2
                training_df[column_index,2] = number
            for column_index,column in enumerate(training_df[:,3]):
                low,high = column.split('-')
                number = (int(low) + int(high))/2
                training_df[column_index,3] = number

        # Here I am using OneHotEncoder to turn the remaining categories into their own binary variables
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        # For index 4, I should really set yes to 1, no to 0, and ? to -1 rather than using OneHotEncoder
        
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1,4,6,7])], remainder='passthrough')
        training_df = np.array(ct.fit_transform(training_df))
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        training_df = sc.fit_transform(training_df)
        processed_df = training_df

        return processed_df

    def preprocess_test_data(self, test_df):

        """
        This function should process the training data and store any features required in the class
        I need to turn 
        """
        # This for loop is replacing the age ranges with an average of the high and low values of the range
        for column_index,column in enumerate(test_df[:,0]):
            low,high = column.split('-')
            number = (int(low) + int(high))/2
            test_df[column_index,0] = number

        # The LabelEncoder here is turning the breast and irradiat variables into 0's and 1's
        test_df[:,6] = le.fit_transform(test_df[:,6])
        test_df[:,8] = le.fit_transform(test_df[:,8])

        # Here I will attempt to fix index 2 and 3, so that they no longer have months but the original values, then take the average as with age (index 0)      
        fixed = True

        if fixed == True:  
            for column_index,column in enumerate(test_df[:,2]):
                if 'May' in column:
                    fixed_column = column.replace('Oct','10')
                    test_df[column_index,2] = fixed_column
                if 'Sep' in column:
                    fixed_column = column.replace('Sep','9')
                    test_df[column_index,2] = fixed_column
                if 'Oct' in column:
                    fixed_column = column.replace('Oct','10')
                    test_df[column_index,2] = fixed_column
            for column_index,column in enumerate(test_df[:,3]):
                if 'Nov' in column:
                    fixed_column = column.replace('Nov','11')
                    test_df[column_index,3] = fixed_column
                if 'May' in column:
                    fixed_column = column.replace('May','5')
                    test_df[column_index,3] = fixed_column
                if 'Aug' in column:
                    fixed_column = column.replace('Aug','9')
                    test_df[column_index,3] = fixed_column
                if 'Dec' in column:
                    fixed_column = column.replace('Dec','12')
                    test_df[column_index,3] = fixed_column
            for column_index,column in enumerate(test_df[:,2]):
                low,high = column.split('-')
                number = (int(low) + int(high))/2
                test_df[column_index,2] = number
            for column_index,column in enumerate(test_df[:,3]):
                low,high = column.split('-')
                number = (int(low) + int(high))/2
                test_df[column_index,3] = number

        # Here I am using OneHotEncoder to turn the remaining categories into their own binary variables
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        # For index 4, I should really set yes to 1, no to 0, and ? to -1 rather than using OneHotEncoder
        
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1,4,6,7])], remainder='passthrough')
        test_df = np.array(ct.fit_transform(test_df))
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        test_df = sc.fit_transform(test_df)
        processed_df = test_df

        return processed_df

# Dont change   
my_model = Module4_Model()

# Dont change
# x_train_processed = my_model.preprocess_training_data(x_train)


ann = tf.keras.models.Sequential()

ann.add(tf.keras.layers.Dense(units=6, activation="relu"))

ann.add(tf.keras.layers.Dense(units=6, activation="relu"))

ann.add(tf.keras.layers.Dense(units=1, activation="sigmoid"))

ann.compile(optimizer='adam' , loss='binary_crossentropy' , metrics=['accuracy'])

history = ann.fit(x_train_processed, y_train, epochs=15)
model_accuracy = history.history['accuracy'][-1]
model_loss = history.history['loss'][-1]

# x_test_processed = my_model.preprocess_test_data(x_test)

loss, accuracy = ann.evaluate(x_test_processed, y_test)

print(accuracy)
print()
print(loss)
1/0