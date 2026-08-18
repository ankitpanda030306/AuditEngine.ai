import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

class LogAnomalyDetector:
    def __init__(self):
        # Isolation Forest flags anomalous data points in log metrics
        self.model = IsolationForest(contamination=0.15, random_state=42)
        self._fit_mock_baseline()

    def _fit_mock_baseline(self):
        # Generate baseline normal metrics: [login_failures, cpu_util_pct, req_rate_per_sec]
        normal_data = np.random.normal(loc=[1, 35, 100], scale=[0.5, 10, 20], size=(200, 3))
        # Add some anomalous spikes
        anomalous_data = np.random.uniform(low=[10, 85, 500], high=[50, 99, 2000], size=(30, 3))
        X_train = np.vstack([normal_data, anomalous_data])
        self.model.fit(X_train)

    def analyze_log_metrics(self, login_failures: int, cpu_usage: float, request_rate: float) -> dict:
        sample = np.array([[login_failures, cpu_usage, request_rate]])
        prediction = self.model.predict(sample)[0]  # -1 = anomaly, 1 = normal
        score = float(self.model.decision_function(sample)[0])
        
        # Scale score into a human-readable 0-100 Risk Score
        risk_score = min(max(int((0.5 - score) * 100), 5), 98)
        
        status = "HIGH RISK (Anomaly Detected)" if prediction == -1 else "NORMAL"
        return {
            "status": status,
            "risk_score": risk_score,
            "is_anomaly": bool(prediction == -1)
        }

if __name__ == "__main__":
    detector = LogAnomalyDetector()
    test_normal = detector.analyze_log_metrics(login_failures=1, cpu_usage=40.0, request_rate=120.0)
    test_attack = detector.analyze_log_metrics(login_failures=25, cpu_usage=95.0, request_rate=1500.0)
    
    print("Normal Metric Test:", test_normal)
    print("Attack Spike Metric Test:", test_attack)