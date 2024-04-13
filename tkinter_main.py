import os
import io
import sys
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk
from tkinterdnd2 import Tk, DND_FILES
from pdf2image import convert_from_path
# cx的に通らなかった
# import icecream
# from icecream import ic

import main
import values

# pythonの標準出力をUTF-8に
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# python標準出力をテキストファイルに
sys.stdout = open("log.txt", "w")
# sys.stdout = sys.__stdout__
# open("temp.txt", "r").read()

# pdf2image関連初期化
poppler_dir = os.path.join(os.getcwd(), "poppler/bin")
os.environ["PATH"] += os.pathsep + str(poppler_dir)

# グローバル変数初期化
EXE_FILE_NAME = values.EXE_FILE_NAME
EXE_VER = values.EXE_VER
EXE_NAME_VER = values.EXE_NAME_VER

i_dir = os.path.abspath(os.path.dirname(__file__))
select_dir = i_dir

input_files = []
list_mode = ("分解", "結合", "回転", "画像変換")
mode = list_mode[0]

roll_degs = ["90", "180", "270"]
default_deg = 0
roll_deg = roll_degs[default_deg]

image_mode = ["jpg(100dpi)", "jpg(350dpi)", "jpg(450dpi)", "jpg(600dpi)",
              "png(100dpi)", "png(350dpi)", "png(450dpi)", "png(600dpi)",
              "tiff(100dpi)", "tiff(350dpi)", "tiff(450dpi)", "tiff(600dpi)"]
image_type = "jpg"
image_dpi = 600


# 基礎的な関数
def mode_update():  # モード選択による処理
    global mode

    mode = combo_mode_string_var.get()
    print("Mode : " + mode)
    if mode == "回転":
        label_mode_config.configure(text='回転角度（時計周り）')
        combo_mode_config.configure(state='readonly', values=roll_degs)
        combo_mode_config.current(0)

    elif mode == "画像変換":
        label_mode_config.configure(text='保存形式')
        # combo_mode_config.configure(state='readonly', values=image_mode)
        combo_mode_config.configure(state='normal', values=image_mode)
        combo_mode_config.current(0)

    else:
        label_mode_config.configure(text='----------------')
        combo_mode_config.configure(state='disable')

    mode_config_update()


def mode_config_update():  # モード設定選択による処理
    if mode == "回転":
        global roll_deg
        roll_deg = int(combo_mode_config_string_var.get())
        print("Roll Deg. : " + str(roll_deg))
    elif mode == "画像変換":
        global poppler_dir
        if not os.path.isdir(poppler_dir):
            output_label_update("Popplerがありません。"+poppler_dir)
        else:
            global image_type
            global image_dpi
            image_type = combo_mode_config_string_var.get()
            image_dpi = int(image_type[-7:-4])
            image_type = image_type[0:-8]
            print("Image Type: " + image_type)
            print("Image DPI : " + str(image_dpi))


def input_files_select():  # 複数ファイル選択
    print("GUI:Input Files Select.")
    global select_dir
    # f_typ = [("", "*")]
    f_typ = [('処理対象PDF', '*.pdf'), ('', '*')]
    files = tkinter.filedialog.askopenfilenames(filetypes=f_typ, initialdir=select_dir)
    if files:
        select_dir = os.path.abspath(os.path.dirname(files[0]))
        print(files)
        print("     Path:   " + str(select_dir))
    else:
        print("GUI:Input Files Select is Canceled.")
    return files


# 処理対象ファイル
def input_files_list_update():  # 選択済み入力PDF一覧表示更新
    global input_files
    print("GUI:[Input_textbox] Update.")
    text = main.list_to_text(input_files)
    # list_input.delete(0, tkinter.END)
    list_input.configure(state='normal')
    list_input.delete("1.0", tkinter.END)
    list_input.insert(tkinter.END, text)
    list_input.configure(state='disabled')


def input_files_clear():  # 選択済み入力PDF一覧初期化
    print("VAR:[input_files] Clear.")
    global input_files
    input_files = []
    input_files_list_update()


def in_file_select():  # ボタン　入力ファイル選択
    global input_files
    files = input_files_select()
    print(files)
    input_files += files
    input_files_list_update()


def in_file_drop(event):  # windowへのドラックアンドドロップ
    global input_files
    print("Drag&Drop: " + str(event.data))
    files = list(root.tk.splitlist(event.data))
    print(type(files))
    print(files)
    # files_str = str(files).replace(os.sep, '/').replace("\"", "").split(",")
    input_files += files
    print(input_files)
    input_files_list_update()


def b_mw_infile():  # 入力ファイル確認（Message Box) [debug]
    global input_files
    input_files_text = main.list_to_text(input_files)
    if input_files_text == "":
        tkinter.messagebox.showinfo(EXE_FILE_NAME, "No File Selected.")
    else:
        tkinter.messagebox.showinfo(EXE_FILE_NAME, input_files_text)


# ファイル出力関係
def output_file_select():  # 保存先ファイルパス取得
    print("GUI:Output Files Path.")
    global select_dir
    f_type = [('結合PDF', '*.pdf'), ('', '*')]
    save_path = str(tkinter.filedialog.asksaveasfilename(filetypes=f_type, initialdir=select_dir))
    if save_path == "":
        return ""
    while save_path[-4:] == ".pdf":
        print(save_path)
        save_path = save_path[:-4]
    save_path += '.pdf'
    select_dir = os.path.abspath(os.path.dirname(save_path))
    print(save_path)
    print(select_dir)
    return save_path


def output_dir_select():  # 保存先フォルダパス取得
    print("GUI:Output Directory Select.")
    global select_dir
    save_path = tkinter.filedialog.askdirectory(initialdir=select_dir)
    select_dir = save_path
    print(save_path)
    print(select_dir)
    return save_path


def output_label_update(message):
    label_output_info.configure(text=message)


def run_and_save():  # 判定、ファイル出力先指定
    output_modes = ["file", "folder"]
    open_path = ""
    save_path = ""
    output_label_update("出力処理中...")
    # グローバル変数取得
    global mode
    global select_dir
    global input_files
    # 実行前モードチェック
    input_files_num = len(input_files)
    print("Input File Num : " + str(input_files_num))
    print("GUI: Run [" + mode + "]")
    if mode == "分解":
        output_mode = output_modes[1]
        save_path = output_dir_select()
        if save_path != "":
            open_path = save_path
            for file_n in input_files:
                output_label_update("分解保存中... ->File: " + file_n)
                main.pdf_split(file_n, save_path)

    elif mode == "結合":
        output_mode = output_modes[0]
        save_path = output_file_select()
        output_label_update("結合保存中... ※最大10分ほど時間がかかる場合があります。")
        if save_path != "":
            open_path = os.path.dirname(save_path)
            main.pdf_merge(input_files, save_path)

    elif mode == "回転":
        global roll_deg
        roll_deg = int(combo_mode_config_string_var.get())
        print("Roll Deg. : " + str(roll_deg))
        output_mode = output_modes[1]
        save_path = output_dir_select()
        if save_path != "":
            open_path = save_path
            for r_file in input_files:
                file_name = os.path.basename(r_file)[:-4]
                output_label_update("回転中... ->File: " + file_name)
                file_name += "_R" + str(roll_deg) + ".pdf"
                main.pdf_roll(r_file, roll_deg, os.path.join(save_path, file_name))

    elif mode == "画像変換":
        global image_type
        global image_dpi
        image_type = combo_mode_config_string_var.get()
        image_dpi = int(image_type[-7:-4])
        image_type = image_type[0:-8]
        message_str = "ImageSetting: Type... " + image_type + " DPI... " + str(image_dpi)
        print(message_str)
        output_label_update("変換開始中...　※最大10分ほど時間がかかる場合があります。")
        output_mode = output_modes[1]
        save_path = output_dir_select()
        if save_path != "":
            open_path = save_path
            print("GUI: Image Convert")
            output_label_update("出力処理中... [" + message_str + "] 変換開始中...")
            for p_file in input_files:
                print(" -> File: "+p_file)
                pages = convert_from_path(p_file, image_dpi)
                for i, page in enumerate(pages):
                    print("  -> Page: " + str(i+1))
                    output_label_update("出力処理中... [->Page: " + str(i+1) + "/" + str(enumerate(pages)) +
                                        ", ->File: " + p_file + "] 変換開始中...")
                    p_filename = os.path.basename(p_file)[:-4]
                    image_path = os.path.join(save_path, p_filename+"_"+str(i+1))
                    if image_type == "jpg":
                        page.save(image_path+".jpg", "JPEG")
                    elif image_type == "png":
                        page.save(image_path+".png", "PNG")
                    elif image_type == "tiff":
                        pages[0].save(image_path+".tif", "TIFF", compression="tiff_deflate", save_all=True,
                                      append_images=pages[1:])
                        break
            print("GUI: Image Convert Done.")

    if save_path != "":
        os.startfile(open_path)
        output_label_update("完了")
    else:
        output_label_update("キャンセルしました")
    print("GUI: Run DONE.")


# 終了時処理
def window_close():
    # sys.stdout = open("log.txt", "w")
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    # open("temp.txt", "r").read()


# ウィンドウ設定
# root = tkinter.Tk()
root = Tk()
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', in_file_drop)
root.title(EXE_NAME_VER)  # ウィンドウタイトル
root.geometry("780x470")  # ウィンドウサイズ

# tkinter ico設定
root.iconbitmap('inc_dir/icon.ico')

# ウィンドウ内設定
# フレーム作成
f1 = tkinter.Frame(root)
f1.rowconfigure(1, weight=1)
f1.columnconfigure(0, weight=1)
f1.grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)

# f1内定義
label_input = tkinter.Label(f1, text='----- 入力PDF -----')
label_input.grid(row=0, column=0, columnspan=3, pady=5, sticky=tkinter.W+tkinter.E)
list_input = tkinter.Text(f1, state='disabled', wrap='none', height=15)
list_input.grid(row=1, column=0, padx=20, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
list_input_scroll_y = tkinter.Scrollbar(f1, orient=tkinter.VERTICAL, command=list_input.yview)
list_input_scroll_y.grid(row=1, column=1, sticky=tkinter.N+tkinter.W+tkinter.S)
list_input["yscrollcommand"] = list_input_scroll_y.set
list_input_scroll_x = tkinter.Scrollbar(f1, orient=tkinter.HORIZONTAL, command=list_input.xview)
list_input_scroll_x.grid(row=2, column=0, padx=20, sticky=tkinter.N+tkinter.W+tkinter.E)
list_input["xscrollcommand"] = list_input_scroll_x.set

btn_clear_infile = tkinter.Button(f1, text='クリア', command=input_files_clear)
btn_clear_infile.grid(row=1, column=2, padx=20, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)

btn_in_file_select = tkinter.Button(f1, text='選択', command=in_file_select)
btn_in_file_select.grid(row=3, column=0, padx=20, pady=20, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)

btn_mw_infile = tkinter.Button(f1, text='表示', command=b_mw_infile)
btn_mw_infile.grid(row=3, column=2, sticky=tkinter.W+tkinter.E)

label_mode = tkinter.Label(f1, text='----- 編集モード選択 -----')
label_mode.grid(row=4, column=0, columnspan=2, pady=5, sticky=tkinter.W+tkinter.E)

label_mode_config = tkinter.Label(f1, text='----------------')
label_mode_config.grid(row=4, column=2, sticky=tkinter.W+tkinter.E)

combo_mode = tkinter.ttk.Combobox(f1, values=list_mode, state='readonly', justify=tkinter.CENTER)
combo_mode_string_var = tkinter.StringVar()
combo_mode['textvariable'] = combo_mode_string_var
combo_mode.bind('<<ComboboxSelected>>', lambda e: mode_update())
combo_mode.grid(row=5, column=0, padx=20, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
combo_mode.current(0)

combo_mode_config = tkinter.ttk.Combobox(f1, values=["", ""], state='disable', justify=tkinter.CENTER)
combo_mode_config_string_var = tkinter.StringVar()
combo_mode_config['textvariable'] = combo_mode_config_string_var
combo_mode_config.bind('<<ComboboxSelected>>', lambda e: mode_config_update())
combo_mode_config.grid(row=5, column=2, sticky=tkinter.W+tkinter.E)
combo_mode_config.current(default_deg)


btn_save_path = tkinter.Button(f1, text='実行', command=run_and_save)
btn_save_path.grid(row=6, column=0, columnspan=3, padx=20, pady=20, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)

label_output_info = tkinter.Label(f1, text='', fg='#ffffff', bg='#000000')
label_output_info.grid(row=7, column=0, columnspan=3, padx=20, pady=10, sticky=tkinter.W+tkinter.E)

root.mainloop()  # ウィンドウ表示
