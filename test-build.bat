@echo off
title DoubleClicker Compiler
:::
:::   88PPP. 88888888 888  888 d88PPPo 888        ,d8PPPP doooooo 888         8888 doooooo 888  ,dP   ,d8PPPP   ,dbPPPp
:::  88   8 888  888 888  888 888ooo8 888        d88ooo  d88     888         8888 d88     888o8P'    d88ooo    d88ooP'
:::  88   8 888  888 888  888 888   8 888      ,88'      d88     888         8888 d88     888 Y8L  ,88'      ,88' P'
:::  88oop' 888oo888 888PP888 888PPPP 888PPPPP 88bdPPP   d888888 888PPPPP    8888 d888888 888  `8p 88bdPPP   88  do
:::
::: Compiler - Build into a single file
:::
for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
echo Starting build
echo.
pyinstaller cli.py --name DoubleClicker --icon icon.ico --noconfirm --noconsole --onefile
echo.
echo Finished build
echo.
pause