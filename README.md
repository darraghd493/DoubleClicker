# DoubleClicker
This double clicker allows you to customise nearly every aspect of it just to make it bypass.

# How to use

To use this, simply run the executable (or the `cli.py` file if you are running this through Python) and boom! It works. To modify the settings look at `C:\dogesupremacy\DoubleClicker` and look for the `settings.json` file and all the settings will be available to be configured in there.

# How to build

To build this, you will need to install PyInstaller. This can be done with `pip` (apart from Python) by doing `pip install pyinstaller`. Once you have done this simply run `pyinstaller cli.py --name DoubleClicker --icon icon.ico --noconfirm --noconsole --onefile` and you should have compiled the Python application.

## Automation
The automation for building is in testing right now (Windows only). To use this, open your terminal and run `start "build.bat"` or `start "test-build.bat"` depending on the automated building files name.
