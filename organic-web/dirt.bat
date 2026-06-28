@echo off
echo Switching folders...
cd /d "C:\xampp\htdocs\dirt"
echo Launching Python...
call "%USERPROFILE%\anaconda3\Scripts\activate.bat" "%USERPROFILE%\anaconda3"
echo running python
python dirt.py
pause
