#-*-coding:utf-8-*-
import os
import re
import xlwt
import codecs
if __name__ == "__main__":
    # pattern   = re.compile('(.+)(_|-)(\d+).*.txt')
    pattern   = re.compile('_(\d+)(_|.)')
    text_path = './text'
    row = 0
    workbook = xlwt.Workbook(encoding = 'ascii')
    sheet = workbook.add_sheet('Sheet1')
    textcount = {}

    for txt in os.listdir(text_path):
        # if txt != '张朝阳_2015(2).txt':
        #     continue
        print(txt)
        count = 0
        # name  = re.search(pattern,txt).group(1)

        uname = u'李瑜'

        year  = re.search(pattern,txt).group(1)
        print(year)
        file  = codecs.open(os.path.join(text_path,txt),encoding='utf-8').read()
        flag  = False
        say_word    = u'：'+'|'+':'+'|'+u'指出'+'|'+u'表示'+'|'+u'认为'+\
                      '|'+u'说'+'|'+u'告诉'+'|'+u'提到'+'|'+u'坦言'+\
                      '|'+u'宣布'+'|'+u'看来'+'|'+u'直言'+'|'+u'预测'+'|'+u'暗示'+'|'+u'以为'+'|'+u'说道'+'|'+u'强调'+'|'+u'看来'
        push_pattern= re.compile('\s*'+uname+'('+say_word+')')
        pop_pattern = re.compile('^.{0,10}'+u'：')
        for para in file.split('\n'):
            # print(para)
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
            # print(flag)
        textcount[txt] = count
    for record in textcount.items():
        if record[1] < 2:
            print(record[0])
            print(record[1])
    workbook.save('mix.xls')
