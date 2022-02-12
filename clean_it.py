#!/usr/bin/python

import os,sys
import pathlib
import shutil
from os.path import expanduser

columns = shutil.get_terminal_size().columns
reduced_size = 0

dirty_dirs = {"迅雷下载":r"C:\ProgramData\Thunder Network\XLLiveUD\Download",
                "Pycharm":os.path.join(expanduser("~"), "AppData\Local\JetBrains\PyCharm2020.1\caches\content.dat.storageData")}


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def traversal_dir(dirname):
    for file_name in dirname.rglob("*"):
        yield file_name


def clean_sys_submodule(idx, temp_dir, module_name, mod_ptrn, need_check=1):
    global reduced_size
    sub_module_name = module_name
    answer = 'n'
    tmp_count = 0
    tmp_size = 0
    print("> 开始清理第{}个位置，模块:{}..\r\n路径为:{}".format(idx,sub_module_name, temp_dir))
    for file_name in temp_dir.rglob(mod_ptrn):
        print(file_name)
        tmp_count +=1
        if os.path.isdir(file_name):
            path_size = sum(f.stat().st_size for f in file_name.glob('**/*') if f.is_file())
        else:
            path_size = file_name.stat().st_size
        tmp_size += path_size
    
    if tmp_count < 1:
        print("跳过，路径不存在:{}".format(sub_module_name))
        return
    print("清理前{}临时文件[{}],共{}.".format(sub_module_name, tmp_count,sizeof_fmt(tmp_size)))
    if need_check == 1:
        while True:
            answer = input("你确定要删除上面这些目录或文件吗? Y or N?\r\n").lower()
            if answer in ('y', 'n'):
                break
    else:
        answer = 'y'
    if answer == 'y': 
        try:
            for sub_path in temp_dir.rglob(mod_ptrn):
                # print(sub_path)
                if os.path.isdir(sub_path):
                    shutil.rmtree(sub_path)
                else:
                    os.remove(sub_path)
        except Exception as e:
            print(e)
        reduced_size += tmp_size
        print("已经清理模块: %s"%sub_module_name)
        if os.path.isdir(temp_dir):
            print("残余文件[{}]: {}".format(len([x for x in temp_dir.rglob(mod_ptrn)]),temp_dir.rglob(mod_ptrn)))
        else:
            print("残余文件[{}]: {}".format(1,sub_module_name))
    else:
        print("跳过目录:%s"%sub_module_name)


def clean_systemp():
    global reduced_size
    module_name = "系统应用缓存"
    home_dir = expanduser("~")
    temp_dir = os.path.join(home_dir, "AppData\Local\Temp")
    tmp_count = 0
    tmp_size = 0
    path= pathlib.Path(temp_dir)
    submodule_list = [("Microsoft Office","TCD*.tmp", 1 ), 
                ("火狐浏览器升级","MozillaBackgroundTask-*", 0 ), 
                ("Outlook","CVR*.tmp.cvr", 0 ),
                # ("7Zip","7zO*", 0 ),
                ("adobe","~DF*.TMP", 0 )]
    for submodule in submodule_list:
        clean_sys_submodule(1, path, *submodule )
    

def clean_dir(index, module_name, dirname):
    global reduced_size
    answer = 'n'
    path = pathlib.Path(dirname)
    print("> 开始清理第{}个位置，模块:{}..\r\n路径为:{}".format(index,module_name, dirname))
    if not os.path.exists(path):
        print("跳过，路径不存在:{}".format(path))
        return
    if os.path.isdir(path):
        path_size = sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
        print("清理前文件[{}],共{}: {}".format(len(os.listdir(dirname)),sizeof_fmt(path_size),os.listdir(dirname)))
    else:
        path_size = path.stat().st_size
        
        print("清理前文件[{}],共{}: {}".format(1,sizeof_fmt(path_size),dirname))

    
    while True:
        answer = input("你确定要删除上面这些目录或文件吗? Y or N?\r\n").lower()
        if answer in ('y', 'n'):
            break
    if answer == 'y': 
        if os.path.isdir(path):
            for sub_path in traversal_dir(path):
                print(sub_path)
                if os.path.isdir(sub_path):
                    shutil.rmtree(sub_path)
                else:
                    os.remove(sub_path)
        else:
            os.remove(path)
        reduced_size += path_size
        print("已经清理目录: %s"+dirname)
        if os.path.isdir(path):
            print("残余文件[{}]: {}".format(len(os.listdir(dirname)),os.listdir(dirname)))
        else:
            print("残余文件[{}]: {}".format(1,dirname))
    else:
        print("跳过目录:%s"%dirname)

if __name__ == "__main__":
    print("======欢迎使用Win7空间清理工具======".center(columns))
    for index,module_name in enumerate( dirty_dirs):
        dirname = dirty_dirs.get(module_name)
        clean_dir(index, module_name, dirname)
        print("\r\n")
    clean_systemp()
    print("\r\n\r\n共清理空间[{}]".format(sizeof_fmt(reduced_size)))
