import os
import subprocess
from PySide6.QtWidgets import QMessageBox, QMenu, QFileDialog
from core.folder_operations import FolderOperations
from ui.settings.undo_commands import DeleteFolderCommand, AddFolderCommand, MoveFolderCommand, EditFolderCommand


class ConfiguratorHandlers:
    def __init__(self, dialog):
        self.dialog = dialog

    def add_folders(self):
        # Store original folder count
        original_count = len(self.dialog.folders)

        # Use the existing method to add folders
        if FolderOperations.add_folders(self.dialog, self.dialog.folders):
            # Get only the newly added folders
            new_folders = self.dialog.folders[original_count:]

            # Create undo command with only the new folders
            command = AddFolderCommand(
                self.dialog.ui.folders_list,
                self.dialog.folders,
                new_folders,
                f"Add {len(new_folders)} folder(s)"
            )
            self.dialog.undo_stack.push(command)
            return True
        return False

    def remove_folder(self):
        selected_items = self.dialog.ui.folders_list.selectedItems()
        if not selected_items:
            return False

        indices = [self.dialog.ui.folders_list.row(item) for item in selected_items]
        command = DeleteFolderCommand(
            self.dialog.ui.folders_list,
            self.dialog.folders,
            indices,
            f"Delete {len(indices)} folder(s)"
        )
        self.dialog.undo_stack.push(command)
        return True

    def move_folder_up(self):
        selected_items = self.dialog.ui.folders_list.selectedItems()
        if not selected_items or len(selected_items) != 1:
            return False

        current_row = self.dialog.ui.folders_list.row(selected_items[0])
        if current_row > 0:
            command = MoveFolderCommand(
                self.dialog.ui.folders_list,
                self.dialog.folders,
                current_row,
                current_row - 1,
                "Move folder up"
            )
            self.dialog.undo_stack.push(command)
            self.dialog.ui.folders_list.setCurrentRow(current_row - 1)
            return True
        return False

    def move_folder_down(self):
        selected_items = self.dialog.ui.folders_list.selectedItems()
        if not selected_items or len(selected_items) != 1:
            return False

        current_row = self.dialog.ui.folders_list.row(selected_items[0])
        if current_row < self.dialog.ui.folders_list.count() - 1:
            command = MoveFolderCommand(
                self.dialog.ui.folders_list,
                self.dialog.folders,
                current_row,
                current_row + 1,
                "Move folder down"
            )
            self.dialog.undo_stack.push(command)
            self.dialog.ui.folders_list.setCurrentRow(current_row + 1)
            return True
        return False

    def on_folder_edited(self, item):
        row = self.dialog.ui.folders_list.row(item)
        old_value = self.dialog.folders[row]
        new_value = item.text()

        # Keep the original validation logic from FolderOperations
        if old_value != new_value:
            # Check if the path exists
            if not os.path.exists(new_value):
                QMessageBox.warning(
                    self.dialog,
                    "Warning",
                    f"The path '{new_value}' doesn't exist. It will be added, but may not work when opened."
                )

            # Create and execute the undo command
            command = EditFolderCommand(
                self.dialog.ui.folders_list,
                self.dialog.folders,
                row,
                old_value,
                new_value,
                "Edit folder path"
            )
            self.dialog.undo_stack.push(command)

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
            # Use the undo command for consistency
            command = DeleteFolderCommand(
                self.dialog.ui.folders_list,
                self.dialog.folders,
                [index],
                "Delete folder"
            )
            self.dialog.undo_stack.push(command)
