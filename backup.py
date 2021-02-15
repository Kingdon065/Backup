#!/usr/bin/python3
# _*_ coding:utf-8 _*_
# @Author: Evil Mat
# @Date: 2020/8/23 13:18

import os
import shutil
import time
import argparse
import logging
from zipfile import ZipFile, ZIP_BZIP2, ZIP_STORED, ZIP_LZMA, ZIP_DEFLATED


logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
log = logging.getLogger(__name__)


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


def backup2file(origin_folder, backup_dir, view, extension, filter):
    """备份为文件"""
    for folder, subfolders, filenames in os.walk(origin_folder):
        bak_folder = folder.replace(origin_folder, backup_dir)
        if filter not in bak_folder:
            if view:
                print(f'INFO - 创建文件夹<{bak_folder}>...')
            os.makedirs(bak_folder, exist_ok=True)

        for subfolder in subfolders:
            bak_sub_folder = os.path.join(bak_folder, subfolder)
            if filter not in bak_sub_folder:
                if view:
                    print(f'INFO - 创建文件夹<{bak_sub_folder}>...')
                os.makedirs(bak_sub_folder, exist_ok=True)

        for filename in filenames:
            if os.path.splitext(filename)[1] in extension:   # 默认不复制zip和exe文件
                if view:
                    print(f'INFO - 跳过文件<{filename}>')
                continue
            file_name = os.path.join(folder, filename)
            bak_filename = os.path.join(bak_folder, filename)
            if filter not in file_name:
                try:
                    if view:
                        print(f'INFO - 将<{file_name}>复制到<{bak_filename}>...')
                    shutil.copy(file_name, bak_filename)
                except:
                    if view:
                        print(f'ERROR - 无法复制{file_name}')
    print('INFO - 复制完成!')


def backup2zip(origin_folder, compression, view, extension, filter, pathZip):
    """备份到压缩文件"""
    compression_lower = compression.lower()
    filename_zip = f'{os.path.basename(origin_folder)}_{get_datetime()}_bak.zip'
    print(f'INFO - 创建文件{filename_zip}，采用{compression_lower}压缩算法...')
    c = compressions[compression_lower]
    backupZip = ZipFile(filename_zip, 'w', compression=c)   # 使用bzip2压缩算法
    
    cur_dir = os.getcwd()
    
    os.chdir(origin_folder)
    os.chdir('../')
    folder = os.path.basename(origin_folder)

    for folder, subfolders, filenames in os.walk(folder):
        if filter not in folder:
            if view:
                print(f'INFO - 添加文件到{folder}')
            backupZip.write(folder)
        else:
            continue
        for filename in filenames:
            if os.path.splitext(filename)[1] in extension:  # 默认不备份zip和exe文件
                if view:
                    print(f'INFO - 跳过文件<{filename}>')
                continue
            path = os.path.join(folder, filename)
            if filter not in path:
                backupZip.write(path)
    backupZip.close()
    
    os.chdir(cur_dir)
    size = bytes2human(os.path.getsize(filename_zip))
    print(f'INFO - 生成的ZIP文件 {filename_zip} ({size})在 {os.getcwd()}')

    if pathZip != '.':
        if os.path.exists(pathZip):
            print(f'INFO - 开始复制文件<{filename_zip}>到{pathZip}...')
            shutil.copy(filename_zip, os.path.join(pathZip, filename_zip))
            print('INFO - 复制完成！')
            print(f'INFO - 开始删除当前目录下的<{filename_zip}>....')
            os.unlink(filename_zip)
            print('INFO - 删除完成！')
        else:
            print(f'INFO - <{pathZip}>不存在！')


def backup():
    parse = argparse.ArgumentParser(
        prog='backup',
        description='备份文件夹'
    )
    parse.add_argument(
        '-d',
        '--dir',
        default='/home/masy/Projects',
        help='指定要备份的文件夹，默认为</home/masy/Projects>'
    )
    parse.add_argument(
        '-f',
        '--file',
        action='store_true',
        help='备份文件的类型为普通文件夹'
    )
    parse.add_argument(
        '-z',
        '--zip',
        action='store_true',
        help='备份文件的类型为压缩文件zip，默认采用bzip2压缩算法'
    )
    parse.add_argument(
        '-c',
        '--compression',
        default='zip_bzip2',
        help='压缩算法，默认为zip_bzip2，可用压缩算法有：zip_stored, zip_deflated, zip_lzma'
    )
    parse.add_argument(
        '-v',
        '--view',
        action='store_true',
        help='显示备份过程'
    )
    parse.add_argument(
        '--ext',
        nargs='+',
        default=['.exe', '.zip', '.ini'],
        help="不备份的文件类型列表，默认('.exe', '.zip', '.ini')"
    )
    parse.add_argument(
        '--filter',
        default='venv',
        help='路径过滤器，默认过滤掉含有“venv”的路径'
    )
    parse.add_argument(
        '-pf',
        '--pathFile',
        default='.',
        help='指定普通文件夹的存储路径，默认与源文件夹同目录，后缀为“_bak”'
    )
    parse.add_argument(
        '-pz',
        '--pathZip',
        default='.',
        help='指定zip文件的存储路径, 默认为当前路径'
    )

    args = parse.parse_args()

    origin_folder = os.path.abspath(args.dir)

    if not os.path.exists(origin_folder):
        print(f'ERROR - <{origin_folder}>不存在！')
        return

    if args.file:
        backup_dir = origin_folder + '_bak'
        if args.pathFile != '.':
            if os.path.exists(args.pathFile):
                backup_dir = os.path.join(args.pathFile, os.path.basename(origin_folder))
            else:
                print(f'ERROR - <{args.pathFile}>不存在！')
                return
        backup2file(origin_folder, backup_dir, args.view, args.ext, args.filter)
        return

    if args.zip:
        try:
            backup2zip(origin_folder, args.compression, args.view, args.ext, args.filter, args.pathZip)
        except KeyError:
            print(f'ERROR - 指定的压缩算法{args.compression}不存在！')


if __name__ == '__main__':
    backup()