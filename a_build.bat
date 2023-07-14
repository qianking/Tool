echo start build...
cd /d %~dp0
cd ..
cd .\Scripts
set PAT="%cd%\activate.bat"
call %PAT% && cd /d %~dp0 && pyinstaller --onefile GEMINI_BURNIN.py && pause
