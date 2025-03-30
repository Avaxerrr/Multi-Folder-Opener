# folder_opening_manager.py

from PySide6.QtCore import QTimer
from core.folder_operations import FolderOpeningThread
import logging


class FolderOpeningManager:
    def __init__(self, parent=None, logger=None):
        self.parent = parent
        self.logger = logger
        self.folder_thread = None
        self.progress_bar = None
        self.execute_button = None
        self.folders = []
        self.sleep_timers = {}
        self.auto_close = False
        self.auto_close_delay = 0

    def set_ui_components(self, progress_bar, execute_button, cancel_button):
        """Set UI components that will be updated during folder opening"""
        self.progress_bar = progress_bar
        self.execute_button = execute_button
        self.cancel_button = cancel_button

    def set_config(self, folders, sleep_timers, auto_close, auto_close_delay):
        """Set configuration parameters for folder opening"""
        self.folders = folders
        self.sleep_timers = sleep_timers
        self.auto_close = auto_close
        self.auto_close_delay = auto_close_delay

    def log(self, message, level=logging.INFO):
        """Log a message using the logger if available"""
        if self.logger:
            if level == logging.INFO:
                self.logger.info(message)
            elif level == logging.WARNING:
                self.logger.warning(message)
            elif level == logging.ERROR:
                self.logger.error(message)

    def execute_folder_opening(self):
        """Start the folder opening process"""
        if self.folder_thread and self.folder_thread.isRunning():
            self.log("Folder opening process is already running.")
            return

        if not self.folders:
            self.log("No folders configured. Please add folders in the configurator.", logging.WARNING)
            return

        if self.execute_button:
            self.execute_button.setEnabled(False)

        if self.cancel_button:
            self.cancel_button.setEnabled(True)  # Enable cancel button when process starts

        if self.progress_bar:
            self.progress_bar.setValue(0)

        if self.logger:
            self.logger.clear_log_widget()

        self.log("Starting folder opening process...")

        self.folder_thread = FolderOpeningThread(self.folders, self.sleep_timers)
        self.folder_thread.log_signal.connect(self._on_log)
        self.folder_thread.progress_signal.connect(self.update_progress)
        self.folder_thread.finished_signal.connect(self.on_folder_opening_finished)
        self.folder_thread.start()

    def on_folder_opening_finished(self, success, message):
        """Handle completion of folder opening process"""
        if self.execute_button:
            self.execute_button.setEnabled(True)

        if self.cancel_button:
            self.cancel_button.setEnabled(False)  # Disable cancel button when process finishes

        if success:
            self.log("Folder opening process completed successfully.")
            if self.auto_close:
                delay_ms = int(self.auto_close_delay * 1000)
                self.log(f"Auto-close enabled. Closing application in {self.auto_close_delay} seconds...")
                QTimer.singleShot(delay_ms, self._auto_close)
        else:
            self.log(f"Folder opening process failed: {message}", logging.ERROR)

    def _on_log(self, message):
        """Handle log messages from the folder opening thread"""
        self.log(message)

    def update_progress(self, value):
        """Update the progress bar"""
        if self.progress_bar:
            self.progress_bar.setValue((value + 1) * 100 / len(self.folders))

    def on_folder_opening_finished(self, success, message):
        """Handle completion of folder opening process"""
        self.log("Folder opening process finished, disabling cancel button")
        if self.execute_button:
            self.execute_button.setEnabled(True)

        if self.cancel_button:
            self.cancel_button.setEnabled(False)

        if success:
            self.log("Folder opening process completed successfully.")
            if self.auto_close:
                delay_ms = int(self.auto_close_delay * 1000)
                self.log(f"Auto-close enabled. Closing application in {self.auto_close_delay} seconds...")
                QTimer.singleShot(delay_ms, self._auto_close)
        else:
            self.log(f"Folder opening process failed: {message}", logging.ERROR)

    def _auto_close(self):
        """Close the application (should be connected to the main window's close method)"""
        if self.parent:
            self.parent.close()

    def cancel_folder_opening(self):
        """Cancel the ongoing folder opening process"""
        if self.folder_thread and self.folder_thread.isRunning():
            self.folder_thread.terminate()
            self.folder_thread.wait()
            self.log("Folder opening process cancelled.", logging.WARNING)
            if self.execute_button:
                self.execute_button.setEnabled(True)
            if self.progress_bar:
                self.progress_bar.setValue(0)
            if self.cancel_button:
                self.cancel_button.setEnabled(False)
