@echo off
echo ==========================================
echo Building Farm Data Analyzer Documentation
echo Author: Lucas Zabeu
echo ==========================================

echo.
echo Step 1: Cleaning previous documentation...
cd docs
call make.bat clean
cd ..

echo.
echo Step 1.5: Removing old source files...
del /Q docs\source\src.*.rst 2>nul
del /Q docs\source\modules.rst 2>nul

echo.
echo Step 2: Auto-generating module documentation...
sphinx-apidoc -o docs/source src -f --separate --module-first

echo.
echo Step 3: Building HTML documentation...
cd docs
call make.bat html

echo.
echo Step 4: Documentation built successfully!
echo Location: docs/build/html/index.html

echo.
echo Step 5: Opening documentation in browser...
start build/html/index.html

echo.
echo ==========================================
echo Documentation generation complete!
echo ==========================================
pause