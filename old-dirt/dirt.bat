@echo off
echo Switching folders...
cd /d "C:\xampp\htdocs\dirt"
echo Launching Python...
call "%USERPROFILE%\miniforge3\Scripts\activate.bat" "%USERPROFILE%\miniforge3"
echo running python
python dirt.py
pause
