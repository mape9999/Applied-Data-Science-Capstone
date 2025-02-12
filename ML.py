
    # Objective: Create a ML pipeline to predict first stage landing.
    
    # Perform EDA and determine training labels (dataset_part_2.csv)
    # Create a column for the class, standardize the data, split into training/test data 
    # & find best hyperparameter for SVM, Classification Trees and Logistic Regression
    
    
# Import required libraries, modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.metrics import confusion_matrix 


# Define a function to plot the confusion matrix
def plot_confusion_matrix(y_true, y_pred, title='Confusion Matrix'):
    cm = confusion_matrix(y_true, y_pred)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax, fmt='d', cmap='Blues');  # fmt='d' for integer annotations
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title(title)  # Set the title here
    ax.xaxis.set_ticklabels(['Did Not Land', 'Landed']); 
    ax.yaxis.set_ticklabels(['Did Not Land', 'Landed']) 
    plt.show()

# Load the dataframes
data = pd.read_csv('dataset_part_2.csv')
print(data.head())
X = pd.read_csv('dataset_part3.csv')
print(X.head(100))

# Extract the 'Class' column and keep it as a Pandas series
y = data['Class']
print(y)

# Create an instance of StandardScaler
scaler = StandardScaler()

# Split the data into training and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Display the shapes of the resulting datasets
#print("Training data shape:", X_train.shape, y_train.shape)
#print("Test data shape:", X_test.shape, y_test.shape)

print("Number of records in the test sample: {}".format(len(y_test)))

# Split the training data into training and validation sets
X_train_final, X_val, y_train_final, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

# Standardize the features
X_train_final = scaler.fit_transform(X_train_final)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

# Create an instance of StandardScaler
scaler = StandardScaler()

# Split the data into training and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Display the shapes of the resulting datasets
#print("Training data shape:", X_train.shape, y_train.shape)
#print("Test data shape:", X_test.shape, y_test.shape)

# Split the training data into training and validation sets
X_train_final, X_val, y_train_final, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

# Standardize the features (fit the scaler on the training, validation and test data)
X_train_final = scaler.fit_transform(X_train_final)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

# Convert scaled data back to a df to retain feature names
X_train_final = pd.DataFrame(X_train_final, columns=X_train.columns)
X_val = pd.DataFrame(X_val, columns=X_train.columns)
X_test = pd.DataFrame(X_test, columns=X_train.columns)

# Create a logistic regression model
lr = LogisticRegression(max_iter=1000, class_weight = 'balanced')

# Define the parameter grid
parameters = {
    'C': [0.001,0.01,0.1,1,10,100],  # Regularization strength
    'penalty': ['l2'],  # Regularization type
    'solver': ['newton-cg','lbfgs','saga'],  # Optimization algorithm
    'multi_class': ['multinomial']  # Multi-class option
}

# Create the GridSearchCV object with cv=10
logreg_cv = GridSearchCV(lr, parameters, cv=10, verbose=1)

# Fit the GridSearchCV object to the training data
logreg_cv.fit(X_train_final, y_train_final)

# Print the best parameters and accuracy
print("Logistic Regression - Tuned hyperparameters (best parameters): {}".format(logreg_cv.best_params_))
print("Logistic Regression - Best cross-validated accuracy: {:.2f}".format(logreg_cv.best_score_))

# Use the best estimator to calculate accuracy on the validation data (if available)
if 'X_val' in locals() or 'X_val' in globals():  # Check if validation set exists
    val_accuracy = logreg_cv.best_estimator_.score(X_val, y_val)
    print('Logistic Regression - Validation Accuracy: {:.2f}'.format(val_accuracy))

# Calculate accuracy on the test data using the score method
# Use the best estimator to calculate accuracy on the test data
best_model = logreg_cv.best_estimator_
accuracy = best_model.score(X_test, y_test)
print('Accuracy on test data: {:.2f}'.format(accuracy))

# Confusion matrix 
yhat=logreg_cv.predict(X_test)
plot_confusion_matrix(y_test,yhat, title='Logistic Regression Confusion Matrix')

# The performance of the classification model correctly predicted landed when it landed (True positives = 14)
# True negatives = 3
# 1 false positive (Type I error) and 0 false negative (Type II error)

# Create a Support Vector Machine model
svm = SVC()

# Define the parameter grid for SVM
parameters = {
    'kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
    'C': np.logspace(-3, 3, 5),
    'gamma': np.logspace(-3, 3, 5)
}

# Initialize the SVM model
svm = SVC()

# Create the GridSearchCV object with cv=10
svm_cv = GridSearchCV(svm, parameters, cv=10, verbose=1)
# Fit the GridSearchCV object to the training data
svm_cv.fit(X_train_final, y_train_final)

# Print the best parameters and accuracy
print("SVM - Tuned hyperparameters (best parameters): {}".format(svm_cv.best_params_))
print("SVM - Best cross-validated accuracy: {:.2f}".format(svm_cv.best_score_))

# Use the best estimator to calculate accuracy on the validation data
best_model_svm = svm_cv.best_estimator_
val_accuracy = best_model_svm.score(X_val, y_val)
print('SVM - Validation Accuracy: {:.2f}'.format(val_accuracy))

# Calculate accuracy on the test data
test_accuracy_svm = best_model_svm.score(X_test, y_test)
print('SVM - Test Accuracy: {:.2f}'.format(test_accuracy_svm))

print("Best Kernel:", svm_cv.best_params_['kernel'])

# Plot the confusion matrix for the SVM model
yhat=svm_cv.predict(X_test)
plot_confusion_matrix(y_test,yhat, title='SVM Confusion Matrix')


# Create a Decision Tree Classifier object
tree = DecisionTreeClassifier(random_state=42)

# Compute the pruning path
path = tree.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas = path.ccp_alphas

# Define the parameter grid for Decision Tree
parameters = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': [2 * n for n in range(1, 10)] + [None], # max_depth = None means unlimited depth
    'max_features': ['log2', 'sqrt'],
    'min_samples_leaf': [1, 2, 3, 4, 5],
    'min_samples_split': [2, 5, 10],
    'ccp_alpha': ccp_alphas
}

# Create the GridSearchCV object with cv=10
tree_cv = GridSearchCV(tree, parameters, cv=10, verbose=1, n_jobs=1)

# Fit the GridSearchCV object to the training data
tree_cv.fit(X_train, y_train)

# Print the best parameters and accuracy using format()
print("Decision Tree - Tuned hyperparameters (best parameters): {}".format(tree_cv.best_params_))
print("Decision Tree - Best cross-validated accuracy: {:.2f}".format(tree_cv.best_score_))

# Use the best estimator to calculate accuracy on the validation data (if available)
if 'X_val' in locals() or 'X_val' in globals():  # Check if validation set exists
    val_accuracy = tree_cv.best_estimator_.score(X_val, y_val)
    print('Decision Tree - Validation Accuracy: {:.2f}'.format(val_accuracy))
    
# Use the best estimator to calculate accuracy on the test data
best_model_tree = tree_cv.best_estimator_
test_accuracy_tree = best_model_tree.score(X_test, y_test)
print('Decision Tree - Test Accuracy: {:.2f}'.format(test_accuracy_tree))

# Make predictions using the Decision Tree model
yhat_tree = best_model_tree.predict(X_test)

#Test Accuracy: 0.44 is significantly lower than the cross-validated accuracy. Prune to adjust overfitting if possible.

# Plot the confusion matrix for the Decision Tree model
def plot_confusion_matrix(y_true, y_pred, title='Confusion Matrix'):
    cm = confusion_matrix(y_true, y_pred)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax, fmt='d', cmap='Blues');  # fmt='d' for integer annotations
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title(title)  
    ax.xaxis.set_ticklabels(['Did Not Land', 'Landed']); 
    ax.yaxis.set_ticklabels(['Did Not Land', 'Landed']) 
    plt.show()

# Plot the confusion matrix with a title
plot_confusion_matrix(y_test, yhat_tree, title='Decision Tree Confusion Matrix')

# Feature Importance
importances = tree_cv.best_estimator_.feature_importances_
feature_names = X_train.columns  # Ensure X_train is a DataFrame
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
print("Feature Importances:")
print(feature_importance_df)

# Create a k nearest neighbors classifier object and perform hyperparameter tuning using GridSearchCV
KNN = KNeighborsClassifier()

# Define the parameter grid for KNN
parameters = {
    'n_neighbors': [3, 5, 7],
    'weights': ['uniform', 'distance'],
    'algorithm': ['brute', 'auto', 'kd_tree', 'ball_tree'],  
    'p': [1, 2]  #Minkowski distance
}

# Create the GridSearchCV object with cv=10
knn_cv = GridSearchCV(KNN, parameters, cv=10, verbose=1, n_jobs=1) # Run on a single thread to avoid threadpool issues

# Fit the GridSearchCV object to the training data
knn_cv.fit(X_train, y_train)

# Print the best parameters and accuracy using format()
print("KNN - Tuned hyperparameters (best parameters): {}".format(knn_cv.best_params_))
print("KNN - Best cross-validated accuracy: {:.2f}".format(knn_cv.best_score_))

# Use the best estimator to calculate accuracy on the validation data (if available)
if 'X_val' in locals() or 'X_val' in globals():  # Check if validation set exists
    val_accuracy = knn_cv.best_estimator_.score(X_val, y_val)
    print('KNN - Validation Accuracy: {:.2f}'.format(val_accuracy))

# Use the best estimator to calculate accuracy on the test data
best_model_knn = knn_cv.best_estimator_
test_accuracy_knn = best_model_knn.score(X_test, y_test)
print('KNN - Test Accuracy: {:.2f}'.format(test_accuracy_knn))

# Make predictions using the KNN model
yhat_knn = best_model_knn.predict(X_test)
#print(X_test)

# Plot the confusion matrix for the KNN model
def plot_confusion_matrix(y_true, y_pred, title='Confusion Matrix'):
    cm = confusion_matrix(y_true, y_pred)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax, fmt='d', cmap='Blues');  # fmt='d' for integer annotations
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title(title)  # Set the title here
    ax.xaxis.set_ticklabels(['Did Not Land', 'Landed']); 
    ax.yaxis.set_ticklabels(['Did Not Land', 'Landed']) 
    plt.show()

# Plot the confusion matrix with a title
plot_confusion_matrix(y_test, yhat_knn, title='KNN Confusion Matrix')

# Which method performs the best?
# Assuming you have the following test accuracies from your models
test_accuracy_lr = 0.94  
test_accuracy_tree = 0.44
test_accuracy_knn = 0.78  
test_accuracy_svm = 0.89  

# Create a dictionary to hold the model names and their corresponding accuracies
model_accuracies = {
    'Logistic Regression': test_accuracy_lr,
    'Decision Tree': test_accuracy_tree,
    'KNN': test_accuracy_knn,
    'SVM': test_accuracy_svm
}

# Find the model with the highest accuracy
best_model = max(model_accuracies, key=model_accuracies.get)
best_accuracy = model_accuracies[best_model]

# Print the results using format()
print("Model Performance:")
for model, accuracy in model_accuracies.items():
    print("{}: Test Accuracy = {:.2f}".format(model, accuracy))

print("\nBest Performing Model: {} with Test Accuracy = {:.2f}".format(best_model, best_accuracy))

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Define the model performance data
model_accuracies = {
    'Logistic Regression': 0.94,
    'Decision Tree': 0.44,
    'KNN': 0.78,
    'SVM': 0.89
}

# Convert data to DataFrame
df_bar = pd.DataFrame(list(model_accuracies.items()), columns=['Model', 'Accuracy'])

# Create the barplot
plt.figure(figsize=(12, 6))
sns.barplot(x='Model', y='Accuracy', data=df_bar, order=df_bar.sort_values('Accuracy', ascending=False)['Model'])

# Title and labels
plt.title("Accuracies per Model", fontsize=20)
plt.xlabel("Models", fontsize=14)
plt.ylabel("Accuracy", fontsize=14)

# Display the plot
plt.tight_layout()
plt.show()