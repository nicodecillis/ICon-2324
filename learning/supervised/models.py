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
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.linear_model import RidgeClassifierCV
import joblib


def save_results(title, best_params, y_test, y_pred_test, accuracy):
    with open("results/" + title + ".txt", "w") as file:
        file.write("Best parameters found: " + str(best_params) + "\n")
        file.write("Accuracy: " + str(accuracy) + "\n")
        file.write("Confusion matrix:\n" + str(metrics.confusion_matrix(y_test, y_pred_test)) + "\n")
        file.write("Classification report:\n" + str(metrics.classification_report(y_test, y_pred_test)) + "\n")


def compare_accuracy(tree_accuracy, knn_accuracy, gau_accuracy, svm_accuracy, rf_accuracy, ada_accuracy, nn_accuracy):
    accuracies = {
        "tree": tree_accuracy,
        "knn": knn_accuracy,
        "gau": gau_accuracy,
        "svm": svm_accuracy,
        "rf": rf_accuracy,
        "ada": ada_accuracy,
        "nn": nn_accuracy
    }
    best_model = max(accuracies, key=accuracies.get)
    return best_model


def save_model(model, filename):
    joblib.dump(model, filename)


def decision_tree(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

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
        refit=True,
        verbose=3
    )

    grid_search_tree.fit(x_train, y_train)
    best_decision_tree = grid_search_tree.best_estimator_
    best_params = grid_search_tree.best_params_
    y_pred_test = best_decision_tree.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred_test)

    return best_decision_tree, best_params, y_test, y_pred_test, accuracy


def knn(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

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
        refit=True,
        verbose=3
    )

    grid_search_knn.fit(x_train, y_train)
    best_knn = grid_search_knn.best_estimator_
    best_params = grid_search_knn.best_params_
    y_pred_test = best_knn.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred_test)

    return best_knn, best_params, y_test, y_pred_test, accuracy


def gaussian_nb(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    gau = GaussianNB()
    parameters_gau = {'var_smoothing': np.logspace(0, -9, num=200)}
    grid_search_gau = GridSearchCV(
        estimator=gau,
        param_grid=parameters_gau,
        scoring='accuracy',
        n_jobs=-1,
        cv=10,
        refit=True,
        verbose=3
    )

    grid_search_gau.fit(x_train, y_train)
    best_gau = grid_search_gau.best_estimator_
    best_params = grid_search_gau.best_params_
    y_pred_test = best_gau.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred_test)

    return best_gau, best_params, y_test, y_pred_test, accuracy


def support_vector_machine(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

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
    best_params = grid_search_svm.best_params_
    y_pred_test = best_svm.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred_test)

    return best_svm, best_params, y_test, y_pred_test, accuracy


def random_forest(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

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
        cv=10,
        refit=True,
        verbose=3
    )

    grid_search_rf.fit(x_train, y_train)
    best_rf = grid_search_rf.best_estimator_
    best_params = grid_search_rf.best_params_
    y_pred_test = best_rf.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred_test)

    return best_rf, best_params, y_test, y_pred_test, accuracy


def ada_boost(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    ada = AdaBoostClassifier()
    parameters_ada = {
        'n_estimators': (50, 100, 200, 300),
        'learning_rate': (0.01, 0.1, 0.5, 1, 1.5),
        'algorithm': ['SAMME'],
        'estimator': (GaussianNB(), RidgeClassifierCV(), DecisionTreeClassifier(), RandomForestClassifier())
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
    best_params = grid_search_ada.best_params_
    y_pred_test = best_ada.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred_test)

    return best_ada, best_params, y_test, y_pred_test, accuracy


def neural_network(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    nn = MLPClassifier()
    parameters_nn = {
        'hidden_layer_sizes': [(10,), (50,), (120, 80, 40), (150, 100, 50)],     # (100, 50, 30)
        'activation': ['tanh', 'relu'],
        'solver': ['sgd', 'adam'],
        'alpha': [0.001, 0.05],     # 0.0001
        'learning_rate': ['constant', 'adaptive'],
        'max_iter': [1500]
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
    best_params = grid_search_nn.best_params_
    y_pred_test = best_nn.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred_test)

    return best_nn, best_params, y_test, y_pred_test, accuracy


df = pd.read_csv("../../dataset/finalized-playstore-apps.csv", na_filter=False)
df["Success Rate"] = df["Success Rate"].replace("Not very popular", 1)
df["Success Rate"] = df["Success Rate"].replace("Mildly popular", 2)
df["Success Rate"] = df["Success Rate"].replace("Popular", 3)
df["Success Rate"] = df["Success Rate"].replace("Very popular", 4)

df["Size (MB)"] = df["Size (MB)"].replace("Varies with device", -1)

categorical_features = ["App Name", "App Id", "Category", "Minimum Android", "Developer Id", "Content Rating", "Last Updated"]
encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
df[categorical_features] = encoder.fit_transform(df[categorical_features])

training = df.drop(columns=["Downloads", "Rating", "Editors Choice", "Success Rate"], axis=1)
target = df["Success Rate"]

# Dataset numerico per prediction e elbow method
encoded_df = pd.concat([df[["App Name", "App Id", "Category", "Price ($)", "Rating", "Downloads", "Content Rating",
                            "Developer Id", "Minimum Android", "Last Updated", "Editors Choice"]], target], axis=1)
encoded_df.to_csv("../../dataset/encoded-playstore-apps.csv", index=False)


best_tree, best_tree_params, y_test_tree, y_pred_test_tree, tree_accuracy = decision_tree(training, target)
save_results("decision_tree", best_tree_params, y_test_tree, y_pred_test_tree, tree_accuracy)

best_knn, best_knn_params, y_test_knn, y_pred_test_knn, knn_accuracy = knn(training, target)
save_results("knn", best_knn_params, y_test_knn, y_pred_test_knn, knn_accuracy)

best_gau, best_gau_params, y_test_gau, y_pred_test_gau, gau_accuracy = gaussian_nb(training, target)
save_results("gaussian_nb", best_gau_params, y_test_gau, y_pred_test_gau, gau_accuracy)

best_svm, best_svm_params, y_test_svm, y_pred_test_svm, svm_accuracy = support_vector_machine(training, target)
save_results("svm", best_svm_params, y_test_svm, y_pred_test_svm, svm_accuracy)

best_rf, best_rf_params, y_test_rf, y_pred_test_rf, rf_accuracy = random_forest(training, target)
save_results("random_forest", best_rf_params, y_test_rf, y_pred_test_rf, rf_accuracy)

best_ada, best_ada_params, y_test_ada, y_pred_test_ada, ada_accuracy = ada_boost(training, target)
save_results("ada_boost", best_ada_params, y_test_ada, y_pred_test_ada, ada_accuracy)

best_nn, best_nn_params, y_test_nn, y_pred_test_nn, nn_accuracy = neural_network(training, target)
save_results("neural_network", best_nn_params, y_test_nn, y_pred_test_nn, nn_accuracy)

best_model = compare_accuracy(tree_accuracy, knn_accuracy, gau_accuracy, svm_accuracy, rf_accuracy, ada_accuracy, nn_accuracy)
save_model(globals()["best_" + best_model], "results/best_model.joblib")
