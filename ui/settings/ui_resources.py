# ui_resources.py

"""Version 1.1"""

class UIResources:
    tooltips = {
        "explorer_startup": (
            "Time to wait after launching Windows Explorer before performing any actions.\n"
            "If folders aren't opening properly, try increasing this value.\n"
            "Default: 1.2 seconds"
        ),
        "new_tab": (
            "Time to wait after opening a new tab before the app tries to type in the address bar.\n"
            "If you notice new tabs aren't being properly prepared, increase this value.\n"
            "Default: 0.5 seconds"
        ),
        "address_bar_focus": (
            "Time to wait after clicking the address bar before typing begins.\n"
            "If you notice the folder path is being typed before the address bar is ready, increase this value.\n"
            "Default: 0.5 seconds"
        ),
        "after_typing": (
            "Time to wait after the folder path is typed before pressing Enter.\n"
            "If Explorer seems to cut off parts of your folder paths, increase this value.\n"
            "Default: 0.5 seconds"
        ),
        "after_enter": (
            "Time to wait after pressing Enter before moving to the next folder.\n"
            "If some folders aren't opening completely before the next one starts, increase this value.\n"
            "Default: 0.5 seconds"
        ),
        "start_instantly": (
            "When checked, folders will open automatically as soon as you launch the app.\n"
            "Useful for creating a desktop shortcut that immediately opens all your folders with one click."
        ),
        "start_on_boot": (
            "When checked, the app will automatically start when you turn on your computer.\n"
            "Helpful if you always need these folders open after starting your PC."
        ),
        "auto_close": (
            "When checked, the app will automatically close after opening all your folders.\n"
            "Useful to keep your taskbar clean after folders are opened."
        ),
        "auto_close_delay": (
            "How long to wait before closing the app after all folders are opened.\n"
            "Gives you time to see that everything opened correctly before the app disappears."
        )
    }

