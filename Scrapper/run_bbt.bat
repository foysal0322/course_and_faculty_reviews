@echo off
setlocal EnableExtensions
title NSU Course Scraper - BBT batch
set "HERE=%~dp0"
cd /d "%HERE%.."

echo ============================================================
echo   NSU Faculty Review Scraper  -  BBT batch (20 courses)
echo   Output folder: BBT\
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

echo ============================================================
echo   Notes:
echo     * Chrome opens with its own scraper profile. The FIRST
echo       run imports your existing Facebook session; if that
echo       fails, sign in once in the Chrome window that opens.
echo     * Leave the small "fbsink" tab open while scraping runs.
echo     * 20 courses run one after another. This takes a while.
echo       You can close this window to stop; rerunning resumes.
echo ============================================================
echo.

REM ---- 3. Run ------------------------------------------------------------
python "%HERE%scrape_course.py" ^
    bbt221 bbt230 bbt312 bbt314 bbt315 bbt316 bbt317 bbt318 bbt335 ^
    bbt413 bbt415 bbt416 bbt417 bbt418 bbt419 bbt421 bbt422 bbt423 ^
    bbt424 bbt427 ^
    --outdir BBT
set "RESULT=%ERRORLEVEL%"

echo.
if "%RESULT%"=="0" (
    echo [done] BBT batch finished. Raw data is in BBT\
) else (
    echo [ERROR] Scraper exited with code %RESULT%. See the messages above.
)
echo.
pause
exit /b %RESULT%
