cd ../../
call Scripts\activate.bat
pip freeze > requirements.txt
Scripts\python.exe YakunyakuKonjac_Public\src\app.py
pause