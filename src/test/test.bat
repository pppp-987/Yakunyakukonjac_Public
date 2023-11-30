@REM ファイル保存時に、エンコーディングを"Shift-JIS"にする

@REM 文字コードを"Shift-JIS"に設定
chcp 932

@REM @REM 仮想環境の有効化
cd ../../
call Scripts\activate.bat

@REM 仮想環境のパスを環境変数として保存
set VENV_PATH=%CD%

echo %VENV_PATH%

cd ../

set VENV_PATH=%CD%
echo %VENV_PATH%
pause
@REM set /a num1= cd


@REM 現在のカレントディレクトリの取得
@REM set DIRECTORY_PATH=%~dp0
@REM for %%i in ("%DIRECTORY_PATH:~0,-1%") do set THIS_DIRECTORY=%%~ni

@REM echo %THIS_DIRECTORY%

for %%i in ("%cd%") do echo %%~nxi

msg * TEST