import os, re, io
import os.path
import shutil
import time, datetime

def get_config_item_path(dir, name):
    default_dir = os.path.join(dir, name)
    return default_dir


def read_file(filepath):
    with io.open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filepath, content):
    with io.open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def copyFiles(sourceDir, targetDir):  # 把某一目录下的所有文件复制到指定目录中
    if sourceDir.find(".svn") > 0:
        return
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, file)
        targetFile = os.path.join(targetDir, file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or (
                os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
        if os.path.isdir(sourceFile):
            First_Directory = False
            copyFiles(sourceFile, targetFile)


def removeFileInFirstDir(targetDir):  # 删除一级目录下的所有文件
    for file in os.listdir(targetDir):
        targetFile = os.path.join(targetDir, file)
        if os.path.isfile(targetFile):
            os.remove(targetFile)


def coverFiles(sourceDir, targetDir):  # 复制一级目录下的所有文件到指定目录
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, file)
        targetFile = os.path.join(targetDir, file)
        # cover the files
        if os.path.isfile(sourceFile):
            open(targetFile, "wb").write(open(sourceFile, "rb").read())


def moveFileto(sourceDir, targetDir):  # 复制指定文件到目录
    shutil.copy(sourceDir, targetDir)


def removeFolders(path):
    shutil.rmtree(path)


def getCurTime():  # 返回当前的日期，以便在创建指定目录的时候用
    nowTime = time.localtime()
    year = str(nowTime.tm_year)
    month = str(nowTime.tm_mon)
    if len(month) < 2:
        month = '0' + month
    day = str(nowTime.tm_yday)
    if len(day) < 2:
        day = '0' + day
    return (year + '-' + month + '-' + day)
