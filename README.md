# Multi Folder Opener

A Windows utility that streamlines your workflow by opening multiple folders simultaneously in Windows Explorer tabs. Version 1.1.0

| | |
|---------|---------|
| <img src="https://github.com/user-attachments/assets/4fc7e7f6-e6cd-4387-9f22-6fd8e28e2dac" width="100%"> | <img src="https://github.com/user-attachments/assets/abc4c7eb-f366-46b1-b1bf-51f16841b89c"> |
|<img src="https://github.com/user-attachments/assets/5546758a-f65f-482a-835a-a5db0b5dd329" width="100%">|<img src="https://github.com/user-attachments/assets/93536ecc-2f9c-45b5-a6af-cfcc09ef2ac4" width="100%">|


## Features

- **Open Multiple Folders**: Launch multiple folders in Windows Explorer tabs with a single click
- **Configurable Delays**: Adjust timing settings to accommodate different system speeds
- **Editable Folder Paths**: Easily add, remove, and reorder folders
- **Auto-Start Option**: Configure the application to start opening folders immediately upon launch
- **Auto-Close Option**: Automatically close the launcher after folders are opened
- **Theme Support**: Automatically adapts to Windows light/dark theme settings
- **Keyboard Shortcuts**: Use Delete to remove folders, Ctrl+Z to undo actions and Ctrl+Y to redo
- **Right-Click Context Menu**: Manage folders with a convenient context menu
- **System Tray Integration**: Easy access from the system tray

## Installation

1. Download the latest release from the [Releases](https://github.com/Avaxerrr/Multi-Folder-Opener/releases) page
2. Extract the zip file to your preferred location
3. Run `launcher.exe` to start the application

No installation is required - the application is portable and can be run from any location.

## Usage

### Configurator

The Configurator allows you to set up your folder paths and application settings:

1. Click "Add Folders" to select folders you want to open
2. Arrange folders in the desired order using the Up/Down buttons or drag-and-drop
3. Adjust delay settings based on your system performance
4. Toggle auto-start and auto-close options as needed
5. Click "Save" to store your settings

You can edit folder paths directly by double-clicking on them in the list or using the right-click context menu.

### Launcher

The Launcher opens your configured folders in Windows Explorer:

1. Click "Execute Folder Opening" to start the process
2. The application will open Windows Explorer and navigate to each folder
3. Progress is displayed in real-time with detailed logging

**Note**: Do not interact with your computer during the folder opening process to prevent interruptions.

You're absolutely right. I've revised the section to make more logical sense:

## Important Note

Some antivirus programs may flag this application as a false positive. This is a common occurrence for Python applications packaged into executables. Rest assured, the application is completely safe to use.

If you have any concerns about security, you can review the source code or download it and compile it yourself using the following Nuitka command:

```
python -m nuitka --standalone(you can use --onefile) --enable-plugin=pyside6 --windows-icon-from-ico=icons/launcher.ico --include-data-dir=icons=icons --follow-imports --lto=yes --windows-console-mode=disable --msvc=latest --output-filename=launcher main_launcher.py
```

False positives occur because antivirus software can be suspicious of executable packers like those used by Nuitka, but this doesn't indicate any actual security risk.

## License

This project is licensed under the MIT License - see the [LICENSE](license.md) file for details.

## Acknowledgments

- Launcher icon created by [3D Color](https://www.flaticon.com/authors/3d/color/) from [Flaticon](https://www.flaticon.com/)
- Arrow icon created by [Creatype](https://www.flaticon.com/authors/creatype) from [Flaticon](https://www.flaticon.com/)
