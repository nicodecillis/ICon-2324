import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import OrdinalEncoder


def decision_tree(training, target):
    x_train, x_test, y_train, y_test = train_test_split(training, target, test_size=0.3, random_state=42)

    tree = DecisionTreeClassifier()
    parameters_tree = {
        "criterion": ("gini", "entropy"),
        "max_depth": (None, 5, 10, 20, 30),
        "min_samples_split": (2, 5, 10, 20, 30),
        "min_samples_leaf": (1, 2, 5, 10, 20, 30),
        "max_features": (0.5, "sqrt", "log2")}

    grid_search_tree = GridSearchCV(
        estimator=tree,
        param_grid=parameters_tree,
        scoring="accuracy",
        n_jobs=-1,
        cv=5)

    grid_search_tree.fit(x_train, y_train)
    print("Best parameters found: ", grid_search_tree.best_params_)
    return grid_search_tree


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

"""
cross_val_score_plot(cross_val_score(best_dtc, X, y, cv=k), "decision_tree", save=True, display=False)
confusion_matrix_plot(confusion_matrix(y, best_y_pred, labels=LABELS), LABELS, "decision_tree", save=True,
                      display=False)
report = classification_report(y, best_y_pred)
return "Decision Tree\n" + "criteria: " + best_criterion + "\nmax_depth: " + str(
    best_max_depth) + "\nmin_samples_split: " + str(best_min_samples_split) + "\nmin_samples_leaf: " + str(
    best_min_samples_leaf) + "\n" + report + "\n"
"""
