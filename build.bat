@echo off
echo Building MiniC Compiler...

REM Check if required tools are installed
where gcc >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: gcc not found. Please install MinGW-w64.
    exit /b 1
)

where win_flex >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: win_flex not found. Please install WinFlexBison.
    exit /b 1
)

where win_bison >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: win_bison not found. Please install WinFlexBison.
    exit /b 1
)

REM Build the compiler
cd src\icg

REM Generate lexer
echo Generating lexer...
win_flex -t scanner.l > lex.yy.c
if %errorlevel% neq 0 (
    echo Error: Failed to generate lexer.
    exit /b 1
)

REM Generate parser
echo Generating parser...
win_bison -d minic.y
if %errorlevel% neq 0 (
    echo Error: Failed to generate parser.
    exit /b 1
)

REM Compile the compiler
echo Compiling compiler...
gcc -o minic lex.yy.c minic.tab.c parser.c icg.c table.c -lfl -ly -w
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

REM Verify WinFlexBison installation
win_flex --version
win_bison --version 