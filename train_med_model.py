import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import joblib

# Load dataset
df = pd.read_csv("synthetic_vitals_100k.csv")  # change filename if needed

# Separate features and target
X = df.drop(columns=["medications"])
y = df["medications"].str.split(",")

# Encode multiple medications as binary labels
mlb = MultiLabelBinarizer()
y_encoded = mlb.fit_transform(y)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y_encoded)

# Save the model and label binarizer
joblib.dump(model, "med_model.pkl")
joblib.dump(mlb, "med_labelizer.pkl")

print("Training complete. Model saved as med_model.pkl and med_labelizer.pkl")
