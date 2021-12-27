'''
    Chương trình download image từ google
    Lưu ý:
    Mỗi lần chạy thì XÓA thư mục image
'''
from utils import *
from File_Class import *
querys = File_Interact('keyword.txt').read_file_list()
folder = './image'
os.mkdir(folder)  
limit = 40
tryagain = 3
for query in querys:
    download_img_google(query,limit,tryagain)