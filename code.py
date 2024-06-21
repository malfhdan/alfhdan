# -*- coding: utf-8 -*-
"""Code.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m9aRWlh5IwMYiB5EuHdYxbD8iUOYn-uh
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
import os
import random
import warnings
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score,confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.ensemble import BaggingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier, LinearRegression
from sklearn.naive_bayes import GaussianNB, CategoricalNB
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier, VotingClassifier, AdaBoostClassifier
from joblib import parallel, delayed
import joblib
from sklearn.metrics import classification_report
random.seed(1)
os.environ['PYTHONHASHSEED'] = '0'
warnings.filterwarnings("ignore")

from google.colab import drive
drive.mount('/content/drive')

base_data = pd.read_csv('/content/drive/MyDrive/Paper3/KFH after updating-delet dignosis-merge all2.csv')

base_data = base_data.fillna(100)


#base_data.diagnosis.replace(["M", "B"], [1,0], inplace= True)
# base_data = base_data.drop('Unnamed: 32', axis=1)
# base_data.diagnosis.replace(["M", "B"], [1,0], inplace= True)
# X = base_data.drop(['id', 'diagnosis'], axis=1)
# y = base_data.diagnosis
X = base_data.drop(['result'], axis=1)
y = base_data.result


sns.despine()
ax = sns.countplot(y,label="Count")       # M = 212, B = 357
# sns.countplot(y, label='Count', color='blue')
B, M = y.value_counts()
print('Number of COVID-19 : ',B)
print('Number of Non-COVIDE : ',M)

from imblearn.over_sampling import RandomOverSampler
ros = RandomOverSampler(random_state=0)
ros.fit(X, y)
X_resampled, y_resampled = ros.fit_resample(X,y)
colors = ['#ef8a62' if v == B else '#f7f7f7' if v == M else '#67a9cf' for v in y_resampled]
plt.scatter(X_resampled.iloc[:, 0], X_resampled.iloc[:, 1], c=colors, linewidth=0.5, edgecolor='black')
sns.despine()
plt.title("Random Over-Sampler Output")
pass

ax = sns.countplot(y_resampled,label="Count")
B, M = y_resampled.value_counts()
print('Number of COVID-19 : ',B)
print('Number of Non-COVIDE : ',M)

import numpy as np
x_train, x_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

select_feature = SelectKBest(chi2, k=12).fit(x_train, y_train)
# print('Score list:', select_feature.scores_)
# print('Feature list:', x_train.columns)

for i,v in enumerate(select_feature.scores_):
	print('Feature: %0d, Score: %.5f' % (i,v))

x_train_2 = select_feature.transform(x_train)
x_test_2 = select_feature.transform(x_test)

select_feature.get_feature_names_out()

indices = np.argsort(select_feature.scores_)[::-1]
print(indices)

plt.figure(1, figsize=(14, 13))
plt.title("Selected Feature Scores")
plt.bar(range(x_train.shape[1]), select_feature.scores_[indices],
       color="blue",  align="center")
plt.xticks(range(x_train.shape[1]), x_train.columns[indices],rotation=90)
plt.xlim([-1, x_train.shape[1]])
plt.show()

#hyperparameter tuning

from sklearn.model_selection import GridSearchCV

para = {
    'n_estimators': [25, 50, 75, 100, 125, 150],
    'max_features': ['sqrt', 'log2', None],
    'max_depth': [3, 6, 9],
    'max_leaf_nodes': [3, 6, 9]
}


G_search = GridSearchCV(RandomForestClassifier(), param_grid=para, verbose=2, return_train_score=True)

G_search.fit(x_train_2, y_train)
y_pred = G_search.predict(x_test_2)
print(classification_report(y_pred, y_test))
print(G_search.best_estimator_)

classifier = RandomForestClassifier(max_depth=6, max_features='log2', max_leaf_nodes=9, n_estimators=50)
clr_rf_2 = classifier.fit(x_train_2,y_train)
y_pred = classifier.predict(x_test_2)
pred = classifier.predict(x_test_2)
from sklearn import metrics
print("Random Forest Classifier Accuracy(in %):", metrics.accuracy_score(y_test, y_pred)*100)
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print('==============')
print(y_pred.shape)
print(y_pred)
target_name = ['Non COVID-19', 'COVID-19']
cm = confusion_matrix(y_test , y_pred )
print('Print Classification Report')
CR = classification_report(y_test , y_pred , target_names=target_name)
print(CR)
print('\n')
total = sum(sum(cm))
acc = (cm[0, 0] + cm[1, 1]) / total
sensitivity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
specificity = cm[1, 1] / (cm[1, 0] + cm[1, 1])
print('Confusion Matrix \n')
print(cm)
print('\n')
print("acc: {:.4f}".format(acc))
print('\n')
print("sensitivity: {:.4f}".format(sensitivity))
print('\n')
print("specificity: {:.4f}".format(specificity))
plt.style.use('seaborn')
plt.figure(figsize=(15,12))
sns.set(font_scale=1.2)
sns.heatmap(cm , cmap='Blues' ,fmt='d' ,annot=True, xticklabels=target_name , yticklabels=target_name)
plt.title('Confusion Matrix of Random Forest Classifier')
# plt.savefig('final/machine/cm-SGDC.png', dpi=800 , bbox_inches='tight')
plt.show()
print('[Operation] Done .')
joblib.dump(classifier, 'filename.pkl')

from_joblib = joblib.load('/content/filename.pkl')
input =[[3, 2, 4, 0, 15, 0, 0,0, 5, 0, 0,1]]

predict = from_joblib.predict(input)
if predict == 0:
  print('non-covid-19')
else:
  print('covid-19')

#Cross Validation k=10
from sklearn.model_selection import cross_val_score
scores = cross_val_score(classifier, X_resampled, y_resampled, cv=10)

print(scores)


print("%0.2f Accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

#hyperparameter tuning

para = {
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}


G_search = GridSearchCV(DecisionTreeClassifier(), param_grid=para, verbose=2, return_train_score=True)

G_search.fit(x_train_2, y_train)
y_pred = G_search.predict(x_test_2)
print(classification_report(y_pred, y_test))
print(G_search.best_estimator_)

classifier1 = DecisionTreeClassifier(max_depth=30)
clr_rf_2 = classifier1.fit(x_train_2,y_train)
y_pred1 = classifier1.predict(x_test_2)
pred = classifier1.predict(x_test_2)
from sklearn import metrics
print("Decision Tree Classifier Accuracy(in %):", metrics.accuracy_score(y_test, y_pred1)*100)
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred1))
print(classification_report(y_test, y_pred1))
print('==============')
print(y_pred1.shape)
print(y_pred1)
target_name = ['Non COVID-19', 'COVID-19']
cm = confusion_matrix(y_test , y_pred1 )
print('Print Classification Report')
CR = classification_report(y_test , y_pred1 , target_names=target_name)
print(CR)
print('\n')
total = sum(sum(cm))
acc = (cm[0, 0] + cm[1, 1]) / total
sensitivity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
specificity = cm[1, 1] / (cm[1, 0] + cm[1, 1])
print('Confusion Matrix \n')
print(cm)
print('\n')
print("acc: {:.4f}".format(acc))
print('\n')
print("sensitivity: {:.4f}".format(sensitivity))
print('\n')
print("specificity: {:.4f}".format(specificity))
plt.style.use('seaborn')
plt.figure(figsize=(15,12))
sns.set(font_scale=1.2)
sns.heatmap(cm , cmap='Blues' ,fmt='d' ,annot=True, xticklabels=target_name , yticklabels=target_name)
plt.title('Confusion Matrix of Decision Tree Classifier')
# plt.savefig('final/machine/cm-SGDC.png', dpi=800 , bbox_inches='tight')
plt.show()
print('[Operation] Done .')

#Cross Validation k=10
from sklearn.model_selection import cross_val_score
scores = cross_val_score(classifier1, X_resampled, y_resampled, cv=10)

print(scores)


print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

#hyperparameter tuning

para = {
    'n_estimators': [10, 20, 30, 40, 50],
    'max_samples': [1, 0.9, 0.8, 0.7, 0.6],
    'max_features': [1, 0.9, 0.8, 0.7, 0.6]
}


G_search = GridSearchCV(BaggingClassifier(), param_grid=para, verbose=2, return_train_score=True)

G_search.fit(x_train_2, y_train)
y_pred = G_search.predict(x_test_2)
print(classification_report(y_pred, y_test))
print(G_search.best_estimator_)

classifier2 = BaggingClassifier(max_features=0.6, max_samples=0.8, n_estimators=50)
clr_rf_2 = classifier2.fit(x_train_2,y_train)
y_pred2 = classifier2.predict(x_test_2)
pred = classifier2.predict(x_test_2)
from sklearn import metrics
print("SVC Accuracy(in %):", metrics.accuracy_score(y_test, y_pred2)*100)
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred2))
print(classification_report(y_test, y_pred2))
print('==============')
print(y_pred2.shape)
print(y_pred2)
target_name = ['Non COVID-19', 'COVID-19']
cm = confusion_matrix(y_test , y_pred2 )
print('Print Classification Report')
CR = classification_report(y_test , y_pred2 , target_names=target_name)
print(CR)
print('\n')
total = sum(sum(cm))
acc = (cm[0, 0] + cm[1, 1]) / total
sensitivity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
specificity = cm[1, 1] / (cm[1, 0] + cm[1, 1])
print('Confusion Matrix \n')
print(cm)
print('\n')
print("acc: {:.4f}".format(acc))
print('\n')
print("sensitivity: {:.4f}".format(sensitivity))
print('\n')
print("specificity: {:.4f}".format(specificity))
plt.style.use('seaborn')
plt.figure(figsize=(15,12))
sns.set(font_scale=1.2)
sns.heatmap(cm , cmap='Blues' ,fmt='d' ,annot=True, xticklabels=target_name , yticklabels=target_name)
plt.title('Confusion Matrix of Bagging Classifier')
# plt.savefig('final/machine/cm-SGDC.png', dpi=800 , bbox_inches='tight')
plt.show()
print('[Operation] Done .')

#Cross Validation k=10
from sklearn.model_selection import cross_val_score
scores = cross_val_score(classifier2, X_resampled, y_resampled, cv=10)

print(scores)

print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

#hyperparameter tuning

para = {
    'multi_class': ['multinomial', 'auto', 'ovr'],
    'solver': ['lbfgs', 'liblinear', 'newton-cg', 'newton-cholesky', 'sag', 'saga'],
    'penalty': ['l1', 'l2', 'elasticnet', None],
    'tol': [0.0001, 0.001, 0.01]
}


G_search = GridSearchCV(LogisticRegression(), param_grid=para, verbose=2, return_train_score=True)

G_search.fit(x_train_2, y_train)
y_pred = G_search.predict(x_test_2)
print(classification_report(y_pred, y_test))
print(G_search.best_estimator_)

classifier3 = LogisticRegression(multi_class='multinomial', solver='newton-cholesky', tol=0.01)
clr_rf_2 = classifier3.fit(x_train_2,y_train)
y_pred3 = classifier3.predict(x_test_2)
pred = classifier3.predict(x_test_2)
from sklearn import metrics
print("Multinomial Logistic Regression Accuracy(in %):", metrics.accuracy_score(y_test, y_pred3)*100)
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred3))
print(classification_report(y_test, y_pred3))
print('==============')
print(y_pred3.shape)
print(y_pred3)
target_name = ['Non COVID-19', 'COVID-19']
cm = confusion_matrix(y_test , y_pred3 )
print('Print Classification Report')
CR = classification_report(y_test , y_pred3 , target_names=target_name)
print(CR)
print('\n')
total = sum(sum(cm))
acc = (cm[0, 0] + cm[1, 1]) / total
sensitivity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
specificity = cm[1, 1] / (cm[1, 0] + cm[1, 1])
print('Confusion Matrix \n')
print(cm)
print('\n')
print("acc: {:.4f}".format(acc))
print('\n')
print("sensitivity: {:.4f}".format(sensitivity))
print('\n')
print("specificity: {:.4f}".format(specificity))
plt.style.use('seaborn')
plt.figure(figsize=(15,12))
sns.set(font_scale=1.2)
sns.heatmap(cm , cmap='Blues' ,fmt='d' ,annot=True, xticklabels=target_name , yticklabels=target_name)
plt.title('Confusion Matrix of Multinomial Logistic Regression')
# plt.savefig('final/machine/cm-SGDC.png', dpi=800 , bbox_inches='tight')
plt.show()
print('[Operation] Done .')

#Cross Validation k=10
from sklearn.model_selection import cross_val_score
scores = cross_val_score(classifier3, X_resampled, y_resampled, cv=10)

print(scores)

print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

from sklearn.metrics import roc_curve, auc, roc_auc_score, precision_recall_curve, f1_score
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from keras.models import load_model
import numpy as np

fp , tp , threshold = roc_curve(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred)

fp1 , tp1 , threshold1 = roc_curve(y_test, y_pred1)
auc1 = roc_auc_score(y_test, y_pred1)

fp2 , tp2 , threshold2 = roc_curve(y_test, y_pred2)
auc2 = roc_auc_score(y_test, y_pred2)

fp3 , tp3 , threshold3 = roc_curve(y_test, y_pred3)
auc3 = roc_auc_score(y_test, y_pred3)

plt.style.use('ggplot')
plt.figure(1)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fp, tp, label='RF (Area = {:.3f})'.format(auc))
plt.plot(fp1, tp1, label='DT (Area = {:.3f})'.format(auc1))
plt.plot(fp2, tp2, label='BC (Area = {:.3f})'.format(auc2))
plt.plot(fp3, tp3, label='LR (Area = {:.3f})'.format(auc3))
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='lower right')
plt.savefig('ROC Curve VGG16&3kernel.png')

plt.show()





















