@echo off
echo [DEBUG 1] Switching folders...
cd /d "C:\xampp\htdocs\dirt-swarm"
echo [DEBUG 2] Launching Python...
call "%USERPROFILE%\anaconda3\Scripts\activate.bat" "%USERPROFILE%\anaconda3"
echo [DEBUG 2] running python
python text.py
pause
