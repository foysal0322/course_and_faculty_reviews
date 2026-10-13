@echo off
setlocal EnableExtensions
title NSU Course Scraper
set "HERE=%~dp0"
cd /d "%HERE%.."

echo ============================================================
echo   NSU Faculty Review Scraper  -  two Facebook groups
echo ============================================================
echo.

REM ---- 1. Python ---------------------------------------------------------
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python was not found on PATH.
    echo         Install it from https://www.python.org/downloads/ and tick
    echo         "Add python.exe to PATH", then run this file again.
    echo.
    pause
    exit /b 1
)

REM ---- 2. Dependencies ---------------------------------------------------
echo [setup] Installing required Python packages...
python -m pip install --disable-pip-version-check --quiet -r "%HERE%requirements.txt"
if errorlevel 1 (
    echo [ERROR] Could not install dependencies. Check your internet connection.
    echo.
    pause
    exit /b 1
)
echo [setup] Dependencies are ready.
echo.

REM ---- 3. Course code ----------------------------------------------------
set "COURSE=%~1"
if "%COURSE%"=="" (
    set /p "COURSE=Enter the course code to scrape (e.g. BBT203): "
)
if "%COURSE%"=="" (
    echo [ERROR] No course code was provided.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Course: %COURSE%
echo.
echo   Notes:
echo     * Chrome opens with its own scraper profile. The FIRST
echo       run asks you to sign in to Facebook once - the login
echo       is remembered for later runs.
echo     * Leave the small "fbsink" tab open while scraping runs.
echo     * Keep scraping one course at a time.
echo ============================================================
echo.

REM ---- 4. Run ------------------------------------------------------------
set "EXTRA=%2 %3 %4 %5 %6 %7 %8 %9"
python "%HERE%scrape_course.py" "%COURSE%" %EXTRA%
set "RESULT=%ERRORLEVEL%"

echo.
if "%RESULT%"=="0" (
    echo [done] Scraping finished. Raw data is in raw\q_%COURSE%.json
) else (
    echo [ERROR] Scraper exited with code %RESULT%. See the messages above.
)
echo.
pause
exit /b %RESULT%
