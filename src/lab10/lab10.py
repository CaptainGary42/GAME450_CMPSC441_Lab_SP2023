""" Lab 10: Save people
You can save people from heart disease by training a model to predict whether a person has heart disease or not.
The dataset is available at src/lab8/heart.csv
Train a model to predict whether a person has heart disease or not and test its performance.
You can usually improve the model by normalizing the input data. Try that and see if it improves the performance. 
"""
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np

data = pd.read_csv("src/lab10/heart.csv")

# Transform the categorical variables into dummy variables.
print(data.head())
string_col = data.select_dtypes(include="object").columns
df = pd.get_dummies(data, columns=string_col, drop_first=False)     #Convert character values to numerical ones
print(data.head())                                                  #

y = df.HeartDisease.values                                          #Heart disease column
x = df.drop(["HeartDisease"], axis=1)
x_train, x_test, y_train, y_test = train_test_split(                #Split data set into training and test data sets
    x, y, test_size=0.2, random_state=25                            #183 sets are in the x_test. 183 in the y_test
)

""" Train a sklearn model here. """                                 #Create an instance of a sklearn model

neighbors = 12
sklearn_model = KNeighborsClassifier(n_neighbors= neighbors)
sklearn_model.fit(x_train,y_train)



print("Accuracy of model: {}\n".format(sklearn_model.score(x_test, y_test)))

""" Improve the model by normalizing the input data. """

#Normalize x_train
x_train = (x_train - x_train.min()) / (x_train.max() - x_train.min())  

#Normalize x_test
x_test = (x_test - x_test.min()) / (x_test.max() - x_test.min())  

#Fit the training sets
sklearn_model.fit(x_train,y_train)

print("Accuracy of improved model: {}\n".format(sklearn_model.score(x_test, y_test)))


