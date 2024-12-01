import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from joblib import dump

print("Loading data...")
file_path = '/Users/sofiagonzalez/Desktop/exoplanet.csv'
kepler_data = pd.read_csv(file_path, comment='#', low_memory=False)

print("Preprocessing data...")
features = [
    'koi_period', 'koi_time0bk', 'koi_impact', 'koi_duration', 'koi_depth',
    'koi_prad', 'koi_teq', 'koi_insol', 'koi_model_snr', 'koi_steff',
    'koi_slogg', 'koi_srad', 'ra', 'dec', 'koi_kepmag'
]
X = kepler_data[features]
y = kepler_data['koi_disposition']

imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Avoid stratification due to class with only one instance
print("Performing train-test split without stratification...")
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

print("Fitting a simple model for sanity check...")
simple_model = GradientBoostingClassifier(random_state=42)
simple_model.fit(X_train, y_train)
print("Simple model fitted. Proceeding to more complex grid search...")

param_grid = {
    'n_estimators': [100], 
    'max_depth': [3], 
    'learning_rate': [0.1]
}

cv_folds = StratifiedKFold(n_splits=3)  # Reduced CV folds due to class size constraints

print("Starting Grid Search CV with adjusted CV folds due to class size...")
gb_clf = GradientBoostingClassifier(random_state=42)
grid_search = GridSearchCV(estimator=gb_clf, param_grid=param_grid, cv=cv_folds, scoring='accuracy')
grid_search.fit(X_train, y_train)
print("Grid Search CV completed.")

best_clf = grid_search.best_estimator_

scores = cross_val_score(best_clf, X_scaled, y_encoded, cv=5, scoring='accuracy')
print(f"Average cross-validated score: {scores.mean():.2%}")

best_clf.fit(X_train, y_train)
y_pred = best_clf.predict_proba(X_test)
print(f"Test Set Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred))

dump(best_clf, '/Users/sofiagonzalez/Desktop/Innovation Engineering/my_trained_model.joblib')
dump(scaler, '/Users/sofiagonzalez/Desktop/Innovation Engineering/scaler.joblib')
dump(label_encoder, '/Users/sofiagonzalez/Desktop/Innovation Engineering/label_encoder.joblib')

print("Model and preprocessing objects saved to /Users/sofiagonzalez/Desktop/Innovation Engineering/")
