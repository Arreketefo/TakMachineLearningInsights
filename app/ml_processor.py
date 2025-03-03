import joblib
import numpy as np
from typing import Dict
import logging
from sklearn.ensemble import IsolationForest
from .schemas import CoTEvent

logger = logging.getLogger(__name__)

class MLProcessor:
    def __init__(self):
        # Initialize the ML model (Isolation Forest for anomaly detection)
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
        )
        self._train_initial_model()
    
    def _train_initial_model(self):
        """Train initial model with some sample data"""
        # Generate some sample normal data for initial training
        X_train = np.random.normal(size=(1000, 4))
        self.model.fit(X_train)
    
    def _extract_features(self, event: CoTEvent) -> np.ndarray:
        """Extract relevant features from CoT event"""
        features = np.array([
            event.lat,
            event.lon,
            event.speed or 0.0,
            event.course or 0.0
        ]).reshape(1, -1)
        return features
    
    def process_event(self, event: CoTEvent) -> Dict:
        """Process a CoT event and detect anomalies"""
        try:
            # Extract features
            features = self._extract_features(event)
            
            # Get anomaly score
            score = self.model.score_samples(features)[0]
            
            # Predict if anomaly (-1 for anomaly, 1 for normal)
            is_anomaly = self.model.predict(features)[0] == -1
            
            # Create enriched CoT
            enriched_cot = {
                "event_id": event.event_id,
                "type": event.type,
                "time": event.time.isoformat(),
                "lat": event.lat,
                "lon": event.lon,
                "altitude": event.altitude,
                "speed": event.speed,
                "course": event.course,
                "ml_enrichment": {
                    "anomaly_detected": is_anomaly,
                    "anomaly_score": float(score),
                    "confidence": float(np.exp(score) / (1 + np.exp(score)))
                }
            }
            
            return {
                "is_anomaly": is_anomaly,
                "anomaly_score": float(score),
                "enriched_cot": enriched_cot
            }
            
        except Exception as e:
            logger.error(f"Error processing event: {str(e)}")
            raise
