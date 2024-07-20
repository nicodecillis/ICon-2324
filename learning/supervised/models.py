import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import RidgeClassifierCV


def decision_tree(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)

    tree = DecisionTreeClassifier()
    parameters_tree = {
        "criterion": ("gini", "entropy"),
        "max_depth": (5, 10, 20),
        "min_samples_split": (10, 20, 30),
        "min_samples_leaf": (10, 20, 30),
        "max_leaf_nodes": (10, 20, 30),
        "max_features": (0.1, 0.2)}      # valore basso per evitare l'overfitting

    grid_search_tree = GridSearchCV(
        estimator=tree,
        param_grid=parameters_tree,
        scoring="accuracy",
        n_jobs=-1,
        cv=10,
        refit=True
    )

    grid_search_tree.fit(x_train, y_train)
    best_decision_tree = grid_search_tree.best_estimator_
    y_pred_test = best_decision_tree.predict(x_test)

    with open("results/decision_tree.txt", "w") as file:
        file.write("Best parameters found: " + str(grid_search_tree.best_params_) + "\n")
        file.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred_test)) + "\n")
        file.write("Confusion matrix:\n" + str(metrics.confusion_matrix(y_test, y_pred_test)) + "\n")
        file.write("Classification report:\n" + str(metrics.classification_report(y_test, y_pred_test)) + "\n")


def knn(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)

    knn = KNeighborsClassifier()
    parameters_knn = {
        "n_neighbors": (3, 5, 7, 9, 10, 11, 13, 15),
        "weights": ["uniform"],
        "metric": ("minkowski", "manhattan", "euclidean", "chebyshev")}

    grid_search_knn = GridSearchCV(
        estimator=knn,
        param_grid=parameters_knn,
        scoring="accuracy",
        n_jobs=-1,
        cv=10,
        refit=True
    )

    grid_search_knn.fit(x_train, y_train)
    best_knn = grid_search_knn.best_estimator_
    y_pred_test = best_knn.predict(x_test)

    with open("results/knn.txt", "w") as file:
        file.write("Best parameters found: " + str(grid_search_knn.best_params_) + "\n")
        file.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred_test)) + "\n")
        file.write("Confusion matrix:\n" + str(metrics.confusion_matrix(y_test, y_pred_test)) + "\n")
        file.write("Classification report:\n" + str(metrics.classification_report(y_test, y_pred_test)) + "\n")


def gaussian_nb(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)

    gau = GaussianNB()
    parameters_gau = {'var_smoothing': np.logspace(0, -9, num=200)}
    grid_search_gau = GridSearchCV(
        estimator=gau,
        param_grid=parameters_gau,
        scoring='accuracy',
        n_jobs=-1,
        cv=10,
        refit=True,
    )

    grid_search_gau.fit(x_train, y_train)
    best_gau = grid_search_gau.best_estimator_
    y_pred_test = best_gau.predict(x_test)

    with open("results/gaussian_nb.txt", "w") as file:
        file.write("Best parameters found: " + str(grid_search_gau.best_params_) + "\n")
        file.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred_test)) + "\n")
        file.write("Confusion matrix:\n" + str(metrics.confusion_matrix(y_test, y_pred_test)) + "\n")
        file.write("Classification report:\n" + str(metrics.classification_report(y_test, y_pred_test)) + "\n")


def support_vector_machine(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)

    svm = SVC()
    parameters_svm = {
        'C': [0.1, 1, 10, 50],
        'gamma': ['scale', 'auto'],
        'kernel': ['rbf', 'sigmoid'],
    }

    grid_search_svm = GridSearchCV(
        estimator=svm,
        param_grid=parameters_svm,
        scoring='accuracy',
        n_jobs=-1,
        cv=10,
        refit=True,
        verbose=3
    )

    grid_search_svm.fit(x_train, y_train)
    best_svm = grid_search_svm.best_estimator_
    y_pred_test = best_svm.predict(x_test)

    with open("results/svm.txt", "w") as file:
        file.write("Best parameters found: " + str(grid_search_svm.best_params_) + "\n")
        file.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred_test)) + "\n")
        file.write("Confusion matrix:\n" + str(metrics.confusion_matrix(y_test, y_pred_test)) + "\n")
        file.write("Classification report:\n" + str(metrics.classification_report(y_test, y_pred_test)) + "\n")


def random_forest(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)

    rf = RandomForestClassifier()
    parameters_rf = {
        'n_estimators': (250, 300),
        'max_depth': [None],
        'min_samples_split': (2, 4, 6),
        'min_samples_leaf': (1, 2, 4),
        'max_features': [0.1, 0.2, 0.3],
    }

    grid_search_rf = GridSearchCV(
        estimator=rf,
        param_grid=parameters_rf,
        scoring='accuracy',
        n_jobs=-1,
        cv=5,
        refit=True,
        verbose=3
    )

    grid_search_rf.fit(x_train, y_train)
    best_rf = grid_search_rf.best_estimator_
    y_pred_test = best_rf.predict(x_test)

    with open("results/random_forest.txt", "w") as file:
        file.write("Best parameters found: " + str(grid_search_rf.best_params_) + "\n")
        file.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred_test)) + "\n")
        file.write("Confusion matrix:\n" + str(metrics.confusion_matrix(y_test, y_pred_test)) + "\n")
        file.write("Classification report:\n" + str(metrics.classification_report(y_test, y_pred_test)) + "\n")


def ada_boost(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)

    ada = AdaBoostClassifier()
    parameters_ada = {
        'n_estimators': (50, 100, 200, 300),
        'learning_rate': (0.01, 0.1, 0.5, 1, 1.5),
        'algorithm': ['SAMME'],
        'estimator': (GaussianNB(), DecisionTreeClassifier(max_depth=1), DecisionTreeClassifier(max_depth=3),
                      DecisionTreeClassifier(max_depth=5), RidgeClassifierCV())
    }

    grid_search_ada = GridSearchCV(
        estimator=ada,
        param_grid=parameters_ada,
        scoring='accuracy',
        n_jobs=-1,
        cv=10,
        refit=True,
        verbose=3
    )

    grid_search_ada.fit(x_train, y_train)
    best_ada = grid_search_ada.best_estimator_
    y_pred_test = best_ada.predict(x_test)

    with open("results/ada_boost.txt", "w") as file:
        file.write("Best parameters found: " + str(grid_search_ada.best_params_) + "\n")
        file.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred_test)) + "\n")
        file.write("Confusion matrix:\n" + str(metrics.confusion_matrix(y_test, y_pred_test)) + "\n")
        file.write("Classification report:\n" + str(metrics.classification_report(y_test, y_pred_test)) + "\n")


def neural_network(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)

    nn = MLPClassifier()
    parameters_nn = {
        'hidden_layer_sizes': [(200, 100, 50, 25)],
        'activation': ['tanh', 'relu'],
        'solver': ['sgd', 'adam'],
        'alpha': [0.0001, 0.001],
        'learning_rate': ['constant', 'adaptive'],
        'max_iter': [700]
    }

    grid_search_nn = GridSearchCV(
        estimator=nn,
        param_grid=parameters_nn,
        scoring='accuracy',
        n_jobs=-1,
        cv=10,
        refit=True,
        verbose=3,
    )

    grid_search_nn.fit(x_train, y_train)
    best_nn = grid_search_nn.best_estimator_
    y_pred_test = best_nn.predict(x_test)

    with open("results/neural_network.txt", "w") as file:
        file.write("Best parameters found: " + str(grid_search_nn.best_params_) + "\n")
        file.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred_test)) + "\n")
        file.write("Confusion matrix:\n" + str(metrics.confusion_matrix(y_test, y_pred_test)) + "\n")
        file.write("Classification report:\n" + str(metrics.classification_report(y_test, y_pred_test)) + "\n")


df = pd.read_csv("../../dataset/balanced-playstore-apps.csv", na_filter=False)
df["Success Rate"] = df["Success Rate"].replace("Not very popular", 1)
df["Success Rate"] = df["Success Rate"].replace("Mildly popular", 2)
df["Success Rate"] = df["Success Rate"].replace("Popular", 3)
df["Success Rate"] = df["Success Rate"].replace("Very popular", 4)

df["Size (MB)"] = df["Size (MB)"].replace("Varies with device", -1)

categorical_features = ["App Name", "App Id", "Category", "Minimum Android", "Developer Id", "Content Rating", "Last Updated"]
encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
df[categorical_features] = encoder.fit_transform(df[categorical_features])

training = df.drop(columns=["Downloads", "Rating Count", "Rating", "Success Rate", "Last Updated"], axis=1)
target = df["Success Rate"]

df.to_csv("../../dataset/encoded-playstore-apps.csv", index=False)

# decision_tree(training, target)
# knn(training, target)
# gaussian_nb(training, target)
# support_vector_machine(training, target)
# random_forest(training, target)
# ada_boost(training, target)
# neural_network(training, target)
