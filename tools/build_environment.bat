@REM AWSの設定
@REM aws configure

@REM 仮想環境作成
@REM cd Desktop
python -m venv venv_YakunyakuKonjac
cd venv_YakunyakuKonjac
call Scripts\activate.bat

@REM パッケージインストール

pip install PySimpleGUI
pip install pyautogui
pip install opencv-python
pip install awscli
pip install boto3
pip install easyocr
pip install deep-translator
pip install keyboard
pip install black

@REM パッケージ一覧出力ファイルの作成
pip freeze > requirements.txt

@REM gitからクローン
git clone https://github.com/pppp-987/YakunyakuKonjac_Public.git


@REM ディレクトリ構成ファイルの作成
@REM tree /f > directory_tree.txt

@REM VScodeで開く
@REM インタプリタを .\Scripts\python.exeに設定

pause