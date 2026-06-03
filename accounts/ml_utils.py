import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def predict_fraud_risk(balance, total_transactions, total_withdrawals, total_transfers):
    data = pd.DataFrame({
        "balance": [10000, 7000, 3000, 1000, 500, 200],
        "total_transactions": [2, 5, 8, 12, 18, 25],
        "total_withdrawals": [1, 2, 4, 7, 10, 15],
        "total_transfers": [0, 1, 3, 5, 8, 12],
        "risk": ["Low", "Low", "Medium", "Medium", "High", "High"]
    })

    X = data[[
        "balance",
        "total_transactions",
        "total_withdrawals",
        "total_transfers"
    ]]

    y = data["risk"]

    model = DecisionTreeClassifier()

    model.fit(X, y)

    prediction = model.predict([[
        float(balance),
        total_transactions,
        total_withdrawals,
        total_transfers
    ]])

    return prediction[0]