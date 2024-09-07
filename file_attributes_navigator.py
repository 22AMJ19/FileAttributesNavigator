import os
import threading
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import subprocess

FILE_ATTRIBUTES_PATH = 'FileAttributes.txt'
if not os.path.isfile(FILE_ATTRIBUTES_PATH):
    file_creation_handle = open(FILE_ATTRIBUTES_PATH, 'w')
    file_creation_handle.write('')
    file_creation_handle.close()
file_attributes_handle = open(FILE_ATTRIBUTES_PATH, 'r', encoding='UTF-8')
FILE_ATTRIBUTES = file_attributes_handle.read()
file_attributes_handle.close()

SEARCH_FILE_PATH = "SearchFilePath.txt"
if not os.path.isfile(SEARCH_FILE_PATH):
    file_creation_handle = open(SEARCH_FILE_PATH, 'w')
    file_creation_handle.write('')
    file_creation_handle.close()
file_handle = open(SEARCH_FILE_PATH, 'r', encoding='UTF-8')
SEARCH_TARGET_PATHS = file_handle.read()
file_handle.close()

SEARCH_TARGET_ATTRIBUTES_FILE = '.Attributes.txt'

global checkbox_bool_matrix

def search(search_word):
    global checkbox_bool_matrix

    if not SEARCH_TARGET_PATHS:
        messagebox.showerror("エラー", "検索対象が指定されていません。")
        return

    # 検索中のメッセージボックスを表示
    search_window = tkinter.Toplevel()
    search_window.title("検索中")
    ttk.Label(search_window, text="検索中です...しばらくお待ちください。").pack(padx=20, pady=20)
    search_window.geometry("300x100")

    def perform_search():
        search_attribute_matrix = []

        for i, checkbox_bools in enumerate(checkbox_bool_matrix):
            search_attribute_matrix.append(list())

            attributes = FILE_ATTRIBUTES.splitlines()[i].split(',')

            if attributes[1] != "true":
                continue

            for j, checkbox_bool in enumerate(checkbox_bools):
                if checkbox_bool.get():
                    search_attribute_matrix[i].append(attributes[j+2])

        search_results_path_matrix = []

        for search_target_path in SEARCH_TARGET_PATHS.splitlines():
            if os.path.isdir(search_target_path):
                search_results_paths = []
                search_results_path_matrix.append(search_file(search_target_path, search_attribute_matrix, search_results_paths, search_word))
            else:
                messagebox.showerror("エラー", "検索対象が存在しません。")

        result_window = create_result_window()
        path = []

        for search_results_paths in search_results_path_matrix:
            for search_results_path in search_results_paths:
                path.append(search_results_path)
                link = ttk.Label(result_window, text=search_results_path, cursor="hand1")
                link.pack()
                link.bind("<Button-1>", lambda p=search_results_path: subprocess.Popen(["explorer", p], shell=True))

        # 検索完了後にメッセージボックスを閉じる
        search_window.destroy()

    # 検索を別スレッドで実行
    threading.Thread(target=perform_search).start()

def search_file(search_path, search_attribute_matrix, search_results_paths, search_word):
    search_results_paths = search_results_paths

    for entry in os.listdir(search_path):
        if (os.path.isdir(os.path.join(search_path, entry))):
            search_file(os.path.join(search_path, entry),search_attribute_matrix, search_results_paths, search_word)

        if os.path.join(search_path, entry)==(os.path.join(search_path,SEARCH_TARGET_ATTRIBUTES_FILE)):

            file_handle = open(os.path.join(search_path, entry), 'r', encoding='UTF-8')
            search_target_attributes = file_handle.read()
            file_handle.close()

            is_matched = True

            for search_attributes,target_attributes in zip(search_attribute_matrix, search_target_attributes.splitlines()):

                target_attribute = target_attributes.split(",")
                target_attribute = target_attribute[1:]

                for search_attribute in search_attributes:
                    if search_attribute in target_attribute:
                        if (is_matched):
                            is_matched = True
                    if not (search_attribute in target_attribute):
                        is_matched = False
                    if not search_attribute:
                        break 
            
            if is_matched:
                if not search_word:
                    search_results_paths.append(search_path)
                elif search_word in os.path.basename(search_path):
                   search_results_paths.append(search_path)

    return search_results_paths

def create_main_window():
    main_window = tkinter.Tk()
    main_window.title("File Attributes Navigator")
    return main_window

def create_result_window():
    result_window = tkinter.Toplevel()
    result_window.title("検索結果")
    return result_window

def create_search_frame(main_window):
    search_frame = ttk.Frame(main_window, padding=10)
    search_frame.grid(row=0, column=0, sticky=W+E)

    search_word_label = ttk.Label(search_frame, text="検索ワード", padding=(5, 2))
    search_word_label.pack(side=LEFT)

    search_word_entry = ttk.Entry(search_frame, textvariable=StringVar(), width=30)
    search_word_entry.pack(side=LEFT)

    search_button = ttk.Button(search_frame, text="検索", command=lambda:search(search_word_entry.get()))
    search_button.pack(side=LEFT)

def create_checkbox_frame(main_window):
    global checkbox_bool_matrix
    checkbox_bool_matrix=[]

    checkbox_tab_note = ttk.Notebook(main_window)
    checkbox_tab_note.grid(row=1, column=0, sticky=W+E)

    if not FILE_ATTRIBUTES:
        empty_tab = ttk.Frame(checkbox_tab_note)

        checkbox_tab_note.add(empty_tab, text = "空のタブ")
        checkbox_tab_note.grid(row=1, column=0, sticky=W + E + N + S)

        empty_label = ttk.Label(empty_tab, text = "要素が空です")
        empty_label.pack()

        return


    for i,file_attribute in enumerate(FILE_ATTRIBUTES.splitlines()):
        checkbox_bool_matrix.append(list())

        attributes = file_attribute.split(',')
        attribute_title = attributes[0]

        if attributes[1] != "true":
            continue

        attribute_tab = ttk.Frame(checkbox_tab_note)
        checkbox_tab_note.add(attribute_tab, text=attribute_title)

        checkbox_canvas = Canvas(attribute_tab)
        checkbox_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(attribute_tab, orient=VERTICAL, command=checkbox_canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        checkbox_canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ttk.Frame(checkbox_canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: checkbox_canvas.configure(
                scrollregion=checkbox_canvas.bbox("all")
            )
        )

        checkbox_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        for j, attribute in enumerate(attributes[2:]):
            is_checked = BooleanVar()
            checkbox_bool_matrix[i].append(is_checked)
            attribute_checkbox = ttk.Checkbutton(
                scrollable_frame, padding=(10), text=attribute,
                variable=checkbox_bool_matrix[i][j]
            )
            attribute_checkbox.grid(row=j // 3, column=j % 3, sticky=W + E + N + S)

def create_frames(main_window):
    create_search_frame(main_window)
    create_checkbox_frame(main_window)

def main():
    main_window = create_main_window()
    create_frames(main_window)
    main_window.mainloop()

if __name__ == "__main__":
    main()
