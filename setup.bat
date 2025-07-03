@echo off
echo Installing Entrepreneurship Copilot...
echo.

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Install the package in development mode
echo Installing the package...
pip install -e .

echo.
echo Setup complete! You can now run:
echo   streamlit run ui.py
echo.
pause
