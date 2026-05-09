import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import random

# Create dataset

data = []

for i in range(5000):

    amount = random.randint(100, 50000)

    is_night = random.choice([0, 1])

    distance = random.randint(1, 500)

    unknown_device = random.choice([0, 1])

    new_merchant = random.choice([0, 1])

    foreign_transaction = random.choice([0, 1])

    fraud = 0

    # Fraud conditions

    if (
        amount > 10000
        and is_night == 1
        and unknown_device == 1
    ):
        fraud = 1

    if (
        foreign_transaction == 1
        and amount > 20000
    ):
        fraud = 1

    data.append([
        amount,
        is_night,
        distance,
        unknown_device,
        new_merchant,
        foreign_transaction,
        fraud
    ])

# Create dataframe

df = pd.DataFrame(data, columns=[
    'Amount',
    'Is_Night',
    'Distance_From_Home',
    'Unknown_Device',
    'New_Merchant',
    'Foreign_Transaction',
    'Fraud'
])

# Features and labels

X = df.drop('Fraud', axis=1)
y = df['Fraud']

# Split dataset

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model

model = RandomForestClassifier()

model.fit(X_train, y_train)

# Predictions

predictions = model.predict(X_test)

# Accuracy

accuracy = accuracy_score(y_test, predictions)

print("Accuracy:", accuracy)

# Save model

joblib.dump(model, 'fraud_model.pkl')

print("Model trained successfully")
print("fraud_model.pkl created")