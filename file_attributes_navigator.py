import os,sys
import tkinter
from tkinter import *
from tkinter import ttk

def search():
    print

def create_main_window():
    main_window = tkinter.Tk()
    main_window.title("File Attributes Navigator")
    return main_window

def create_search_frame(main_window):
    search_frame = ttk.Frame(main_window, padding=10)
    search_frame.grid(row=0, column=0, sticky=E)

    search_word_label = ttk.Label(search_frame, text="検索ワード", padding=(5, 2))
    search_word_label.pack(side=LEFT)

    search_word_entry = ttk.Entry(search_frame, textvariable=StringVar(), width=30)
    search_word_entry.pack(side=LEFT)

    search_button = ttk.Button(search_frame, text="検索", command=search)
    search_button.pack(side=LEFT)

def create_checkbox_frame(main_window, options):
    checkbox_canvas = Canvas()


    
    checkbox_frame = ttk.Frame(checkbox_canvas, padding=10)
    checkbox_frame.grid(row=0, column=0, sticky=E)



def create_frames(main_window):
    create_search_frame(main_window)
    create_checkbox_frame(main_window, "a")

def main():
    main_window = create_main_window()
    create_frames(main_window)
    main_window.mainloop()

if __name__ == "__main__":
    main()
