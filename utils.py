# 读取文件
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()
