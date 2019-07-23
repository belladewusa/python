# -*- coding: UTF8 -*-
#此脚本大家参考
#python3
from  time import strftime
import os
import tarfile
import pickle
import hashlib
import datetime
def check_md5(fname):
    m = hashlib.md5()
    with open(fname,'rb') as fobj:
        while True:
            data =fobj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()

#删除大于31天的完全备份
def del_full_file(filePath):
    filter = ['full']  # 设置过滤后的文件类型 当然可以设置多个类型
    #    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(filePath):

        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",file_name_list)  #当前主目录下的所有文件

        for filename in file_name_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            try:
                os.path.split(apath)[1].split(sep='_', )[1]
            except IndexError:
                pass
                continue
            ext = os.path.split(apath)[1].split(sep='_', )[1]
            if ext in filter:
                t1=os.path.getatime(filePath)
                local_time=datetime.datetime.fromtimestamp(t1)
                t2=datetime.datetime.now()
                t3 = t2 - local_time
#                print(t3.days)
                if t3.days > 31:
                    os.remove(filePath)
#    return datetime.datetime.strftime(local_time,'%Y%m%d')

#全量备份后删除以前的增量备份
def del_incr_file(dirname):
    filter = ['incr']  # 设置过滤后的文件关键字，以'_'分隔 当然可以设置多个类型
#    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):

        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",file_name_list)  #当前主目录下的所有文件

        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            try:
                os.path.split(apath)[1].split(sep='_', )[1]
            except IndexError:
                pass
                continue
            ext = os.path.split(apath)[1].split(sep='_', )[1]
            if ext in filter:
#                result.append(apath)
                os.remove(apath)


def full_backup(folder,dest,md5file):
    md5_dict = {}
    fname = os.path.basename(folder.rstrip('\\'))
    fname = '%s_full_%s.tar.gz' % (fname, strftime('%Y%m%d'))
    fname = os.path.join(dest,fname)

    tar = tarfile.open(fname,'w:gz')
    tar.add(folder)
    tar.close()

    for path,folder,files in os.walk(folder):
        for file in files:
            key = os.path.join(path,file)
            md5_dict[key] = check_md5(key)
    with open(md5file,'wb') as fobj:
        pickle.dump(md5_dict,fobj)
    del_incr_file(dest)
    del_full_file(dest)

def incr_backup(folder,dest,md5file):
    fname = os.path.basename(folder.rstrip('\\'))
    fname = '%s_incr_%s.tar.gz' % (fname,strftime('%Y%m%d_%H%M%S'))
    fname = os.path.join(dest,fname)
    md5_dict = {}

    for path,folder,files in os.walk(folder):
        for file in files:
            key = os.path.join(path,file)
            md5_dict[key] = check_md5(key)

    with open(md5file,'rb') as fobj:
        oldmd5 =pickle.load(fobj)
    with open(md5file,'wb') as fobj:
        pickle.dump(md5_dict,fobj)
    tar = tarfile.open(fname,'w:gz')
    for key in md5_dict:
        if oldmd5.get(key) !=md5_dict[key]:
            tar.add(key)
    tar.close()

if __name__ == '__main__':
    #要备份的目录
    folder =r'E:\test'
    #备份后的tar包目录
    dest=r'D:\file'
    #备份时记录文件MD5值得目录
    md5file=r'D:\file\md5.data'
    if strftime('%a') == 'Tue':
        full_backup(folder,dest,md5file)
    else:
        incr_backup(folder,dest,md5file)
