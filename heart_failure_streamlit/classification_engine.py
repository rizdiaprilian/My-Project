from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score, make_scorer, recall_score, precision_score
from sklearn.metrics import roc_curve, precision_recall_curve, auc, plot_precision_recall_curve
from sklearn.model_selection import train_test_split
import streamlit as st

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


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

        precision, recall, fscore, _ = score(y_test, rf_model_predict, average='binary')
        accuracy = accuracy_score(y_test, rf_model_predict)
        conf_matrix_array = confusion_matrix(y_test, rf_model_predict)
        tnr = precision_score(y_test, rf_model_predict, pos_label=0, average='binary')
        npv = recall_score(y_test, rf_model_predict, pos_label=0, average='binary')

    elif classifier == "Support Vector Machine":
        C = st.sidebar.number_input("Regularization parameter (C)", 0.01, 10.0, step=0.01, key='C')
        kernel = st.sidebar.radio("Kernel", ("rbf", "linear"), key="kernel")
        max_iter = st.sidebar.slider("Max_iter", value=100, min_value=50, max_value=500, step=25)

        rbf_svc_model = SVC(C=C, max_iter=max_iter, kernel=kernel, probability=True, class_weight="balanced", random_state=42)
        rbf_svc_model.fit(X_train, y_train)
        rbf_svm_predict = rbf_svc_model.predict(X_test)
        y_prob = rbf_svc_model.predict_proba(X_test)

        precision, recall, fscore, _ = score(y_test, rbf_svm_predict, average='binary')
        accuracy = accuracy_score(y_test, rbf_svm_predict)
        conf_matrix_array = confusion_matrix(y_test, rbf_svm_predict)
        tnr = precision_score(y_test, rbf_svm_predict, pos_label=0, average='binary')
        npv = recall_score(y_test, rbf_svm_predict, pos_label=0, average='binary')

    elif classifier == "Logistic Regression":
        C = st.sidebar.number_input("Regularization parameter", 0.01, 10.0, step=0.01, key='C')
        max_iter = st.sidebar.slider("Max_iter", value=100, min_value=50, max_value=500, step=25)
        penalty = st.sidebar.radio("Penalty", ("l1", "l2"), key="penalty")
        lr_model = LogisticRegression(penalty = penalty, solver = 'liblinear',
                              C = C, class_weight="balanced", n_jobs=-1, max_iter=max_iter)
        lr_model.fit(X_train, y_train)
        lr_predict = lr_model.predict(X_test)
        y_prob = lr_model.predict_proba(X_test)

        precision, recall, fscore, _ = score(y_test, lr_predict, average='binary')
        accuracy = accuracy_score(y_test, lr_predict)
        conf_matrix_array = confusion_matrix(y_test, lr_predict)
        tnr = precision_score(y_test, lr_predict, pos_label=0, average='binary')
        npv = recall_score(y_test, lr_predict, pos_label=0, average='binary')


    fpr, tpr, thresholds = roc_curve(y_test, y_prob[:,1])
    auc = roc_auc_score(y_test, y_prob[:,1]).round(3)

    return precision, recall, fscore, accuracy, tnr, npv, fpr, tpr, auc, y_prob, conf_matrix_array