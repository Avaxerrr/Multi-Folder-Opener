from PySide6.QtWidgets import QFileDialog, QListView, QTreeView, QAbstractItemView


class FolderOperations:
    @staticmethod
    def update_folders_list(folders_list_widget, folders):
        folders_list_widget.clear()
        for folder in folders:
            folders_list_widget.addItem(folder)

    @staticmethod
    def add_folders(parent_widget, folders):
        dialog = QFileDialog(parent_widget)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)

        # Find the list and tree views
        list_view = dialog.findChild(QListView, "listView")
        if list_view:
            list_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
            # Set selection behavior to require Ctrl/Shift for multiple selection
            list_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        tree_view = dialog.findChild(QTreeView)
        if tree_view:
            tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
            # Set selection behavior to require Ctrl/Shift for multiple selection
            tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        if dialog.exec():
            selected_folders = dialog.selectedFiles()
            for folder in selected_folders:
                if folder not in folders:
                    folders.append(folder)
            return True
        return False

    @staticmethod
    def remove_folder(folders_list_widget, folders):
        selected_items = folders_list_widget.selectedItems()
        if not selected_items:
            return False

        for item in selected_items:
            folders.remove(item.text())

        return True

    @staticmethod
    def move_folder_up(folders_list_widget, folders):
        selected_indices = sorted([folders_list_widget.row(item) for item in folders_list_widget.selectedItems()])
        if not selected_indices or selected_indices[0] <= 0:
            return False

        for index in selected_indices:
            if index > 0:  # Ensure we don't try to move the first item up
                folders[index], folders[index - 1] = folders[index - 1], folders[index]

        # Reselect the moved items
        for index in selected_indices:
            if index > 0:
                folders_list_widget.setCurrentRow(index - 1)
                # Select the item
                folders_list_widget.item(index - 1).setSelected(True)

        return True

    @staticmethod
    def move_folder_down(folders_list_widget, folders):
        selected_indices = sorted([folders_list_widget.row(item) for item in folders_list_widget.selectedItems()],
                                  reverse=True)
        if not selected_indices or selected_indices[-1] >= len(folders) - 1:
            return False

        for index in selected_indices:
            if index < len(folders) - 1:  # Ensure we don't try to move the last item down
                folders[index], folders[index + 1] = folders[index + 1], folders[index]

        # Reselect the moved items
        for index in selected_indices:
            if index < len(folders) - 1:
                folders_list_widget.setCurrentRow(index + 1)
                # Select the item
                folders_list_widget.item(index + 1).setSelected(True)

        return True

