import os
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

FILE_ATTRIBUTES_PATH = 'FileAttributes.txt'
if not os.path.isfile(FILE_ATTRIBUTES_PATH):
    file_creation_handle = open(FILE_ATTRIBUTES_PATH, 'w')
    file_creation_handle.write('')
    file_creation_handle.close()

SEARCH_FILE_PATH = "SearchFilePath.txt"
if not os.path.isfile(SEARCH_FILE_PATH):
    file_creation_handle = open(SEARCH_FILE_PATH, 'w')
    file_creation_handle.write('')
    file_creation_handle.close()
file_handle = open(SEARCH_FILE_PATH, 'r', encoding='UTF-8')
SEARCH_TARGET_PATHS = file_handle.read()
file_handle.close()

SEARCH_TARGET_ATTRIBUTES_FILE = '.Attributes.txt'

global checkbox_bool_matrix, reference_var, file_attributes

def load_file_attributes():
    global file_attributes
    file_attributes_handle = open(FILE_ATTRIBUTES_PATH, 'r', encoding='UTF-8')
    file_attributes = file_attributes_handle.read()
    file_attributes_handle.close()

def update_attributes(attribute_title, attribute,main_window):
    global file_attributes
    if not attribute:
        return
    attribute_data_list = []
    for file_attributes_line in file_attributes.splitlines():
        split_file_attributes_line = file_attributes_line.split(",")
        if attribute_title == split_file_attributes_line[0]:
            for split_file_attribute in split_file_attributes_line[2:]:
                if split_file_attribute == attribute:
                    return
            attribute_data_list.append(file_attributes_line + "," + attribute)
            continue
        attribute_data_list.append(file_attributes_line)
    update_file_attributes(attribute_data_list,main_window)

def append_to_file_attributes(attribute_data, main_window):
    with open(FILE_ATTRIBUTES_PATH, 'a', encoding='UTF-8') as file:
        file.write('\n' + attribute_data)
    update_checkbox_frame(main_window)

def update_file_attributes(attribute_data_list,main_window):
    with open(FILE_ATTRIBUTES_PATH, 'w', encoding='UTF-8') as file:
        for attribute_data in attribute_data_list:
            file.write(attribute_data + '\n')
    update_checkbox_frame(main_window)

def update_checkbox_frame(main_window):
    load_file_attributes()

    for widget in main_window.winfo_children():
        widget.destroy()
    
    create_frames(main_window)

def browse_directory_dialog():
    global reference_var
    
    selected_directory = filedialog.askdirectory(initialdir = os.path.abspath(os.path.dirname(__file__)))
    reference_var.set(selected_directory)

def add_attribute_tab(attribute_identifier,is_attribute_tab_visibles, main_window):
    global file_attributes
    if not attribute_identifier:
        return
    
    for file_attributes_line in file_attributes.splitlines():
        split_file_attributes_line = file_attributes_line.split(",")
        if attribute_identifier == split_file_attributes_line[0]:
            return
    
    attribute_data = attribute_identifier + "," 

    if is_attribute_tab_visibles:
        attribute_data = attribute_data + "true"
    else:
        attribute_data = attribute_data + "false"

    append_to_file_attributes(attribute_data, main_window)

def update_tab_visibility_settings(attribute_identifier,is_tab_visible):
    global file_attributes
    attribute_data_list = []
    for i, file_attribute in enumerate(file_attributes.splitlines()):
        if (file_attribute[:len(attribute_identifier)] == attribute_identifier):
            attributes = file_attribute.split(",")
            file_attribute = ""

            if is_tab_visible:
                attributes[1] = "true"
            else:
                attributes[1] = "false"
            
            sorted_attributes = attributes[2:].sort()

            file_attribute = attribute_identifier + "," + attributes[1]

            for attribute in sorted_attributes:
                file_attribute = file_attribute +  "," + attribute
            
        attribute_data_list.append(file_attribute)
        
    update_file_attributes (attribute_data_list)

def create_main_window():
    main_window = tkinter.Tk()
    main_window.title("Attribute Manager")
    return main_window

def create_attribute_file_frame(main_window):
    global reference_var
    
    attribute_file_frame = ttk.Frame(main_window, padding=10)
    attribute_file_frame.grid(row=0, column=0, sticky=W+E)

    reference_label = ttk.Label(attribute_file_frame, text="参照＞＞", padding=(5, 2))
    reference_label.grid(row=0, column=0, sticky=W+E)

    reference_var = StringVar()
    reference_entry = ttk.Entry(attribute_file_frame, textvariable=reference_var, width=30)
    reference_entry.grid(row=0, column=1, sticky=W+E)

    reference_button = ttk.Button(attribute_file_frame, text="参照", command=browse_directory_dialog)
    reference_button.grid(row=0, column=2, sticky=W+E)

    create_attributes_file_button = ttk.Button(attribute_file_frame, text="属性ファイル追加", command=print)
    create_attributes_file_button.grid(row=0, column=3, sticky=W+E)

def create_attribute_identifier_frame(main_window):
    attribute_identifier_frame = ttk.Frame(main_window, padding=10)
    attribute_identifier_frame.grid(row=1, column=0, sticky=W+E)

    reference_label = ttk.Label(attribute_identifier_frame, text="タブタイトル", padding=(5, 2))
    reference_label.grid(row=0, column=0, sticky=W+E)

    attribute_identifier_entry = ttk.Entry(attribute_identifier_frame, textvariable=StringVar(), width=30)
    attribute_identifier_entry.grid(row=0, column=1, sticky=W+E)

    attribute_identifier_tab_visible_var = BooleanVar()
    attribute_identifier_tab_visible_var.set(False)
    show_attribute_identifier_tab_checkbox = ttk.Checkbutton(
        attribute_identifier_frame, padding=(10), text="検索時のタブ表示",
        variable=attribute_identifier_tab_visible_var
        )
    show_attribute_identifier_tab_checkbox.grid(row=0, column=2, sticky=W+E)
    
    create_attributes_file_button = ttk.Button(attribute_identifier_frame, text="属性タブ追加", 
        command=lambda: add_attribute_tab(attribute_identifier_entry.get(),attribute_identifier_tab_visible_var.get(),main_window))
    create_attributes_file_button.grid(row=0, column=3, sticky=W+E)

def create_checkbox_frame(main_window):
    global checkbox_bool_matrix,file_attributes
    checkbox_bool_matrix=[]

    checkbox_tab_note = ttk.Notebook(main_window)
    checkbox_tab_note.grid(row=2, column=0, sticky=W+E)

    if not file_attributes:
        empty_tab = ttk.Frame(checkbox_tab_note)

        checkbox_tab_note.add(empty_tab, text = "空のタブ")
        checkbox_tab_note.grid(row=1, column=0, sticky=W + E + N + S)

        empty_label = ttk.Label(empty_tab, text = "要素が空です")
        empty_label.pack()

        return

    attribute_identifier_tab_visible_vars = []
    for i,file_attribute in enumerate(file_attributes.splitlines()):
        checkbox_bool_matrix.append(list())

        attributes = file_attribute.split(',')
        attribute_title = attributes[0]

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

        attribute_identifier_tab_visible_vars.append(BooleanVar(value=attributes[1] == "true"))
        show_attribute_identifier_tab_checkbox = ttk.Checkbutton(
            scrollable_frame, padding=(10), text="検索時のタブ表示",
            variable=attribute_identifier_tab_visible_vars[i],
            command=lambda:update_tab_visibility_settings(attribute_title,attribute_identifier_tab_visible_vars[i]) 
            )
        show_attribute_identifier_tab_checkbox.grid(row=0, column=0, sticky=W+E)

        attribute_entry = ttk.Entry(scrollable_frame, textvariable=StringVar(), width=30)
        attribute_entry.grid(row=0, column=1, sticky=W+E)

        add_attribute_button = ttk.Button(scrollable_frame, text="属性追加", command=lambda title=attribute_title, entry=attribute_entry: update_attributes(title, entry.get(),main_window))
        add_attribute_button.grid(row=0, column=2, sticky=W+E)      

        checkbox_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        for j, attribute in enumerate(attributes[2:]):
            is_checked = BooleanVar()
            checkbox_bool_matrix[i].append(is_checked)
            attribute_checkbox = ttk.Checkbutton(
                scrollable_frame, padding=(10), text=attribute,
                variable=checkbox_bool_matrix[i][j]
            )
            attribute_checkbox.grid(row=1+(j // 3), column=j % 3, sticky=W + E + N + S)

def create_frames(main_window):
    create_attribute_file_frame(main_window)
    create_attribute_identifier_frame(main_window)
    create_checkbox_frame(main_window)

def main():
    load_file_attributes()
    main_window = create_main_window()
    create_frames(main_window)
    main_window.mainloop()

if __name__ == "__main__":
    main()
