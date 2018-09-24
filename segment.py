#-*-coding:utf-8-*-

import jieba.analyse
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

	def word_frequency(self):
		with open('./config.yml','r') as f:
			config = yaml.load(f.read())
		result = ''
		for key in self.dataset.keys():
			result += key + ':'+'\n'
			content = ''.join(self.dataset[key])
			allowPOS = ('n','v')
			jieba.analyse.set_stop_words("./stopwords.txt")
			if config['withWeight']:
				topk_word = jieba.analyse.extract_tags(content,withWeight=True,
					topK=config['Topk'],allowPOS=allowPOS)
				for word in topk_word:
					result += word[0]+':'+str(word[1])+'\n'
			else:
				topk_word = jieba.analyse.extract_tags(content,withWeight=False,
					topK=config['Topk'],allowPOS=allowPOS)
				result += ' '.join(topk_word)
				result += '\n'
		return result


class animal:
	def __init__(self):
		pass
	def barking(self):
		print('wangwangwang!!!')

class DataSet:
	target_name = [u'马化腾', u'马云', u'李彦宏', u'丁磊', u'张朝阳',
				   u'周鸿祎', u'刘强东', u'王志东', u'梁建章', u'张近东',
				   u'王兴', u'沈亚', u'莫天全', u'雷军', u'陈天桥', u'李瑜',u'张勇']
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

	def word_frequency(self):
		result = ''
		for name in self.target_name:
			result += name + ':' + '\n'
			result += self.dataset[name].word_frequency()
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
		config = yaml.load(f.read())
	excel_data = loadExcelData(config['data_path'])
	dataset = DataSet()
	dataset.readExcelData(excel_data)

	with open(config['count_path'],'w') as f:
		str = dataset.count()
		f.write(str)

	with open(config['output_path'],'w') as f:
		str = dataset.word_frequency()
		f.write(str)