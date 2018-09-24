#-*-coding:utf-8-*-
import os
import re
import xlwt

if __name__ == "__main__":
    pattern   = re.compile('(.+)(_|-)(\d+).*.txt')
    text_path = './text'
    row = 0
    workbook = xlwt.Workbook(encoding = 'ascii')
    sheet = workbook.add_sheet('Sheet1')
    textcount = {}

    for txt in os.listdir(text_path):
        # if txt != '马化腾-2015（8）.txt':
        #     continue
        print(txt)
        count = 0
        name  = re.search(pattern,txt).group(1)
        uname = name.decode('utf-8')
        year  = re.search(pattern,txt).group(3)
        file  = open(os.path.join(text_path,txt)).read().decode('utf-8')
        flag  = False
        say_word    = u'：'+'|'+u'指出'+'|'+u'表示'+'|'+u'认为'+'|'+u'说'+u'告诉'+u'提到'
        push_pattern= re.compile('\s*'+uname+'('+say_word+')')
        pop_pattern = re.compile('^.{0,10}'+u'：')
        for para in file.split('\n'):
            if len(para) > 0:
                if re.match(push_pattern,para):
                    flag = True
                    if len(para) > 20:
                        print('-------------------')
                        print(para)
                        sheet.write(row, 0, uname)
                        sheet.write(row, 1, year)
                        sheet.write(row, 2, para)
                        row += 1
                        count += 1
                elif re.match(pop_pattern,para):
                    flag = False
                elif flag == True:
                    if len(para) > 20:
                        print(para)
                        sheet.write(row, 0, uname)
                        sheet.write(row, 1, year)
                        sheet.write(row, 2, para)
                        row += 1
                        count += 1
        textcount[txt] = count
    for record in textcount.items():
        if record[1] < 2:
            print(record[0].decode('utf-8'))
            print(record[1])
    workbook.save('mix.xls')