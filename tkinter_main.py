import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk
import main


EXE_FILE_NAME = "PyPDF-Edit"
EXE_VER = "0.01"
EXE_NAME_VER = EXE_FILE_NAME + " " + EXE_VER

i_dir = os.path.abspath(os.path.dirname(__file__))
select_dir = i_dir

input_files = []
list_mode = ("分解", "結合", "回転")


# モード選択による処理
def mode_update():
    print("text")


# 基礎的な関数
def files_select():  # 複数ファイル選択
    print("GUI:Input Files Select.")
    global select_dir
    f_typ = [("", "*")]
    files = tkinter.filedialog.askopenfilenames(filetypes=f_typ, initialdir=i_dir)
    select_dir = os.path.abspath(os.path.dirname(files[0]))
    print("     Path:   " + str(select_dir))
    print("  File(s): " + str(files))
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
    list_input.configure(state='disable')


def input_files_clear():  # 選択済み入力PDF一覧初期化
    print("VAR:[input_files] Clear.")
    global input_files
    input_files = []
    input_files_list_update()


def in_file_select():  # ボタン　入力ファイル選択
    global input_files
    files = files_select()
    input_files = files
    input_files_list_update()


def b_mw_infile():
    global input_files
    input_files_text = main.list_to_text(input_files)
    tkinter.messagebox.showinfo(EXE_FILE_NAME, input_files_text)


# ウィンドウ設定
root = tkinter.Tk()
root.title(EXE_NAME_VER)  # ウィンドウタイトル
root.geometry("710x750")  # ウィンドウサイズ

# ウィンドウ内設定
# フレーム作成
f1 = tkinter.Frame(root)
f1.rowconfigure(1, weight=1)
f1.columnconfigure(0, weight=1)
f1.grid(sticky=(tkinter.N, tkinter.W, tkinter.S, tkinter.E))

# f1内定義
label_input = tkinter.Label(f1, text='----- 入力PDF -----')
label_input.grid(row=0, column=0, pady=5, sticky=(tkinter.W, tkinter.E))
list_input = tkinter.Text(f1, state='disable', height=15)
list_input.grid(row=1, column=0, padx=20, sticky=(tkinter.N, tkinter.W, tkinter.S, tkinter.E))
list_input_scroll_y = tkinter.Scrollbar(f1, orient=tkinter.VERTICAL, command=list_input.yview)
list_input_scroll_y.grid(row=1, column=1, sticky=(tkinter.N, tkinter.W, tkinter.S))
list_input["yscrollcommand"] = list_input_scroll_y.set
list_input_scroll_x = tkinter.Scrollbar(f1, orient=tkinter.HORIZONTAL, command=list_input.xview)
list_input_scroll_x.grid(row=2, column=0, padx=20, sticky=(tkinter.N, tkinter.W, tkinter.E))
list_input["xscrollcommand"] = list_input_scroll_x.set

btn_clear_infile = tkinter.Button(f1, text='クリア', command=input_files_clear)
btn_clear_infile.grid(row=1, column=2, padx=20, sticky=(tkinter.N, tkinter.W, tkinter.S, tkinter.E))

btn_in_file_select = tkinter.Button(f1, text='選択', command=in_file_select)
btn_in_file_select.grid(row=3, column=0, padx=10, pady=20, sticky=(tkinter.N, tkinter.W, tkinter.S, tkinter.E))

btn_mw_infile = tkinter.Button(f1, text='表示', command=b_mw_infile)
btn_mw_infile.grid(row=3, column=2, sticky=(tkinter.W, tkinter.E))

label_mode = tkinter.Label(f1, text='----- 編集モード選択 -----')
label_mode.grid(row=4, column=0, pady=5, sticky=(tkinter.W, tkinter.E))
combo_mode = tkinter.ttk.Combobox(f1, state='readonly', justify=tkinter.CENTER)
combo_mode["values"] = list_mode
combo_mode.current(0)
combo_mode.bind('<<ComboboxSelected>>', lambda e: mode_update())
combo_mode.grid(row=5, column=0, padx=20, sticky=(tkinter.N, tkinter.W, tkinter.S, tkinter.E))


root.mainloop()  # ウィンドウ表示
