# dialog_managers.py (new)

from PySide6.QtWidgets import QMessageBox, QDialog
from ui.about_dialog import AboutDialog
from ui.settings.configurator import ConfiguratorDialog


class DialogManager:
    def __init__(self, parent=None, icon=None):
        self.parent = parent
        self.icon = icon

    def set_parent(self, parent):
        """Set or update the parent widget"""
        self.parent = parent

    def set_icon(self, icon):
        """Set or update the application icon"""
        self.icon = icon

    def show_welcome_dialog(self):
        """Show the welcome dialog for first-time users"""
        if not self.parent:
            return

        welcome_box = QMessageBox(self.parent)
        welcome_box.setWindowTitle("Welcome to Multi Folder Opener")
        welcome_box.setIcon(QMessageBox.Information)
        welcome_box.setText(
            "Before you can use it, you need to configure which folders to open. "
            "Please click Open Configurator to set up your folder paths."
        )
        welcome_box.addButton(QMessageBox.Ok)

        if self.icon:
            welcome_box.setWindowIcon(self.icon)

        welcome_box.exec()

    def show_about_dialog(self):
        """Show the about dialog with application information"""
        if not self.parent:
            return

        dialog = AboutDialog(self.parent)
        if self.icon:
            dialog.setWindowIcon(self.icon)
        dialog.exec()

    def open_configurator(self, config_reload_callback=None):
        """Open the configurator dialog and reload config if accepted"""
        if not self.parent:
            return False

        dialog = ConfiguratorDialog(self.parent, callback=config_reload_callback)
        if self.icon:
            dialog.setWindowIcon(self.icon)

        result = dialog.exec()
        return result == QDialog.Accepted

    def open_configurator_and_exit(self, exit_callback=None):
        """Open configurator and exit application afterward"""
        if not self.parent:
            return

        dialog = ConfiguratorDialog(self.parent)
        if self.icon:
            dialog.setWindowIcon(self.icon)

        dialog.exec()

        # Call exit callback if provided
        if exit_callback:
            exit_callback()

    def show_error_dialog(self, title, message):
        """Show an error dialog with the given title and message"""
        if not self.parent:
            return

        error_box = QMessageBox(self.parent)
        error_box.setWindowTitle(title)
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText(message)
        error_box.addButton(QMessageBox.Ok)

        if self.icon:
            error_box.setWindowIcon(self.icon)

        error_box.exec()
