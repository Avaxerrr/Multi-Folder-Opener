# Streamline Your Windows File Navigation

A powerful Windows productivity tool that opens multiple folders simultaneously in Windows Explorer tabs, saving time and eliminating repetitive navigation tasks. Version 1.1.0

<table>
  <tr>
    <td colspan="2" align="center"><strong>Multi Folder Opener Interfaces</strong></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/4fc7e7f6-e6cd-4387-9f22-6fd8e28e2dac" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/abc4c7eb-f366-46b1-b1bf-51f16841b89c"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/5546758a-f65f-482a-835a-a5db0b5dd329" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/93536ecc-2f9c-45b5-a6af-cfcc09ef2ac4" width="100%"></td>
  </tr>
</table>



## Productivity-Enhancing Features

- **Instant Multi-Folder Access**: Open all your frequently used folders in Windows Explorer tabs with one click
- **Customizable Timing Settings**: Fine-tune delay settings to optimize performance on any system
- **Flexible Folder Management**: Easily add, remove, reorder, and edit your folder paths
- **Workflow Automation**: Configure auto-start to begin folder opening immediately upon launch
- **Efficiency Options**: Enable auto-close to streamline your workflow further
- **Windows Theme Integration**: Seamlessly adapts to your Windows light/dark theme preferences
- **Productivity Shortcuts**: Boost efficiency with keyboard shortcuts (Delete, Ctrl+Z, Ctrl+Y)
- **Advanced Context Menu**: Right-click for quick folder management options
- **Quick Access**: Convenient system tray integration for easy launching

## Quick Start Guide

1. Download the latest release from the [Releases](https://github.com/Avaxerrr/Multi-Folder-Opener/releases) page
2. Extract to any location - no installation required
3. Run `launcher.exe` to begin optimizing your workflow

This portable application works from any location without installation requirements.

## How to Use

### Configurator: Set Up Your Workflow

The intuitive Configurator helps you customize your folder navigation experience:

1. Click "Add Folders" to select your frequently accessed directories
2. Organize folders in your preferred order using drag-and-drop or arrow buttons
3. Optimize performance by adjusting timing settings for your system
4. Enable auto-start and auto-close options for maximum efficiency
5. Save your configuration with a single click

Easily edit paths by double-clicking or using the convenient right-click context menu.

### Launcher: Boost Your Productivity

The streamlined Launcher opens all your folders with minimal effort:

1. Click "Execute Folder Opening" to initiate the process
2. Watch as Windows Explorer opens with all your folders in organized tabs
3. Monitor real-time progress with detailed status updates

**Pro Tip**: For optimal performance, avoid interacting with your computer during the folder opening sequence.

## Important Security Information

Some antivirus programs may flag this application as a false positive - a common occurrence with Python applications compiled into executables. The application is completely safe to use.

For additional peace of mind, you can review the source code or compile it yourself using this Nuitka command:

```
python -m nuitka --standalone --enable-plugin=pyside6 --windows-icon-from-ico=icons/launcher.ico --include-data-dir=icons=icons --follow-imports --lto=yes --windows-console-mode=disable --msvc=latest --output-filename=launcher main_launcher.py
```

These false positives occur due to how antivirus software evaluates executable packers like Nuitka, not because of any actual security risk.

## License

This project is licensed under the MIT License - see the [LICENSE](license.md) file for details.

## Acknowledgments

- Launcher icon created by [3D Color](https://www.flaticon.com/authors/3d/color/) from [Flaticon](https://www.flaticon.com/)
- Arrow icon created by [Creatype](https://www.flaticon.com/authors/creatype) from [Flaticon](https://www.flaticon.com/)
