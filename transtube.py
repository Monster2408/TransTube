#!/usr/bin/env python
# -*- coding: utf8 -*-
import tkinter, tkinter.filedialog
import tkinter.ttk as ttk
from tkinter import messagebox
import sys
import os

import mov2mp4

def resourcePath(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(filename)

def get_user_dir():
    iDir = os.path.abspath(os.path.dirname(__file__))
    user_dir = os.path.join(iDir, 'user')
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir

def get_cache_file():
    user_cache_file = os.path.join(get_user_dir(), 'cache.txt')
    return user_cache_file

EXE_NAME = 'TransTube'
VERSION = '1.0.1'

SELECT_MOV2MP4 = 'MOV to MP4'

if __name__ == '__main__':

    root = tkinter.Tk()
    root.title(EXE_NAME)
    iconfile = resourcePath('resources\\favicon.ico')
    root.iconbitmap(default=iconfile)
    
    menu=tkinter.Menu(root)
    #個別のmenuを作る
    menu_1=tkinter.Menu(menu,tearoff=False)
    menu_1.add_command(label="終了",command=root.quit)
    #menuを親menuに追加
    menu.add_cascade(label="ファイル",menu=menu_1)
    
    menu_2=tkinter.Menu(menu,tearoff=False)
    menu_2.add_command(label="バージョン情報",command=lambda: messagebox.showinfo(EXE_NAME, 'v' + VERSION))
    menu.add_cascade(label="ヘルプ",menu=menu_2)
    
    #ラベル
    Static1 = tkinter.Label(text=u'変換元ファイル：')
    Static1.grid(row=0,column=0)
    
    user_cache_file = get_cache_file()
    file_path = ''
    if os.path.exists(user_cache_file):
        with open(user_cache_file, 'r') as f:
            file_path = f.read()
    if not os.path.exists(file_path):
        file_path = ''
    
    #エントリー
    EditBox = tkinter.Entry()
    EditBox.insert(tkinter.END, file_path)
    EditBox.grid(row=0,column=1)

    def select_file(event):
        fTyp = [("MOVファイル","*.mov")]
        if os.path.exists(EditBox.get()):
            iDir = os.path.dirname(EditBox.get())
        else:
            iDir = os.path.abspath(os.path.dirname(__file__))
        file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        EditBox.delete(0, tkinter.END)
        EditBox.insert(tkinter.END,file)
        
        user_cache_file = get_cache_file()
        with open(user_cache_file, 'w') as f:
            f.write(file)

    #ボタン
    SelectFileButton = tkinter.Button(text=u'選択')
    SelectFileButton.bind("<Button-1>",select_file) 
    SelectFileButton.grid(row=0,column=2)
    
    #ラベル
    Static2 = tkinter.Label(text=u'変換先ファイル：')
    Static2.grid(row=1,column=0)
    
    module = [SELECT_MOV2MP4]
    Combobox = ttk.Combobox(root, values=module)
    Combobox.grid(row=1,column=1)
    
    # 実行
    def convert(event):
        input_file = EditBox.get()
        if not os.path.exists(input_file):
            messagebox.showwarning(EXE_NAME, 'ファイルが存在しません。')
            return
        type_text = Combobox.get()
        input_file = input_file.replace('\\', '\\\\')
        if type_text == SELECT_MOV2MP4:
            output_file = EditBox.get().replace('.mov', '.mp4')
            mov2mp4.build(input_file, output_file)
        else:
            messagebox.showwarning(EXE_NAME, '変換形式を選択してください。')
    
    SelectFileButton = tkinter.Button(text=u'実行')
    SelectFileButton.bind("<Button-1>",convert) 
    SelectFileButton.grid(row=2,column=2)
    
    root["menu"]=menu
    root.mainloop()