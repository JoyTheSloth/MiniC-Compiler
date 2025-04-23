@echo off
echo Building MiniC Compiler without WinFlexBison...

REM Check if gcc is installed
where gcc >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: gcc not found. Please install MinGW-w64.
    exit /b 1
)

REM Check if pre-generated files exist
set ICG_DIR=src\icg
if not exist "%ICG_DIR%\lex.yy.c" (
    echo Error: Pre-generated lexer file lex.yy.c not found.
    echo You need to either:
    echo 1. Install WinFlexBison and run build.bat
    echo 2. Download pre-generated files from the project repository
    exit /b 1
)

if not exist "%ICG_DIR%\minic.tab.c" (
    echo Error: Pre-generated parser file minic.tab.c not found.
    echo You need to either:
    echo 1. Install WinFlexBison and run build.bat
    echo 2. Download pre-generated files from the project repository
    exit /b 1
)

if not exist "%ICG_DIR%\minic.tab.h" (
    echo Error: Pre-generated header file minic.tab.h not found.
    echo You need to either:
    echo 1. Install WinFlexBison and run build.bat
    echo 2. Download pre-generated files from the project repository
    exit /b 1
)

REM Build the compiler
cd %ICG_DIR%

REM Compile the compiler
echo Compiling compiler...
gcc -o minic lex.yy.c minic.tab.c parser.c icg.c table.c -w
if %errorlevel% neq 0 (
    echo Error: Failed to compile the compiler.
    exit /b 1
)

REM Move the compiler to the root directory
move minic ..\..\ >nul

REM Build the interpreter
cd ..\ucode
echo Building interpreter...
g++ -c ucodei.cpp -w
g++ -o ucodei ucodei.o
move ucodei ..\..\ >nul
del ucodei.o

cd ..\..

echo.
echo Build completed successfully!
echo You can now run the web interface with: python frontend\app.py 