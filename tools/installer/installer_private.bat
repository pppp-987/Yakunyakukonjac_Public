@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �R�}���h��\�����Ȃ�
@REM @echo off

@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

@REM ���z���쐬
py -3.8 -m venv venv_YakunyakuKonjac
cd venv_YakunyakuKonjac
call Scripts\activate.bat

@REM �p�b�P�[�W�C���X�g�[�� �^�C���A�E�g��100�b�ɕύX

@REM AWS�֘A
pip --default-timeout=100 install awscli
pip --default-timeout=100 install boto3
@REM OCR�֘A
pip --default-timeout=100 install easyocr
@REM �|��֘A
pip --default-timeout=100 install deep-translator
@REM GUI�֘A
pip --default-timeout=100 install keyboard
pip --default-timeout=100 install pyautogui
pip --default-timeout=100 install PySimpleGUI

@REM �p�b�P�[�W�ꗗ�o�̓t�@�C���̍쐬
pip freeze > requirements.txt

@REM git����N���[��
git clone https://github.com/pppp-987/Yakunyakukonjac_Public.git

@REM �v���W�F�N�g�t�@�C���Ɉړ�
cd Yakunyakukonjac_Public

@REM �u�����`�ύX
git checkout environment

@REM �V���[�g�J�b�g�쐬 VBScript�g�p

@REM �V���[�g�J�b�g�̃����N��p�X
set ShortcutPath="%~dp0\YakunyakuKonjac.lnk"

@REM �V���[�g�J�b�g�̕ۑ���p�X
set TargetPath="%cd%\tools\app.bat"

@REM �V���[�g�J�b�g�̃A�C�R���̃p�X
set ShortcutIconPath="%cd%\static\icon\app.ico"

@REM ��ƃt�H���_�̃p�X
set WorkingDirectoryPath="%cd%\tools"

@REM �ꎞ�I��VBScript�t�@�C���̍쐬
copy nul CreateShortcut.vbs

@REM WScript.Shell�I�u�W�F�N�g�̍쐬
echo Set WScriptShell = WScript.CreateObject("WScript.Shell") >> CreateShortcut.vbs

@REM �V���[�g�J�b�g�̍쐬
echo Set Shortcut = WScriptShell.CreateShortcut(%ShortcutPath%) >> CreateShortcut.vbs

@REM �V���[�g�J�b�g�̃����N��p�X�̐ݒ�
echo Shortcut.TargetPath = %TargetPath% >> CreateShortcut.vbs

@REM ��ƃt�H���_�̐ݒ�
echo Shortcut.WorkingDirectory = %WorkingDirectoryPath% >> CreateShortcut.vbs

@REM �V���[�g�J�b�g�A�C�R���̐ݒ�
echo Shortcut.IconLocation = %ShortcutIconPath% >> CreateShortcut.vbs

@REM �V���[�g�J�b�g��ۑ�
echo Shortcut.Save >> CreateShortcut.vbs

@REM VBS�t�@�C�������s���ăV���[�g�J�b�g���쐬
cscript CreateShortcut.vbs

@REM �ꎞ�I�ɍ쐬����VBS�t�@�C�����폜
del CreateShortcut.vbs

msg * �C���X�g�[�����������܂���