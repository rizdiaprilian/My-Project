from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score, make_scorer, recall_score, precision_score
from sklearn.metrics import roc_curve, precision_recall_curve, auc, plot_precision_recall_curve
from sklearn.model_selection import train_test_split
import streamlit as st

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

class LearnerInfo:
  
  
def classification(classifier, X_train, y_train, X_test, y_test):
    if classifier == "Random Forest":
        n_estimators = st.sidebar.slider('n_estimators', 
                        value=150, min_value=50, max_value=400, step=25)
        max_depth = st.sidebar.slider('Max_depth', 
                        value=3, min_value=2, max_value=8, step=1)
        max_samples = st.sidebar.slider('max_samples', 
                        value=0.3, min_value=0.2, max_value=0.8, step=0.1)
        rf_model = RandomForestClassifier(oob_score=True, random_state=42, 
                                class_weight="balanced", n_jobs=-1, 
                                n_estimators = n_estimators, max_depth=max_depth, max_samples=max_samples)
        rf_model.fit(X_train, y_train)
        rf_model_predict = rf_model.predict(X_test)
        y_prob = rf_model.predict_proba(X_test)
        
        precision, recall, fscore, accuracy, tnr, npv, conf_matrix_array = make_prediction(y_test, rf_model_predict)
        
    fpr, tpr, thresholds = roc_curve(y_test, y_prob[:,1])
    auc = roc_auc_score(y_test, y_prob[:,1]).round(3)

    return precision, recall, fscore, accuracy, tnr, npv, fpr, tpr, auc, y_prob, conf_matrix_array
        
        
        
        
        
        
  
