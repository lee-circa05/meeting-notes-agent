@echo off
REM Quick test of the Meeting-Notes-to-Actions Agent
cd /d "c:\Users\levis.escame\Desktop\meeting-notes-agent"

echo.
echo ======================================
echo Meeting-Notes-to-Actions Agent Test
echo ======================================
echo.

REM Install dependencies
echo Installing test dependencies...
pip install pytest pytest-cov -q

echo.
echo Running unit tests...
pytest tests/test_agent.py -v --tb=short

echo.
echo Running tests with coverage...
pytest tests/ -v --cov=src --cov-report=term-missing

echo.
echo ======================================
echo Test Summary
echo ======================================
echo.

pause
