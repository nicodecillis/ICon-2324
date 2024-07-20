import pandas as pd
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import OrdinalEncoder


def decision_tree(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)

    tree = DecisionTreeClassifier()
    parameters_tree = {
        "criterion": ("gini", "entropy"),
        "max_depth": (5, 10, 20),
        "min_samples_split": (10, 20, 30),
        "min_samples_leaf": (10, 20, 30),
        "max_leaf_nodes": (10, 20, 30),
        "max_features": (0.1, 0.2, 0.3)}      # valore basso per evitare l'overfitting

    """
    parameters_tree = {
        "criterion": ("gini", "entropy"),
        "max_depth": (None, 5, 10, 20, 30),
        "min_samples_split": (2, 5, 10, 20, 30),
        "min_samples_leaf": (1, 2, 5, 10, 20, 30),
        "max_features": (0.5, "sqrt", "log2")}
    """

    grid_search_tree = GridSearchCV(
        estimator=tree,
        param_grid=parameters_tree,
        scoring="accuracy",
        n_jobs=-1,
        cv=5,
        refit=True)

    grid_search_tree.fit(x_train, y_train)
    print("Best parameters found: ", grid_search_tree.best_params_)
    best_decision_tree = grid_search_tree.best_estimator_
    # best_decision_tree.fit(x_train, y_train)
    y_pred = best_decision_tree.predict(x_test)
    print("Accuracy: ", metrics.accuracy_score(y_test, y_pred))
    print("Confusion matrix: ", metrics.confusion_matrix(y_test, y_pred))
    print("Classification report: ", metrics.classification_report(y_test, y_pred))


df = pd.read_csv("../../dataset/balanced-playstore-apps.csv")
df["Success Rate"] = df["Success Rate"].replace("Not very popular", 1)
df["Success Rate"] = df["Success Rate"].replace("Mildly popular", 2)
df["Success Rate"] = df["Success Rate"].replace("Popular", 3)
df["Success Rate"] = df["Success Rate"].replace("Very popular", 4)

df["Size (MB)"] = df["Size (MB)"].replace("Varies with device", -1)

categorical_features = ["App Name", "App Id", "Category", "Minimum Android", "Developer Id", "Last Updated", "Content Rating"]
encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
df[categorical_features] = encoder.fit_transform(df[categorical_features])


training = df.drop("Success Rate", axis=1)
target = df["Success Rate"]
decision_tree(training, target)
