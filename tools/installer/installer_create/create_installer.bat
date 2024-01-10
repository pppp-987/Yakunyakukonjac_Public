@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �R�}���h��\�����Ȃ�
@echo off

@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

@REM �K�v�ȃt�@�C�������݂��Ȃ��ꍇ�A�I������
if not exist "installer_public.py" (
    msg * installer_public.py�����݂��܂���
    exit
) else if not exist "installer_private.py" (
    msg * installer_private.py�����݂��܂���
    exit
) else if not exist "app.ico" (
    msg * app.ico�����݂��܂���
    exit
)

@REM ���ł�exe�t�@�C�������݂���ꍇ�A�I������
if exist "installer_public.exe" (
    msg * installer_public.exe�����݂��܂�
    exit
) else if exist "installer_private.exe" (
    msg * installer_private.exe�����݂��܂�
    exit
)

@REM �R�}���h��\������
@echo on

@REM ���z���쐬
py -3.8 -m venv venv_installer
@REM �J�����g�f�B���N�g�������z���̃��[�g�f�B���N�g���ɂ���
cd venv_installer
@REM ���z���̗L����
call Scripts\activate.bat

@REM �p�b�P�[�W�C���X�g�[��
@REM �O���t�B�J�����[�U�[�C���^�[�t�F�C�X(GUI)���ȒP�ɍ쐬���邽�߂̃c�[��
pip install PySimpleGUI

@REM Python�v���O�������X�^���h�A�����̎��s�\�t�@�C��(exe, dmg, etc.)�ɕϊ����邽�߂̃c�[��
pip install pyinstaller

@REM �p�b�P�[�W�ꗗ�o�̓t�@�C���̍쐬
pip freeze > requirements.txt

@REM src�t�H���_�̍쐬
md src

@REM �C���X�g�[���̃X�N���v�g�̃R�s�[
copy ..\installer_public.py src
copy ..\installer_private.py src

@REM �A�C�R���̃R�s�[
copy ..\app.ico src

@REM exe�t�@�C���̍쐬(1�̃t�@�C���ɂ܂Ƃ߂�A�R���\�[����\���A�L���b�V���̍폜, ���O�w��)
@REM �E�C���X�΍�\�t�g�ɂ���Ă͎��s����
pyinstaller src\installer_public.py --onefile --noconsole --clean --name=installer_public.exe --icon=src\app.ico
pyinstaller src\installer_private.py --onefile --noconsole --clean --name=installer_private.exe --icon=src\app.ico

@REM exe�t�@�C���̃R�s�[
copy dist\installer_public.exe ..\
copy dist\installer_private.exe ..\

@REM ���z�����甲���o��
call Scripts\deactivate.bat

@REM �J�����g�f�B���N�g�������z���̊O�ɂ���
cd ..

@REM ���z���̍폜
RMDIR /S /Q venv_installer

msg * �C���X�g�[���̍쐬���������܂���
pause