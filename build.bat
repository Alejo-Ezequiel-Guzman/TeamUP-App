@echo off
echo Construyendo TeamUP...

pyinstaller --clean --onefile ^
    --windowed ^
    --name TeamUP ^
    --add-data "database;database" ^
    --add-data "pages;pages" ^
    --add-data "components;components" ^
    --add-data "utils;utils" ^
    --hidden-import=flet ^
    --hidden-import=sqlite3 ^
    --hidden-import=PIL ^
    --hidden-import=PIL._imaging ^
    main.py

echo.
echo Build completado! El ejecutable esta en dist/TeamUP.exe
pause