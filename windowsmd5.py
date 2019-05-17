# -*- encoding:utf-8 -*-
import hashlib
import os
def GetFileMd5(fname):
    m = hashlib.md5()
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()
if __name__ == '__main__':
    filename = input(r'请输入文件绝对路径+文件名或把文件拉到python3对话框：')
    while filename !='q':
        if os.path.isfile(filename) is True:
            try:
                f=open(filename,'r')
                f.close()
            except (PermissionError):
                print('该文件没有读取权限，若要执行请作出以下修改“单击右键->属性->安全->编辑->读取拒绝框中去掉√”')
                filename = input(r'请重新输入文件绝对路径+文件名或把文件拉到python3对话框：')
                continue
            print( '该文件的md5值为： %s' % (GetFileMd5(filename)))
            filename =input(r'请输入下一个文件绝对路径+文件名或把文件拉到python3对话框(输入q退出)：')
        else:
            print('找不到文件或文件绝对路径+文件名中存在空格等特殊字符不被识别')
            filename =input(r'请重新输入下一个文件绝对路径+文件名或把文件拉到python3对话框(输入q退出)：')
