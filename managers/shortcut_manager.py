# shortcut_manager.py

import os
import sys
import winshell
from win32com.client import Dispatch

class ShortcutManager:
    @staticmethod
    def create_start_menu_shortcuts():
        """Create start menu shortcuts for the application"""
        try:
            # Get paths
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                app_path = sys.executable
            else:
                # Running as script
                app_path = os.path.abspath(sys.argv[0])

            start_menu_path = winshell.start_menu()
            programs_path = os.path.join(start_menu_path, "Programs")
            app_folder_path = os.path.join(programs_path, "Multi Folder Opener")

            # Create the application folder if it doesn't exist
            if not os.path.exists(app_folder_path):
                os.makedirs(app_folder_path)

            # Create launcher shortcut
            launcher_shortcut_path = os.path.join(app_folder_path, "Multi Folder Opener.lnk")
            ShortcutManager._create_shortcut(app_path, launcher_shortcut_path)

            # Create configurator shortcut
            config_shortcut_path = os.path.join(app_folder_path, "Multi Folder Opener Configurator.lnk")
            ShortcutManager._create_shortcut(app_path, config_shortcut_path, "--configure")

            return True
        except Exception as e:
            print(f"Error creating start menu shortcuts: {e}")
            return False

    @staticmethod
    def _create_shortcut(target_path, shortcut_path, arguments=None):
        """Helper method to create a shortcut"""
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        if arguments:
            shortcut.Arguments = arguments
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.IconLocation = target_path
        shortcut.save()

    @staticmethod
    def remove_start_menu_shortcuts():
        """Remove start menu shortcuts for the application"""
        try:
            start_menu_path = winshell.start_menu()
            programs_path = os.path.join(start_menu_path, "Programs")
            app_folder_path = os.path.join(programs_path, "Multi Folder Opener")

            if os.path.exists(app_folder_path):
                for file in os.listdir(app_folder_path):
                    file_path = os.path.join(app_folder_path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(app_folder_path)

            return True
        except Exception as e:
            print(f"Error removing start menu shortcuts: {e}")
            return False
