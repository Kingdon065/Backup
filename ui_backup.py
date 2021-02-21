from tkinter import *
from tkinter.ttk import Combobox
from tkinter.font import Font


def window_center(parent, width, height):
        win_width = parent.winfo_screenwidth()
        win_height = parent.winfo_screenheight()
        x = int((win_width - width) / 2)
        y = int((win_height - height) / 2)
        parent.geometry(f'{width}x{height}+{x}+{y}')


class Ui_Backup:
    def __init__(self, parent):
        self.root = parent
        self.root.title('Backup Folder 1.0')
        window_center(self.root, 900, 700)
        self.root.iconphoto(True, PhotoImage(file='~/.local/pyscripts/icon/backup01.png'))
        
        top_frame = Frame(self.root)
        top_frame.pack(pady=5)
        
        Label(top_frame, text='备份文件夹', width=11, anchor=E, font=Font(size=12)).grid(row=0, column=0, pady=8)
        self.folderVar = StringVar()
        self.folder_path = Entry(top_frame, width=55, textvariable=self.folderVar, font=Font(size=11))
        self.folder_path.grid(row=0, column=1, padx=5)
        self.folder_btn = Button(top_frame, text='浏览...')
        self.folder_btn.grid(row=0, column=2)
        
        Label(top_frame, text='保存为文件夹', width=11, anchor=E, font=Font(size=12)).grid(row=1, column=0, pady=8)
        self.bakfolderVar = StringVar()
        self.bak_folder_path = Entry(top_frame, width=55, textvariable=self.bakfolderVar, font=Font(size=11))
        self.bak_folder_path.grid(row=1, column=1, padx=5)
        self.bak_folder_btn = Button(top_frame, text='浏览...')
        self.bak_folder_btn.grid(row=1, column=2)
        
        Label(top_frame, text='保存为zip文件', width=11, anchor=E, font=Font(size=12)).grid(row=2, column=0, pady=8)
        self.zipVar = StringVar()
        self.zip_path = Entry(top_frame, width=55, textvariable=self.zipVar, font=Font(size=11))
        self.zip_path.grid(row=2, column=1, padx=5)
        self.zip_btn = Button(top_frame, text='浏览...')
        self.zip_btn.grid(row=2, column=2)
         
        Label(top_frame, text='压缩算法', width=11, anchor=E, font=Font(size=12)).grid(row=3, column=0, pady=8)
        self.compressionVar = StringVar()
        self.compression_cb = Combobox(top_frame, textvariable=self.compressionVar)
        self.compression_cb.grid(row=3, column=1, columnspan=2, padx=5, sticky=W)
        
        Label(top_frame, text='扩展名过滤', width=11, anchor=E, font=Font(size=12)).grid(row=4, column=0, pady=8)
        self.extensions_filter = Entry(top_frame, width=55, font=('Source Code Pro', 11))
        self.extensions_filter.insert(0, '.exe;.ini;.zip;.rar')
        self.extensions_filter.grid(row=4, column=1, columnspan=2, padx=5, sticky=W)
        
        Label(top_frame, text='路径过滤', width=11, anchor=E, font=Font(size=12)).grid(row=5, column=0, pady=8)
        self.path_filter = Entry(top_frame, width=55, font=('Source Code Pro', 11))
        self.path_filter.insert(0, 'venv')
        self.path_filter.grid(row=5, column=1, columnspan=2, padx=5, sticky=W)
        
        middle_frame = Frame(self.root)
        middle_frame.pack(pady=5)
        
        self.backupasfolder_btn = Button(middle_frame, text='备份为文件夹', bg='#f0e68c')
        self.backupasfolder_btn.grid(row=0, column=0)
        
        self.backupaszip_btn = Button(middle_frame, text='备份为zip', bg='#ffb6c1')
        self.backupaszip_btn.grid(row=0, column=1, padx=20)
        
        self.show_details = True
        self.show_btn = Button(middle_frame, text='隐藏细节', command=self.show)
        self.show_btn.grid(row=0, column=2)
        
        bottom_frame = Frame(self.root)
        bottom_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        self.scrollbar_x = Scrollbar(bottom_frame, orient=HORIZONTAL)
        self.scrollbar_y = Scrollbar(bottom_frame)
        
        self.text = Text(bottom_frame, padx=5, pady=5, wrap='none', bg='#000001', fg='#00ff00')
        self.text.config(font=Font(size=12))
        self.text.config(insertbackground='white')
        self.text.config(xscrollcommand=self.scrollbar_x.set)
        self.text.config(yscrollcommand=self.scrollbar_y.set)
        
        self.scrollbar_x.config(command=self.text.xview)
        self.scrollbar_y.config(command=self.text.yview)
        
        self.scrollbar_x.pack(side=BOTTOM, fill=X)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.text.pack(fill=BOTH, expand=True)
    
    def show(self):
        if self.show_details == False:
            self.show_details = True
            self.show_btn.config(text='隐藏细节')
            
            self.scrollbar_x.pack(side=BOTTOM, fill=X)
            self.scrollbar_y.pack(side=RIGHT, fill=Y)
            self.text.pack(fill=BOTH, expand=True)
        else:
            self.show_details = False
            self.show_btn.config(text='显示细节')
            self.text.pack_forget()
            self.scrollbar_x.pack_forget()
            self.scrollbar_y.pack_forget()
      
      
if __name__ == '__main__':
    Ui_Backup()