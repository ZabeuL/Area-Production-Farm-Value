@echo off
echo ==========================================
echo Building Farm Data Analyzer Documentation
echo Author: Lucas Zabeu
echo ==========================================

echo.
echo Step 1: Auto-generating module documentation...
sphinx-apidoc -o docs/source src -f

echo.
echo Step 2: Building HTML documentation...
cd docs
make html

echo.
echo Step 3: Documentation built successfully!
echo Location: docs/build/html/index.html

echo.
echo Step 4: Opening documentation in browser...
start build/html/index.html

echo.
echo ==========================================
echo Documentation generation complete!
echo ==========================================
pause