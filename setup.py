# BUILD : python setup.py py2exe

from distutils.core import setup
import py2exe

TARGET_FILE = "main.py"

option = {
    'compressed': False,
    # 圧縮するとファイルサイズは減るが起動時間がかかる

    'optimize': 2,
    # 最適化
    # 通常は2で良い

    'bundle_files': 2,
    # 1 すべてまとめて１つのファイルにする
    # 2 Pythonインタプリタ以外のすべてをまとめる（バンドル）
    # 3（デフォルト）バンドルしない

    # 'includes': ['sip'] #PyQtを使ったときは必要（経験上）
    # 含むモジュールを指定する
    # 自動で取り込んでくれないときに使う

    # 'packages': ['sip']
    # モジュールだけでなくその場所にあるすべてのファイルを含むらしい

    'excludes': ['_gtkagg', '_ssl', '_tkagg', 'bsddb', 'curses', 'doctest', 'email', 'pdb', 'pyreadline', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl', 'Tkconstants', 'Tkinter'],
    # 含まないモジュールを指定する
    # 不要なモジュールを取り込まないことで容量を小さく出来る

    'dll_excludes': ['w9xpopen.exe'],
    # 含まないDLLを指定する

    'dist_dir': './dist'
}

setup(
    options={'py2exe': option},
    console=[
        {'script': TARGET_FILE}
    ],
    # windows=[{
    #     'script': TARGET_FILE,
    #     'icon_resources': [(1, '32x32.ico')],
    #     'name': 'Py PDF Edit',
    #     'version': '0.01',
    #     'description': 'Python PDF Edit.',
    #     'company_name': 'SAra',
    #     'url': 'https://www.hsa12.net/',
    # }],
    zipfile=None
    # default library.zip
    # ./libs/library.zipなど下層にすることも可
)