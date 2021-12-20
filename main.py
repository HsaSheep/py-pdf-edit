# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# --- Imports ---
from natsort import natsorted
import PyPDF2
import glob
import os

# --- Parameter ---
INFO_VERSION = "0.2"

FILE_PDF_SPLIT_FOLDER = 'split'  # 分割で使うフォルダ名
FILE_PDF_MERGE_FOLDER = 'merge'  # 結合で使うフォルダ名


# PDFファイルを入れるフォルダを作成
def folder_check_make(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def list_natsort(list_var):
    sorted_list = natsorted(list_var)
    return sorted_list


def list_to_text(list_var):
    text = '\n'.join(repr(e) for e in list_var)
    text = text.replace('\'', '')
    text = text.replace(',', '')
    return text


# フォルダ内のPDFファイルのリストを表示
def file_list_folder(p_folder):
    file_list = glob.glob(os.path.join(p_folder, '*.pdf'))
    f_list = list_natsort(file_list)
    # print(file_list)
    if len(f_list) > 0:
        for i in range(len(f_list)):
            file_n = f_list[i]
            print('{0} : {1}'.format(i+1, file_n))
    else:
        print("Not Found PDF File.")


# PDFファイルを回転して保存
def pdf_roll(p_file, p_angle, output_pdf):
    file = PyPDF2.PdfFileReader(open(p_file, 'rb'))
    file_output = PyPDF2.PdfFileWriter()
    for page_num in range(file.numPages):
        page = file.getPage(page_num)
        page.rotateClockwise(p_angle)
        file_output.addPage(page)
    with open(output_pdf, 'wb') as f:
        file_output.write(f)


# PDFファイルをページごとに分割して保存
def pdf_split(p_file, output_folder):
    filename = os.path.basename(p_file)[:-4]
    file = PyPDF2.PdfFileReader(open(p_file, 'rb'))
    for page_num in range(file.numPages):
        page = file.getPage(page_num)
        file_output = PyPDF2.PdfFileWriter()
        file_output.addPage(page)
        with open(os.path.join(output_folder, filename + "_p" + str(page_num+1) + ".pdf"), 'wb') as f:
            file_output.write(f)


# PDFファイルを結合して保存
def pdf_merge(f_list, output_pdf):
    file_output = PyPDF2.PdfFileMerger()
    for file in f_list:
        file_output.append(file)
    file_output.write(output_pdf)
    file_output.close()


# PDFにページ番号を追加
# --- TODO ---


# --- MAIN ---
if __name__ == '__main__':
    print("--- Version: "+INFO_VERSION+" ---")

    mode = '0'

    folder_check_make(FILE_PDF_MERGE_FOLDER)
    folder_check_make(FILE_PDF_SPLIT_FOLDER)

    while True:
        print()
        print("---------------------------")
        print("Mode Select(Type and Enter)")
        print("L:List R:Roll S:Split M:Merge E:Exit")
        mode = input()
        mode_val = mode[0]

        if mode_val == 'L' or mode_val == 'l':
            print("---List  Mode---")
            print("-- Folder: "+"[root]"+" --")
            file_list_folder(".")
            print("-- Folder: "+FILE_PDF_SPLIT_FOLDER+" --")
            file_list_folder(FILE_PDF_SPLIT_FOLDER)
            print("-- Folder: "+FILE_PDF_MERGE_FOLDER+" --")
            file_list_folder(FILE_PDF_MERGE_FOLDER)

        elif mode_val == 'R' or mode_val == 'r':
            print("---Roll  Mode---")
            print("Please Type [Input FileName] and Enter.")
            roll_file = input()
            print("Type Roll Angle Value( <270|180|90> ) and Enter.")
            roll_ang = input()
            if roll_ang.isdecimal():
                roll_ang = int(roll_ang)
                pdf_roll(roll_file+".pdf", roll_ang, roll_file + "_r" + str(roll_ang) + ".pdf")
            else:
                print("Please Type Decimal.")

        elif mode_val == 'S' or mode_val == 's':
            print("---Split Mode---")
            print("Please Type [Input FileName] and Enter.")
            split_file = input()
            pdf_split(split_file + ".pdf", FILE_PDF_SPLIT_FOLDER)
            print("Output PDFs in ["+FILE_PDF_SPLIT_FOLDER+"] folder.")

        elif mode_val == 'M' or mode_val == 'm':
            print("---Merge Mode---")
            print("Put the PDFs in the ["+FILE_PDF_MERGE_FOLDER+"] folder.")
            print("Please Type [Output FileName] and Enter.")
            merge_file = input()
            file_list = glob.glob(os.path.join(FILE_PDF_MERGE_FOLDER, '*.pdf'))
            f_list = list_natsort(file_list)
            pdf_merge(f_list, merge_file + ".pdf",)

        elif mode_val == 'E' or mode_val == 'e':
            print("---Exit  Mode---")
            break

        else:
            print("----------------")

    # ①PDFファイルを回転して保存
    # pdf_roll(FILE_PDF, 90)

    # ②PDFファイルをページごとに分割して保存
    # pdf_split(FILE_PDF, FILE_PDF_FOLDER)

    # ③フォルダ内のPDFファイルを結合して保存
    # pdf_merge(FILE_PDF, FILE_PDF_FOLDER)

