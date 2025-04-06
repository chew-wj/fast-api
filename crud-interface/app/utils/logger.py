import logging
import logging.handlers
import json
from datetime import datetime
from typing import Any, Dict
import os

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            "logs/app.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _format_message(self, message: str, extra: Dict[str, Any] = None) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            **(extra or {})
        }
        return json.dumps(log_data)
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        self.logger.info(self._format_message(message, extra))
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        self.logger.error(self._format_message(message, extra))
    
    def warning(self, message: str, extra: Dict[str, Any] = None):
        self.logger.warning(self._format_message(message, extra))
    
    def debug(self, message: str, extra: Dict[str, Any] = None):
        self.logger.debug(self._format_message(message, extra))
    
    def critical(self, message: str, extra: Dict[str, Any] = None):
        self.logger.critical(self._format_message(message, extra))

# Create a default logger instance
logger = StructuredLogger(__name__) 