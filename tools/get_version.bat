@REM �t�@�C���ۑ����ɁA�G���R�[�f�B���O��"Shift-JIS"�ɂ���

@REM �R�}���h��\�����Ȃ�
@echo off

@REM �����R�[�h��"Shift-JIS"�ɐݒ� ���b�Z�[�W�͔�\��
chcp 932 >nul

@REM ���z�����L���łȂ��Ȃ�
if not defined VIRTUAL_ENV (
    @REM ���z���̃��[�g�f�B���N�g���ֈړ�
    cd ../..
    @REM ���z���̗L����
    call Scripts\activate.bat
)


@REM �v���W�F�N�g�̃��[�g�f�B���N�g���ֈړ�
cd Yakunyakukonjac_Public

@REM �ŐV�̃R�~�b�g�̒Z�k�n�b�V���ƃR�~�b�g���b�Z�[�W�̃^�C�g���̏o��
git log --pretty=format:"%%h %%s" -n 1

pause