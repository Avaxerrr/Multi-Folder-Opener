# configurator_handlers.py

import os
import subprocess
from PySide6.QtWidgets import QMessageBox, QMenu
from core.folder_operations import FolderOperations

class ConfiguratorHandlers:
    def __init__(self, dialog):
        self.dialog = dialog

    def add_folders(self):
        if FolderOperations.add_folders(self.dialog, self.dialog.folders):
            FolderOperations.update_folders_list(self.dialog.ui.folders_list, self.dialog.folders)

    def remove_folder(self):
        if FolderOperations.remove_folder(self.dialog.ui.folders_list, self.dialog.folders):
            FolderOperations.update_folders_list(self.dialog.ui.folders_list, self.dialog.folders)

    def move_folder_up(self):
        if FolderOperations.move_folder_up(self.dialog.ui.folders_list, self.dialog.folders):
            FolderOperations.update_folders_list(self.dialog.ui.folders_list, self.dialog.folders)

    def move_folder_down(self):
        if FolderOperations.move_folder_down(self.dialog.ui.folders_list, self.dialog.folders):
            FolderOperations.update_folders_list(self.dialog.ui.folders_list, self.dialog.folders)

    def on_folder_edited(self, item):
        FolderOperations.edit_folder_path(item, self.dialog.ui.folders_list, self.dialog.folders)

    def show_folder_context_menu(self, position):
        item = self.dialog.ui.folders_list.itemAt(position)
        if not item:
            return

        # Context menu and actions
        context_menu = QMenu(self.dialog)
        edit_action = context_menu.addAction("Edit Path")
        explore_action = context_menu.addAction("Open in Explorer")
        remove_action = context_menu.addAction("Remove")

        # Show the menu and get the selected action
        action = context_menu.exec(self.dialog.ui.folders_list.mapToGlobal(position))

        # Handle the selected action
        if action == edit_action:
            self.dialog.ui.folders_list.editItem(item)
        elif action == explore_action:
            try:
                folder_path = item.text()
                if os.path.exists(folder_path):
                    subprocess.Popen(f'explorer "{folder_path}"')
                else:
                    QMessageBox.warning(self.dialog, "Warning", f"The path '{folder_path}' doesn't exist.")
            except Exception as e:
                QMessageBox.critical(self.dialog, "Error", f"Could not open folder: {str(e)}")
        elif action == remove_action:
            index = self.dialog.ui.folders_list.row(item)
            self.dialog.folders.pop(index)
            self.dialog.ui.folders_list.takeItem(index)
