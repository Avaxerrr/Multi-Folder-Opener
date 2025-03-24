import os
import json
from PySide6.QtWidgets import QMessageBox


class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path

    def load_config(self, parent_widget=None):
        # Default values
        folders = []
        sleep_timers = {
            "explorer_startup": 1.0,
            "new_tab": 0.3,
            "address_bar_focus": 0.2,
            "after_typing": 0.2,
            "after_enter": 0.3
        }
        start_instantly = False

        # Check if config file exists, if not create a default one
        if not os.path.exists(self.config_path):
            default_config = {
                "folders": [
                    "C:\\Users\\Work\\Desktop",
                    "Add you folder locations here..."
                ],
                "sleep_timers": sleep_timers,
                "start_instantly": False
            }

            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                folders = default_config['folders']
                sleep_timers = default_config['sleep_timers']
                start_instantly = default_config['start_instantly']
            except Exception as e:
                if parent_widget:
                    QMessageBox.critical(parent_widget, "Error", f"Error creating config file: {e}")
                return folders, sleep_timers, start_instantly

        # Read config from file
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                folders = config.get('folders', [])

                # Load sleep timers if they exist, otherwise use defaults
                if 'sleep_timers' in config:
                    sleep_timers = config['sleep_timers']
                else:
                    # Add sleep_timers to existing config
                    config['sleep_timers'] = sleep_timers
                    with open(self.config_path, 'w') as f:
                        json.dump(config, f, indent=2)

                # Load start_instantly setting if it exists
                start_instantly = config.get('start_instantly', False)

        except Exception as e:
            if parent_widget:
                QMessageBox.critical(parent_widget, "Error", f"Error loading config: {e}")

        return folders, sleep_timers, start_instantly

    def save_config(self, folders, sleep_timers, start_instantly, parent_widget=None):
        try:
            config = {
                "folders": folders,
                "sleep_timers": sleep_timers,
                "start_instantly": start_instantly
            }

            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)

            if parent_widget:
                QMessageBox.information(parent_widget, "Success", "Configuration saved successfully!")
            return True
        except Exception as e:
            if parent_widget:
                QMessageBox.critical(parent_widget, "Error", f"Error saving config: {e}")
            return False
