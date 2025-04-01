import os
import sys
import winshell
from win32com.client import Dispatch


class ShortcutManager:
    @staticmethod
    def create_desktop_shortcut():
        """Create a desktop shortcut for the application"""
        try:
            # Get paths
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                app_path = sys.executable
            else:
                # Running as script
                app_path = os.path.abspath(sys.argv[0])

            desktop_path = winshell.desktop()
            shortcut_path = os.path.join(desktop_path, "Multi Folder Opener.lnk")

            # Create shortcut
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = app_path
            shortcut.WorkingDirectory = os.path.dirname(app_path)
            shortcut.IconLocation = app_path
            shortcut.save()

            return True
        except Exception as e:
            print(f"Error creating desktop shortcut: {e}")
            return False

    @staticmethod
    def create_start_menu_shortcut():
        """Create a start menu shortcut for the application"""
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
            shortcut_path = os.path.join(programs_path, "Multi Folder Opener.lnk")

            # Create shortcut
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = app_path
            shortcut.WorkingDirectory = os.path.dirname(app_path)
            shortcut.IconLocation = app_path
            shortcut.save()

            return True
        except Exception as e:
            print(f"Error creating start menu shortcut: {e}")
            return False
