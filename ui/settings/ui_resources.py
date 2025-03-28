# ui_resources.py

class UIResources:
    tooltips = {
        "explorer_startup": (
            "Time to wait after launching Windows Explorer before performing any actions.\n"
            "Increase this value if Explorer is slow to start on your system."
        ),
        "new_tab": (
            "Time to wait after opening a new tab (Ctrl+T) before focusing the address bar.\n"
            "Increase this value if Explorer is slow to respond to the new tab command."
        ),
        "address_bar_focus": (
            "Time to wait after focusing the address bar (Ctrl+L) before typing the path.\n"
            "Increase this value if Explorer is slow to focus the address bar."
        ),
        "after_typing": (
            "Time to wait after typing the folder path before pressing Enter.\n"
            "Increase this value if Explorer is slow to process the typed path."
        ),
        "after_enter": (
            "Time to wait after pressing Enter before proceeding to the next folder.\n"
            "Increase this value if Explorer is slow to navigate to the folder."
        ),
        "start_instantly": (
            "If checked, the folder opener will automatically open all folders when launched.\n"
            "This is useful if you want to set up a shortcut to quickly open all your folders."
        ),
        "start_on_boot": (
            "If checked, the folder opener will automatically start when Windows starts."
        ),
        "auto_close": (
            "If checked, the executioner will automatically close after opening all folders."
        ),
        "auto_close_delay": (
            "Delay in seconds before closing the executioner after completing folder opening."
        )
    }
