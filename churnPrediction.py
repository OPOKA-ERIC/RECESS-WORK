"""
OPOKA ERIC M.L 1 ASSIGNMENT
U/24/10784/EVE 2400710784
Classification - Predicting Customer Churn using Logistic Regression
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Sample data
data = {
    'MonthlyCharge': [50, 80, 70, 40, 90, 60, 100, 85, 45, 75],
    'ContractLength': [12, 6, 24, 12, 3, 18, 24, 6, 12, 18],
    'Age': [30, 25, 40, 35, 28, 50, 45, 32, 29, 55],
    'Churn': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
}

df = pd.DataFrame(data)

print("=" * 60)
print("CUSTOMER CHURN PREDICTION - LOGISTIC REGRESSION")
print("=" * 60)

print("\n[1] SAMPLE DATA")
print("-" * 40)
print(df.to_string(index=False))

# Features (X) and Target (y)
X = df[['MonthlyCharge', 'ContractLength', 'Age']].values
y = df['Churn'].values

# Train-test split (70% train, 30% test)
np.random.seed(42)
indices = np.random.permutation(len(X))
train_size = int(0.7 * len(X))
train_idx, test_idx = indices[:train_size], indices[train_size:]

X_train, X_test = X[train_idx], X[test_idx]
y_train, y_test = y[train_idx], y[test_idx]

print(f"\n[2] TRAIN-TEST SPLIT")
print("-" * 40)
print(f"Training samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")

# --- Logistic Regression from scratch using Gradient Descent ---

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def compute_cost(X, y, weights):
    m = len(y)
    h = sigmoid(X @ weights)
    epsilon = 1e-5
    cost = -(1/m) * (y.T @ np.log(h + epsilon) + (1 - y).T @ np.log(1 - h + epsilon))
    return cost

def gradient_descent(X, y, weights, learning_rate, iterations):
    m = len(y)
    cost_history = []
    for i in range(iterations):
        h = sigmoid(X @ weights)
        gradient = (1/m) * (X.T @ (h - y))
        weights -= learning_rate * gradient
        cost = compute_cost(X, y, weights)
        cost_history.append(cost)
    return weights, cost_history

# Add intercept term (bias)
X_train_bias = np.c_[np.ones(X_train.shape[0]), X_train]
X_test_bias = np.c_[np.ones(X_test.shape[0]), X_test]

# Initialize weights
np.random.seed(42)
weights = np.random.randn(X_train_bias.shape[1])

# Train the model
learning_rate = 0.01
iterations = 10000
weights, cost_history = gradient_descent(X_train_bias, y_train, weights, learning_rate, iterations)

print(f"\n[3] TRAINING COMPLETE")
print("-" * 40)
print(f"Final weights (coefficients):")
print(f"  Intercept (bias):        {weights[0]:.4f}")
print(f"  MonthlyCharge:           {weights[1]:.4f}")
print(f"  ContractLength:          {weights[2]:.4f}")
print(f"  Age:                     {weights[3]:.4f}")
print(f"Final cost:                {cost_history[-1]:.4f}")

# Predictions
y_prob = sigmoid(X_test_bias @ weights)
y_pred = (y_prob >= 0.5).astype(int)

print(f"\n[4] TEST SET PREDICTIONS")
print("-" * 40)
results = pd.DataFrame({
    'Actual': y_test,
    'Probability': np.round(y_prob, 4),
    'Predicted': y_pred
})
print(results.to_string(index=False))

# --- Evaluation Metrics ---

# Confusion Matrix
TP = np.sum((y_pred == 1) & (y_test == 1))
TN = np.sum((y_pred == 0) & (y_test == 0))
FP = np.sum((y_pred == 1) & (y_test == 0))
FN = np.sum((y_pred == 0) & (y_test == 1))

confusion_matrix = np.array([[TN, FP], [FN, TP]])

print(f"\n[5] CONFUSION MATRIX")
print("-" * 40)
print("              Predicted")
print("              Neg   Pos")
print(f"Actual Neg   {confusion_matrix[0,0]:>3}  {confusion_matrix[0,1]:>3}")
print(f"       Pos   {confusion_matrix[1,0]:>3}  {confusion_matrix[1,1]:>3}")

# Accuracy
accuracy = (TP + TN) / (TP + TN + FP + FN)

# Precision
precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0

# Recall (Sensitivity)
recall = TP / (TP + FN) if (TP + FN) > 0 else 0.0

# F1 Score
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

print(f"\n[6] CLASSIFICATION REPORT")
print("-" * 40)
print(f"{'':>12} {'Precision':>10} {'Recall':>8} {'F1-Score':>10} {'Support':>8}")
print(f"{'Class 0':>12} {TN/(TN+FN):>10.4f} {TN/(TN+FP):>8.4f} {2*(TN/(TN+FN)*TN/(TN+FP))/(TN/(TN+FN)+TN/(TN+FP)):>10.4f} {TN+FP:>8}")
print(f"{'Class 1':>12} {precision:>10.4f} {recall:>8.4f} {f1:>10.4f} {FN+TP:>8}")
print(f"{'Accuracy':>12} {'':>10} {'':>8} {accuracy:>10.4f} {'':>8}")

print(f"\n[7] KEY METRICS SUMMARY")
print("-" * 40)
print(f"Accuracy:           {accuracy:.4f}  ({accuracy*100:.2f}%)")
print(f"Precision:          {precision:.4f}")
print(f"Recall:             {recall:.4f}")
print(f"F1 Score:           {f1:.4f}")

print(f"\n[8] INTERPRETATION")
print("-" * 40)
if accuracy >= 0.8:
    print("The model performs well on this small dataset.")
elif accuracy >= 0.6:
    print("The model shows moderate performance.")
else:
    print("The model needs improvement (larger dataset / feature engineering).")

print(f"\n--- END OF REPORT ---")
