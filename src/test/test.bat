@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �����R�[�h��"Shift-JIS"�ɐݒ�
chcp 932

@REM @REM ���z���̗L����
cd ../../
call Scripts\activate.bat

@REM ���z���̃p�X�����ϐ��Ƃ��ĕۑ�
set VENV_PATH=%CD%

echo %VENV_PATH%

cd ../

set VENV_PATH=%CD%
echo %VENV_PATH%
pause
@REM set /a num1= cd


@REM ���݂̃J�����g�f�B���N�g���̎擾
@REM set DIRECTORY_PATH=%~dp0
@REM for %%i in ("%DIRECTORY_PATH:~0,-1%") do set THIS_DIRECTORY=%%~ni

@REM echo %THIS_DIRECTORY%

for %%i in ("%cd%") do echo %%~nxi

msg * TEST