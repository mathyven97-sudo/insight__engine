@echo off
cd backend
if not exist venv (
    echo Virtual environment not found. Please set it up first.
    pause
    exit /b
)
call venv\Scripts\activate
echo Starting Insight Engine Server...
echo Access the site at http://localhost:8000
uvicorn app.main:app --reload
pause
