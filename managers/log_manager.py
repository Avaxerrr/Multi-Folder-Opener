# log_manager.py

import logging
from datetime import datetime
from PySide6.QtWidgets import QTextEdit


class LogManager:
    def __init__(self, log_text_widget=None):
        self.log_text_widget = log_text_widget

        # Configure Python's logging system
        self.logger = logging.getLogger('FolderOpener')
        self.logger.setLevel(logging.INFO)

        # Create file handler for logging to file
        try:
            file_handler = logging.FileHandler('folder_opener.log')
            file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"Failed to initialize file logging: {e}")

    def set_log_widget(self, log_text_widget):
        """Set or update the log text widget"""
        self.log_text_widget = log_text_widget

    def log(self, message, level=logging.INFO):
        """Log a message to both the UI and log file"""
        # Log to file using Python's logging
        if level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.DEBUG:
            self.logger.debug(message)

        # Log to UI if widget is available
        if self.log_text_widget and isinstance(self.log_text_widget, QTextEdit):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {message}"
            self.log_text_widget.append(log_entry)

    def info(self, message):
        """Log an info message"""
        self.log(message, logging.INFO)

    def warning(self, message):
        """Log a warning message"""
        self.log(message, logging.WARNING)

    def error(self, message):
        """Log an error message"""
        self.log(message, logging.ERROR)

    def debug(self, message):
        """Log a debug message"""
        self.log(message, logging.DEBUG)

    def clear_log_widget(self):
        """Clear the log widget if it exists"""
        if self.log_text_widget:
            self.log_text_widget.clear()
