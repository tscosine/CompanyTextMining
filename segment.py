# -*- coding: utf-8 -*-

import jieba as jb
import yaml
import os
import xlrd
import numpy as np



class PersonalQouta:
	def __init__(self,name):
		self.name = name
		self.dataset = {'2013':[],'2014':[],'2015':[],
						'2016':[],'2017':[],'2018':[]}
	def add_qouta(self,year,qouta):
		self.dataset[str(int(year))].append(qouta)
	def count(self):
		result = ''
		total = 0
		for key in self.dataset.keys():
			result += key+':'
			result += str(self.dataset[key].__len__())+'\n'
			total += self.dataset[key].__len__()
		result += 'Total:'
		result += str(total)+'\n'
		return result
class DataSet:
	target_name = ['马化腾', '马云', '李彦宏', '丁磊', '张朝阳',
				   '周鸿祎', '刘强东', '王志东', '梁建章', '张近东',
				   '王兴', '沈亚', '莫天全', '雷军', '陈天桥', '李瑜','张勇']
	def __init__(self):
		self.dataset = {}
		for name in self.target_name:
			self.dataset[name] = PersonalQouta(name)
	def readExcelData(self,excel_data):
		for row in excel_data:
			self.dataset[row[0]].add_qouta(row[1],row[2])
	def count(self):
		result = ''
		for name in self.target_name:
			result += name+':'+'\n'
			result += self.dataset[name].count()
			result += '######################\n'
		return result
def loadExcelData(path):
	result = []
	for file in os.listdir(path):
		workbook = xlrd.open_workbook(os.path.join(path,file))
		for sheetname in workbook.sheet_names():
			sheet = workbook.sheet_by_name(sheetname)
			for i in range(sheet.nrows):
				row = sheet.row_values(i)
				result.append(row)
	return result


if __name__ == '__main__':
	with open('./config.yml') as f:
		cf = yaml.load(f.read())
	excel_data = loadExcelData(cf['data_path'])
	dataset = DataSet()
	dataset.readExcelData(excel_data)
	with open('./count.txt','w') as f:
		f.write(dataset.count())
	print(dataset.count())
	# workbook = xlrd.open_workbook('/home/cosine/mygit/weibocrawler/data/1.xls')
	# for sheetname in workbook.sheet_names():
	# 	sheet = workbook.sheet_by_name(sheetname)
	# 	row = sheet.row_values(3)
	# 	print(row)

	# seg_list = jb.cut("我来到北京清华大学", cut_all=cf['cut_all'])
	# for seg in seg_list:
	# 	print(seg)