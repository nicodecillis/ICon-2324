import pandas as pd
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
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
        scoring="accuracy",     # sceglie modello migliore in base all'accuratezza
        n_jobs=-1,
        cv=5,   # 5-fold cross validation (o 10?)
        refit=True)    # refit=True: retraining del modello migliore su tutto il dataset

    grid_search_tree.fit(x_train, y_train)
    print("Best parameters found: ", grid_search_tree.best_params_)
    best_decision_tree = grid_search_tree.best_estimator_
    return best_decision_tree


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

best_dtc = decision_tree(training, target)
cross_val_score(best_dtc, training, target, cv=5)   # 5-fold cross validation (o 10?)
confusion_matrix(target, best_dtc.predict(training))

print(classification_report(target, best_dtc.predict(training)))
print("accuracy score:" , accuracy_score(target, best_dtc.predict(training)))






