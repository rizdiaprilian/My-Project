from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score, make_scorer, recall_score, precision_score
from sklearn.metrics import roc_curve, precision_recall_curve, auc, plot_precision_recall_curve
from sklearn.model_selection import train_test_split
import streamlit as st
from dataclasses import dataclass
from typing import List
from Enum import Enum, Auto

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

def make_prediction(y_test, y_predict):
    precision, recall, fscore, _ = score(y_test, y_predict, average='binary')
    accuracy = accuracy_score(y_test, y_predict)
    conf_matrix_array = confusion_matrix(y_test, y_predict)
    tnr = precision_score(y_test, y_predict, pos_label=0, average='binary')
    npv = recall_score(y_test, y_predict, pos_label=0, average='binary')
    
    return precision, recall, fscore, accuracy, tnr, npv, conf_matrix_array

@dataclass
class LearnerInfo:

    learner: string = "Random Forest"

@dataclass
class Logistic_Regression(LearnerInfo):
    """Learning data and make prediction with logit method, Logistic Regression"""
    C: float = st.sidebar.number_input("Regularization parameter", 0.01, 10.0, step=0.01, key='C')
    max_iter: int = st.sidebar.slider("Max_iter", value=100, min_value=50, max_value=500, step=25)
    penalty: string = st.sidebar.radio("Penalty", ("l1", "l2"), key="penalty")

    def create_algorithm(self):
      return LogisticRegression(penalty = self.penalty, solver = 'liblinear',
                              C = self.C, class_weight="balanced", n_jobs=-1, 
                              max_iter=self.max_iter)

@dataclass
class Random_Forest(LearnerInfo):
    """Learning data and make prediction with tree-based method, Random Forest"""

    n_estimators: int = st.sidebar.slider('n_estimators', 
                        value=150, min_value=50, max_value=400, step=25)
    max_depth: int = st.sidebar.slider('Max_depth', 
                        value=3, min_value=2, max_value=8, step=1)
    max_samples: float = st.sidebar.slider('max_samples', 
                        value=0.3, min_value=0.2, max_value=0.8, step=0.1)

    def create_algorithm(self):
      return RandomForestClassifier(oob_score=True, random_state=42, 
                                class_weight="balanced", n_jobs=-1, 
                                n_estimators=self.n_estimators, max_depth=self.max_depth, 
                                max_samples=self.max_samples)

@dataclass
class SVM(LearnerInfo):
    """Learning data and make prediction with kernel-based method, SVM"""

    C: float = st.sidebar.number_input("Regularization parameter (C)", 0.01, 10.0, step=0.01, key='C')
    kernel: string = st.sidebar.radio("Kernel", ("rbf", "linear"), key="kernel")
    max_iter: int = st.sidebar.slider("Max_iter", value=100, min_value=50, max_value=500, step=25)

    def create_algorithm(self):
      return SVC(C=self.C, max_iter=self.max_iter, kernel=self.kernel, 
                 probability=True, class_weight="balanced", random_state=42)

def classification(classifier, X_train, y_train, X_test, y_test):
    if classifier == "Logistic Regression":
        model = Logistic_Regression("Logistic Regression")
        algo_lr = model.create_algorithm()
        algo_lr.fit(X_train, y_train)
        y_predict = algo_lr.predict(X_test)

    elif classifier == "SVM":
        model = SVM("SVM")
        algo_svm = model.create_algorithm()
        algo_svm.fit(X_train, y_train)
        y_predict = algo_svm.predict(X_test)

    elif classifier == "Random Forest":
        model = Random_Forest("Random Forest")
        algo_rf = model.create_algorithm()
        algo_rf.fit(X_train, y_train)
        y_predict = algo_rf.predict(X_test)
        
    precision, recall, fscore, accuracy, tnr, npv, conf_matrix_array = make_prediction(y_test, y_predict)
    fpr, tpr, thresholds = roc_curve(y_test, y_prob[:,1])
    auc = roc_auc_score(y_test, y_prob[:,1]).round(3)
    
    return precision, recall, fscore, accuracy, tnr, npv, conf_matrix_array
        
        
        
        
        
        
  
