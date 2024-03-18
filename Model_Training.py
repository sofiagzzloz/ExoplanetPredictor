import pandas as pd

file_path = '/Users/sofiagonzalez/Desktop/exoplanet.csv'

# Loading the dataset by skipping initial comment lines
kepler_data = pd.read_csv(file_path, comment='#')

# Displaying the first few rows of the dataset to understand its structure and contents
kepler_data.head()


# Import statements
from sklearn.model_selection import train_test_split #splitting the data set
from sklearn.ensemble import RandomForestClassifier #select the random forest algorithm
from sklearn.metrics import accuracy_score, classification_report #evaluating the model accuracy
from sklearn.impute import SimpleImputer #for the missing values
from sklearn.preprocessing import LabelEncoder #encoding labels. from labels into numerical form
import pandas as pd

try:
    kepler_data = pd.read_csv(file_path, comment='#', low_memory=False)
except FileNotFoundError:
    print(f"File not found at {file_path}. Please check the file path.")
    exit()

# Check for missing values in the dataset
if kepler_data.isnull().sum().any():
    print("Warning: Missing values detected in the dataset. Consider handling them before proceeding.")

# Preprocessing the data
features = [
    'koi_period', 'koi_time0bk', 'koi_impact', 'koi_duration', 'koi_depth',
    'koi_prad', 'koi_teq', 'koi_insol', 'koi_model_snr', 'koi_steff',
    'koi_slogg', 'koi_srad', 'ra', 'dec', 'koi_kepmag'
]
X = kepler_data[features]
y = kepler_data['koi_disposition']

# Handling missing values in features
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Check for missing values in target variable
if y.isnull().any():
    print("Warning: Missing values detected in the target variable. Consider handling them before proceeding.")

# Encoding the target variable
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Model evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Print model evaluation summary
def format_classification_report(report):
    lines = report.split('\n')
    header = "| " + " | ".join(lines[0].split()) + " |"
    separator = "|-" + "-|-".join(["-" * len(col) for col in lines[0].split()]) + "-|"
    formatted_report = header + "\n" + separator + "\n"
    for line in lines[2:6]:
        formatted_report += "| " + " | ".join(line.split()) + " |\n"
    return formatted_report

formatted_report = format_classification_report(report)
print("Model Evaluation Summary\n------------------------")
print(f"Overall Model Accuracy: {accuracy:.2%}\n")
print("Classification Report:\n")
print(formatted_report)

from joblib import dump

model_filename = '/Users/sofiagonzalez/Desktop/Innovation Engineering/my_trained_model.joblib'

# Save the model
dump(model, model_filename)

print(f"Model saved to {model_filename}")

