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

EXE_NAME = 'TransTube'

SELECT_MOV2MP4 = 'MOV to MP4'

if __name__ == '__main__':

    root = tkinter.Tk()
    root.title(EXE_NAME)
    iconfile = resourcePath('resources\\favicon.ico')
    root.iconbitmap(default=iconfile)
    
    #ラベル
    Static1 = tkinter.Label(text=u'変換元ファイル：')
    Static1.grid(row=0,column=0)
    #エントリー
    EditBox = tkinter.Entry()
    EditBox.insert(tkinter.END,"")
    EditBox.grid(row=0,column=1)

    def select_file(event):
        fTyp = [("MOVファイル","*.mov")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        EditBox.insert(tkinter.END,file)

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
    
    root.mainloop()