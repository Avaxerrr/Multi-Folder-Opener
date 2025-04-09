# command_line_handler.py

"""Version 1.1"""

import sys

class CommandLineHandler:
    def __init__(self, args=None):
        """Initialize with command line arguments or use sys.argv if not provided"""
        self.args = args if args is not None else sys.argv[1:]
        self.parsed_args = self._parse_args()

    def _parse_args(self):
        """Parse command line arguments into a dictionary"""
        parsed = {
            'configure': False,
            'help': False,
            'version': False,
            # Add more options as needed
        }

        for arg in self.args:
            if arg in ['--configure', '-c']:
                parsed['configure'] = True
            elif arg in ['--help', '-h']:
                parsed['help'] = True
            elif arg in ['--version', '-v']:
                parsed['version'] = True
            # Add more argument parsing as needed

        return parsed

    def is_configure_mode(self):
        """Check if the application should run in configurator mode"""
        return self.parsed_args.get('configure', False)

    def is_help_requested(self):
        """Check if help information was requested"""
        return self.parsed_args.get('help', False)

    def is_version_requested(self):
        """Check if version information was requested"""
        return self.parsed_args.get('version', False)

    def print_help(self):
        """Print help information to console"""
        help_text = """
Multi Folder Opener - Help
--------------------------
Usage: folder_opener [options]

Options:
  -c, --configure    Open the configurator dialog
  -h, --help         Display this help information
  -v, --version      Display version information
        """
        print(help_text)

    def print_version(self, version="1.0.0"):
        """Print version information to console"""
        print(f"Multi Folder Opener v{version}")
