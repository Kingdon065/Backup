#!/usr/bin/python3
# _*_ coding:utf-8 _*_
# @Author: Evil Mat
# @Date: 2020/8/23 13:18

import os
import shutil
import time
from zipfile import ZipFile, ZIP_BZIP2, ZIP_STORED, ZIP_LZMA, ZIP_DEFLATED
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
from ui_backup import *

# 压缩算法
compressions = {
    'zip_stored': ZIP_STORED,
    'zip_deflated': ZIP_DEFLATED,
    'zip_bzip2': ZIP_BZIP2,
    'zip_lzma': ZIP_LZMA
}


def get_datetime():
    now = time.ctime()
    parsed = time.strptime(now)
    return time.strftime('%Y-%m-%d_%H-%M-%S', parsed)


def bytes2human(bytes):
    """将字节数转换为人类可读的数"""
    symbols = ('KB', 'MB', 'GB', 'TB')
    prefix = {}
    for i, s in enumerate(symbols):
         prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if bytes >= prefix[s]:
            value = bytes / prefix[s]
            return f'{value:.2f}{s}'
    return f'{bytes:.2f}B'


class BackupFolder:
    def __init__(self):
        self.root = Tk()
        
        self.ui = Ui_Backup(self.root)
        self.is_open = False
        self.ui.folder_btn.config(command=self.open_folder)
        self.ui.bak_folder_btn.config(command=self.open_bak_folder)
        self.ui.zip_btn.config(command=self.open_zip_folder)
        
        self.ui.compression_cb['value'] = tuple(compressions.keys())
        self.ui.compression_cb.current(2)
        
        self.ui.backupasfolder_btn.config(command=self.backup2folder)
        self.ui.backupaszip_btn.config(command=self.backup2zip)
        
        self.root.mainloop()
    
    def open_folder(self):
        self.is_open = True
        folder = askdirectory(title='打开要备份的文件夹')
        self.ui.folderVar.set(folder)
        self.ui.bakfolderVar.set(folder + '_bak')
        
        self.basename = os.path.basename(folder)
        self.zip_filename = f'{self.basename}_{get_datetime()}.zip'
        zip_path = os.path.join(os.path.dirname(folder), self.zip_filename)
        self.ui.zipVar.set(zip_path)
        
    def open_bak_folder(self):
        if not self.is_open:
            showinfo(title='提示', message='请先设置备份文件夹，再试！')
            return
        bak_folder = askdirectory(title='设置备份文件夹')
        path = os.path.join(bak_folder, self.basename + '_bak')
        self.ui.bakfolderVar.set(path)
    
    def open_zip_folder(self):
        if not self.is_open:
            showinfo(title='提示', message='请先设置备份文件夹，再试！')
            return
        zip_folder = askdirectory(title='设置zip文件夹')
        self.ui.zipVar.set(os.path.join(zip_folder, self.zip_filename))
    
    def write2text(self, s):
        self.ui.text.insert(INSERT, s)
        self.ui.text.see(END)   # Text控件随输入自动拓展到尾行
        self.ui.text.update()

    def filter(self, path):
        path_filter = self.ui.path_filter.get().split(';')

        if path_filter == ['']:
            path_filter[0] = 'null_NULL'

        for keyword in path_filter:
            if keyword in path:
                return True
        return False
    
    def backup2folder(self):
        """备份为文件"""
        self.ui.text.delete(1.0, END)
        
        origin_folder = self.ui.folderVar.get()
        if not os.path.exists(origin_folder):
            showinfo(title='提示', message='备份文件夹不存在!')
            return
        
        backup_folder = self.ui.bakfolderVar.get()

        extensions = self.ui.extensions_filter.get().split(';')
        if extensions == ['']:
            extensions[0] = 'null_NULL'
        
        for folder, subfolders, filenames in os.walk(origin_folder):
            bak_folder = folder.replace(origin_folder, backup_folder)
            if self.filter(bak_folder) == False:
                self.write2text(f'INFO - 创建文件夹<{bak_folder}>...\n')
                os.makedirs(bak_folder, exist_ok=True)
            else:
                self.write2text(f'INFO - 跳过文件夹<{folder}>...\n')
                continue

            for subfolder in subfolders:
                bak_sub_folder = os.path.join(bak_folder, subfolder)
                if self.filter(bak_sub_folder) == False:
                    self.write2text(f'INFO - 创建子文件夹<{bak_sub_folder}>...\n')
                    os.makedirs(bak_sub_folder, exist_ok=True)

            for filename in filenames:
                if os.path.splitext(filename)[1] in extensions:   # 默认不复制zip和exe文件
                    self.write2text(f'INFO - 跳过文件<{filename}>\n')
                    continue
                file_name = os.path.join(folder, filename)
                bak_filename = os.path.join(bak_folder, filename)
                if self.filter(file_name) == False:
                    try:
                        self.write2text(f'INFO - 将<{file_name}>复制到<{bak_filename}>...\n')
                        shutil.copy(file_name, bak_filename)
                    except:
                        self.write2text(f'ERROR - 无法复制{file_name}\n')
                        
        self.write2text('INFO - 复制完成!\n\n')
    
    def backup2zip(self):
        """备份到压缩文件"""
        self.ui.text.delete(1.0, END)
        
        origin_folder = self.ui.folderVar.get()
        if not os.path.exists(origin_folder):
            showinfo(title='提示', message='备份文件夹不存在!')
            return
        
        compression = self.ui.compressionVar.get()
        zip_path = self.ui.zipVar.get()
        if not os.path.exists(os.path.dirname(zip_path)):
            showinfo(title='提示', message='保存zip文件的文件夹不存在!')
            return

        self.write2text(f'INFO - 创建文件 {self.zip_filename}，采用{compression}压缩算法...\n')
        c = compressions[compression]
        backupZip = ZipFile(zip_path, 'w', compression=c)   # 使用bzip2压缩算法
        
        os.chdir(origin_folder)
        os.chdir('../')
        folder = os.path.basename(origin_folder)

        extensions = self.ui.extensions_filter.get().split(';')
        if extensions == ['']:
            extensions[0] = 'null_NULL'

        for folder, subfolders, filenames in os.walk(folder):
            if self.filter(folder) == False:
                self.write2text(f'\nINFO - 正在添加文件夹 {folder}...\n')
                backupZip.write(folder)
            else:
                self.write2text(f'\nINFO - 跳过文件夹 {folder}...\n')
                continue
            for filename in filenames:
                if os.path.splitext(filename)[1] in extensions:
                    self.write2text(f'\nINFO - 跳过文件 {filename}...\n')
                    continue
                path = os.path.join(folder, filename)
                if self.filter(path) == False:
                    self.write2text(f'INFO - 正在写入文件 {filename}...\n')
                    backupZip.write(path)
        backupZip.close()
        
        size = bytes2human(os.path.getsize(zip_path))
        self.write2text(f'INFO - 生成的ZIP文件 {self.zip_filename} ({size})在 {os.path.dirname(zip_path)}\n\n')


if __name__ == '__main__':
    BackupFolder()