from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProcessedEvent(Base):
    """Model to store processed CoT events and their ML analysis results"""
    __tablename__ = 'processed_events'

    id = Column(Integer, primary_key=True)
    event_id = Column(String(100), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    altitude = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    course = Column(Float, nullable=True)
    
    # ML processing results
    is_anomaly = Column(Boolean, nullable=False)
    anomaly_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    
    # Additional data
    raw_cot = Column(JSON, nullable=True)
    enriched_cot = Column(JSON, nullable=True)
    
    # Audit fields
    processed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    processing_time_ms = Column(Float, nullable=True)

    def __repr__(self):
        return f"<ProcessedEvent(event_id='{self.event_id}', is_anomaly={self.is_anomaly})>"

class MLModelMetrics(Base):
    """Model to store ML model performance metrics"""
    __tablename__ = 'ml_model_metrics'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    model_version = Column(String(50), nullable=False)
    events_processed = Column(Integer, nullable=False, default=0)
    anomalies_detected = Column(Integer, nullable=False, default=0)
    avg_processing_time = Column(Float, nullable=True)
    false_positive_rate = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"<MLModelMetrics(model_version='{self.model_version}', events_processed={self.events_processed})>"

class APIMetrics(Base):
    """Model to store API performance metrics"""
    __tablename__ = 'api_metrics'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    endpoint = Column(String(200), nullable=False)
    method = Column(String(10), nullable=False)
    response_time_ms = Column(Float, nullable=False)
    status_code = Column(Integer, nullable=False)
    client_id = Column(String(100), nullable=True)
    error_message = Column(String(500), nullable=True)

    def __repr__(self):
        return f"<APIMetrics(endpoint='{self.endpoint}', status_code={self.status_code})>"

class AuditLog(Base):
    """Model to store security audit logs"""
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    event_type = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    client_ip = Column(String(50), nullable=True)
    api_key_id = Column(String(100), nullable=True)
    severity = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<AuditLog(event_type='{self.event_type}', severity='{self.severity}')>"
