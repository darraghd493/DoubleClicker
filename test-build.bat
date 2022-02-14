@echo off
title WasdInfo Compiler
:::
:::   _____                   ___   ___  __  ___  _
:::  |  __ \                 |__ \ / _ \/_ |/ _ \( )
:::  | |  | | ___   __ _  ___   ) | | | || | (_) |/ ___
:::  | |  | |/ _ \ / _` |/ _ \ / /| | | || |> _ <  / __|
:::  | |__| | (_) | (_| |  __// /_| |_| || | (_) | \__ \
:::  |_____/ \___/ \__, |\___|____|\___/_|_|\___/  |___/
:::  |  __ \        __/ | |   | |     / ____| (_)    | |
:::  | |  | | ___  |___/| |__ | | ___| |    | |_  ___| | _____ _ __
:::  | |  | |/ _ \| | | | '_ \| |/ _ \ |    | | |/ __| |/ / _ \ '__|
:::  | |__| | (_) | |_| | |_) | |  __/ |____| | | (__|   <  __/ |
:::  |_____/ \___/ \__,_|_.__/|_|\___|\_____|_|_|\___|_|\_\___|_|
:::
::: Compiler - Build into a single file
:::
for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A:::
echo Starting build
echo.
pyinstaller cli.py --name WasdInfo --icon icon.ico --noconfirm --noconsole --onefile
echo.
echo Finished build
echo.
pause