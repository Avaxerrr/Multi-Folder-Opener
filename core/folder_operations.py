import pyautogui
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QFileDialog, QListView, QTreeView, QAbstractItemView
import subprocess
import time


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


class FolderOpeningThread(QThread):
    log_signal = Signal(str)
    progress_signal = Signal(int)
    finished_signal = Signal(bool, str)

    def __init__(self, folders, sleep_timers):
        super().__init__()
        self.folders = folders
        self.sleep_timers = sleep_timers

    def run(self):
        try:
            if not self.folders:
                self.log_signal.emit("No folders found in config. Please add folders using the configuration tool.")
                self.finished_signal.emit(False, "No folders to open")
                return

            self.log_signal.emit(f"Starting to open {len(self.folders)} folders...")

            self.log_signal.emit("Opening Windows Explorer...")
            subprocess.Popen(r'explorer.exe')
            time.sleep(self.sleep_timers["explorer_startup"])
            self.log_signal.emit(f"Waiting {self.sleep_timers['explorer_startup']}s for Explorer to start")

            for i, folder in enumerate(self.folders):
                self.progress_signal.emit(i)
                self.log_signal.emit(f"Opening folder {i + 1}/{len(self.folders)}: {folder}")

                if i > 0:
                    self.log_signal.emit("Opening new tab (Ctrl+T)")
                    pyautogui.hotkey('ctrl', 't')
                    time.sleep(self.sleep_timers["new_tab"])
                    self.log_signal.emit(f"Waiting {self.sleep_timers['new_tab']}s after new tab")

                self.log_signal.emit("Focusing address bar (Ctrl+L)")
                pyautogui.hotkey('ctrl', 'l')
                time.sleep(self.sleep_timers["address_bar_focus"])
                self.log_signal.emit(f"Waiting {self.sleep_timers['address_bar_focus']}s after focusing address bar")

                self.log_signal.emit(f"Typing path: {folder}")
                pyautogui.write(folder)
                time.sleep(self.sleep_timers["after_typing"])
                self.log_signal.emit(f"Waiting {self.sleep_timers['after_typing']}s after typing")

                self.log_signal.emit("Pressing Enter")
                pyautogui.press('enter')
                time.sleep(self.sleep_timers["after_enter"])
                self.log_signal.emit(f"Waiting {self.sleep_timers['after_enter']}s after pressing Enter")

            self.progress_signal.emit(len(self.folders))
            self.log_signal.emit("All folders opened successfully!")
            self.finished_signal.emit(True, "All folders opened successfully!")

        except Exception as e:
            self.log_signal.emit(f"Error: {str(e)}")
            self.finished_signal.emit(False, str(e))