#!/usr/bin/env python 
## author: counsellors

import os
import pathlib
import shutil
import sys
from datetime import datetime
from os.path import expanduser

from cv2 import fitEllipse
from loguru import logger
from win32com.shell import shell, shellcon

ext_list = {'pcap':["*.pcap","*.pcapng"],
            'pdf':"*.pdf",
            'xmind':["*.xmind","*.vsdx"],
            'doc':["*.xlsx","*.xls","*.pptx","*.ppt","*.docx","*.doc","*.md"],
            'image':["*.png","*.jpg","*.ico"],
            'script':["*.sh","*.py","*.bat"],
            'txt':["*.txt","*.sql","*.json","*.repo","*.html"]}

columns = shutil.get_terminal_size().columns

def traversal_dir(dirname, file_type):
    file_ptrns = ext_list.get(file_type)
    if not file_ptrns :
        return 
    if isinstance(file_ptrns, list) and len(file_ptrns) >1:
        for file_ptrn in file_ptrns:
            for file_name in dirname.glob(file_ptrn):
                yield file_name
    elif isinstance(file_ptrns, str):
        for file_name in dirname.glob(file_ptrns):
            yield file_name

def check_manual(deskdir, file_type):
    answer = 'n'
    tmp_num = 0
    deleted_num = 0
    while True:
        answer = input("你确定要删除上面这些目录或文件吗? Y or N?\r\n").lower()
        if answer in ('y', 'n'):
            break
    if answer == 'y': 
        for filename in traversal_dir(deskdir, file_type):
            logger.debug(filename)
            tmp_num += 1
            if os.path.exists(filename) and os.path.isfile(filename):
                # os.remove(str(filename))
                # 删除到回收站
                result, aborted = shell.SHFileOperation((0,shellcon.FO_DELETE,str(filename),None, shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,None,None))  #删除文件到回收站
                if not aborted and result != 0:
                    logger.error("Error, file: {} can't be deleted!!".format(filename))
                    raise WindowsError('SHFileOperation failed: 0x%08x' % result)
                    
                else:
                    deleted_num += 1

    logger.debug("已经清理桌面上的{}文件[{}]个.".format(file_type, deleted_num))

def organize_desktop(module_name, deskdir):
    tmp_num = 0
    tmp_copied_num = 0
    dt = datetime.now() 
    dest_dir = os.path.join(deskdir, module_name+"_"+dt.strftime( '%Y%m%d%H' ))
    logger.debug(dest_dir)
    try:
        os.mkdir(dest_dir)
    except Exception as e:
        logger.warning(e)
    for filename in traversal_dir(deskdir, module_name):
        logger.debug(filename)
        if os.path.exists(dest_dir) and os.path.isdir(dest_dir):
            shutil.copy2(str(filename), dest_dir)
        tmp_num += 1

    logger.debug("原始文件个数:{}, 目标文件已有个数:{}".format(tmp_num, len(os.listdir(dest_dir))))
    if tmp_num >0:
        check_manual(deskdir,module_name)

def main():
    logger.debug("======欢迎使用Win7桌面整理工具======")
    deskdir_name = os.path.join(expanduser("~"), "Desktop")
    deskdir = pathlib.Path(deskdir_name)
    logger.debug(deskdir)
    organize_desktop("pcap", deskdir)
    organize_desktop("doc", deskdir)
    organize_desktop("image", deskdir)
    organize_desktop("pdf", deskdir)
    organize_desktop("script", deskdir)
    organize_desktop("txt", deskdir)
    organize_desktop("xmind", deskdir)



if __name__ == "__main__":
    main()
