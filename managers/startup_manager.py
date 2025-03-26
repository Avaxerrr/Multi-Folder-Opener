#  startup_manager.py

import os
import sys
import pythoncom
import win32com.client
from PySide6.QtWidgets import QMessageBox


class StartupManager:
    """Manages Windows startup shortcuts for the application"""

    @staticmethod
    def get_startup_folder_path():
        """Get the path to the Windows Startup folder"""
        return os.path.join(os.environ["APPDATA"],
                            r"Microsoft\Windows\Start Menu\Programs\Startup")

    @staticmethod
    def get_shortcut_path():
        """Get the full path to the startup shortcut"""
        startup_folder = StartupManager.get_startup_folder_path()
        return os.path.join(startup_folder, "Folder Opener.lnk")

    @staticmethod
    def check_startup_shortcut_exists():
        """Check if the startup shortcut exists"""
        shortcut_path = StartupManager.get_shortcut_path()
        return os.path.exists(shortcut_path)

    @staticmethod
    def create_startup_shortcut(application_path, parent_widget=None):
        """Create a shortcut in the Windows Startup folder"""
        try:
            # Initialize COM
            pythoncom.CoInitialize()

            # Get the path to the executable or script
            if getattr(sys, 'frozen', False):
                # Running as executable
                target_path = os.path.join(application_path, "launcher.exe") # need to change for the final executable name
            else:
                # Running as script
                target_path = os.path.join(application_path, "main_launcher.py")
                # For scripts, we need to use the Python interpreter
                if not os.path.exists(target_path):
                    if parent_widget:
                        QMessageBox.warning(parent_widget, "Warning",
                                            "Could not find the launcher. Startup on boot may not work.")
                    return False

            # Create shortcut object
            startup_folder = StartupManager.get_startup_folder_path()
            shortcut_path = os.path.join(startup_folder, "Folder Opener.lnk")

            # Create the shortcut
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)

            if getattr(sys, 'frozen', False):
                # For executable
                shortcut.Targetpath = target_path
                shortcut.WorkingDirectory = application_path
            else:
                # For script
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = f'"{target_path}"'
                shortcut.WorkingDirectory = application_path

            shortcut.IconLocation = os.path.join(application_path, 'icons', 'launcher.ico')
            shortcut.Description = "Folder Opener Launcher"
            shortcut.save()

            return True
        except Exception as e:
            if parent_widget:
                QMessageBox.critical(parent_widget, "Error", f"Could not create startup shortcut: {str(e)}")
            return False
        finally:
            pythoncom.CoUninitialize()

    @staticmethod
    def remove_startup_shortcut(parent_widget=None):
        """Remove the shortcut from the Windows Startup folder"""
        try:
            shortcut_path = StartupManager.get_shortcut_path()
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
            return True
        except Exception as e:
            if parent_widget:
                QMessageBox.critical(parent_widget, "Error", f"Could not remove startup shortcut: {str(e)}")
            return False
