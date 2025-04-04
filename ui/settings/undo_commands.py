from PySide6.QtGui import QUndoCommand
from core.folder_operations import FolderOperations


class DeleteFolderCommand(QUndoCommand):
    def __init__(self, folders_list, folders, indices, description="Delete Folder"):
        super().__init__(description)
        self.folders_list = folders_list
        self.folders = folders
        self.indices = indices
        self.deleted_folders = []

    def redo(self):
        self.deleted_folders = []
        for index in sorted(self.indices, reverse=True):
            if 0 <= index < len(self.folders):
                self.deleted_folders.insert(0, self.folders[index])
                self.folders.pop(index)
        FolderOperations.update_folders_list(self.folders_list, self.folders)

    def undo(self):
        for index, folder in zip(self.indices, self.deleted_folders):
            if 0 <= index <= len(self.folders):
                self.folders.insert(index, folder)
        FolderOperations.update_folders_list(self.folders_list, self.folders)


class AddFolderCommand(QUndoCommand):
    def __init__(self, folders_list, folders, new_folders, description="Add Folder"):
        super().__init__(description)
        self.folders_list = folders_list
        self.folders = folders
        # Store only the new folders that were added
        self.new_folders = list(new_folders)  # Make a copy to avoid reference issues
        self.start_index = len(folders)  # Store the starting index

    def redo(self):
        # Add the new folders to the main list
        for folder in self.new_folders:
            if folder not in self.folders:  # Avoid duplicates
                self.folders.append(folder)
        # Update the UI
        FolderOperations.update_folders_list(self.folders_list, self.folders)

    def undo(self):
        # Remove only the folders we added
        del self.folders[self.start_index:self.start_index + len(self.new_folders)]
        # Update the UI
        FolderOperations.update_folders_list(self.folders_list, self.folders)


class MoveFolderCommand(QUndoCommand):
    def __init__(self, folders_list, folders, from_index, to_index, description="Move Folder"):
        super().__init__(description)
        self.folders_list = folders_list
        self.folders = folders
        self.from_index = from_index
        self.to_index = to_index

    def redo(self):
        if 0 <= self.from_index < len(self.folders) and 0 <= self.to_index < len(self.folders):
            folder = self.folders.pop(self.from_index)
            self.folders.insert(self.to_index, folder)
            FolderOperations.update_folders_list(self.folders_list, self.folders)

    def undo(self):
        if 0 <= self.from_index < len(self.folders) and 0 <= self.to_index < len(self.folders):
            folder = self.folders.pop(self.to_index)
            self.folders.insert(self.from_index, folder)
            FolderOperations.update_folders_list(self.folders_list, self.folders)


class EditFolderCommand(QUndoCommand):
    def __init__(self, folders_list, folders, index, old_value, new_value, description="Edit Folder"):
        super().__init__(description)
        self.folders_list = folders_list
        self.folders = folders
        self.index = index
        self.old_value = old_value
        self.new_value = new_value

    def redo(self):
        if 0 <= self.index < len(self.folders):
            self.folders[self.index] = self.new_value
            FolderOperations.update_folders_list(self.folders_list, self.folders)

    def undo(self):
        if 0 <= self.index < len(self.folders):
            self.folders[self.index] = self.old_value
            FolderOperations.update_folders_list(self.folders_list, self.folders)
