#-*-coding:utf-8-*-
import os
import re
import xlwt

if __name__ == "__main__":
    pattern   = re.compile('(.+)_(\d+).txt')
    text_path = './text'
    row = 0
    workbook = xlwt.Workbook(encoding = 'ascii')
    sheet = workbook.add_sheet('Sheet1')

    for txt in os.listdir(text_path):
        name  = re.search(pattern,txt).group(1)
        uname = name.decode('utf-8')
        year  = re.search(pattern,txt).group(2)
        file  = open(os.path.join(text_path,txt)).read().decode('utf-8')
        flag  = False
        push_pattern = re.compile('^'+uname+'：'.decode('utf-8'))
        pop_pattern = re.compile('^.*'+'：'.decode('utf-8'))
        for para in file.split('\n'):
            if len(para) > 0:
                if re.match(push_pattern,para):
                    flag = True
                    print('-------------------')
                    print(para)
                    sheet.write(row, 0, uname)
                    sheet.write(row, 1, year)
                    sheet.write(row, 2, para)
                    row += 1
                elif re.match(pop_pattern,para):
                    flag = False
                elif flag == True:
                    print(para)
                    sheet.write(row, 0, uname)
                    sheet.write(row, 1, year)
                    sheet.write(row, 2, para)
                    row += 1

    workbook.save('mix.xls')