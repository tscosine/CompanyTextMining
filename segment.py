#-*-coding:utf-8-*-

import jieba.analyse
import yaml
import os
import xlrd
import xlwt

year_list = ['2013','2014','2015','2016','2017','2018']
class PersonalQouta:
	def __init__(self,name):
		self.name = name
		self.dataset = {'2013':[],'2014':[],'2015':[],
						'2016':[],'2017':[],'2018':[]}

	def add_qouta(self,year,qouta):
		self.dataset[str(int(year))].append(qouta)

	def count(self):
		result = []
		total = 0
		for key in year_list:
			result.append(self.dataset[key].__len__())
			total += self.dataset[key].__len__()
		result.append(total)
		return result

	def word_frequency(self):
		result = []
		for key in year_list:
			result_a_year = []
			content = ''.join(self.dataset[key])
			allowPOS = ('n','v')
			jieba.analyse.set_stop_words("./stopwords.txt")
			topk_word = jieba.analyse.extract_tags(content,withWeight=True,
				topK=config['Topk'],allowPOS=allowPOS)
			for word in topk_word:
				# result_a_year.append([word[0],':%.2f\n'%word[1]])
				result_a_year.append(word[0:2])
			result.append(result_a_year)
		return result

	def get_content(self,year):
		return ''.join(self.dataset[year])


class DataSet:
	target_name = [u'马化腾', u'马云', u'李彦宏', u'丁磊', u'张朝阳',
				   u'周鸿祎', u'刘强东', u'王志东', u'梁建章', u'张近东',
				   u'王兴', u'沈亚', u'莫天全', u'雷军', u'陈天桥', u'李瑜',u'张勇',u'齐向东']
	def __init__(self):
		self.dataset = {}
		for name in self.target_name:
			self.dataset[name] = PersonalQouta(name)

	def readExcelData(self,excel_data):
		for row in excel_data:
			self.dataset[row[0]].add_qouta(row[1],row[2])

	def count(self):
		result = {}
		for name in self.target_name:
			result[name] = self.dataset[name].count()
		return result

	def word_frequency(self):
		result = {}
		for name in self.target_name:
			result[name] = self.dataset[name].word_frequency()
		return result

	def all_word_frequency(self):
		result  = []
		for year in year_list:
			result_a_year = []
			content = ''
			for name in self.target_name:
				content += self.dataset[name].get_content(year)
			allowPOS = ('n', 'v')
			jieba.analyse.set_stop_words("./stopwords.txt")
			topk_word = jieba.analyse.extract_tags(
				content, withWeight=True,topK=config['Topk'], allowPOS=allowPOS)
			for word in topk_word:
				result_a_year.append(word[0:2])
			result.append(result_a_year)
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

	workbook = xlwt.Workbook(encoding = 'utf-8')
	worksheet_count = workbook.add_sheet('count')
	worksheet_frequency = workbook.add_sheet('frequency')
	worksheet_frequency_by_year = workbook.add_sheet('frequency_annual')

	count_dict = dataset.count()
	row = 0
	column = 0
	for key in count_dict.keys():
		worksheet_count.write(row,column,key)
		column += 1
		for c in count_dict[key]:
			worksheet_count.write(row, column, c)
			column +=1
		row += 1
		column = 0

	word_frequency_dict = dataset.word_frequency()
	row = 0
	column = 0
	for key in word_frequency_dict.keys():
		worksheet_frequency.write(row,column,key)
		column += 1
		for year in year_list:
			worksheet_frequency.write(row, column, year)
			row += 2
		row -= 2*len(year_list)
		for frequency_list in word_frequency_dict[key]:
			column = 2
			for tuple in frequency_list:
				worksheet_frequency.write(row, column, tuple[0])
				worksheet_frequency.write(row+1, column, ':%.2f\n' % tuple[1])
				column += 1
			row += 2

		column = 0
		row += 1

	annual_word_frequency_list = dataset.all_word_frequency()
	row = 0
	column = 0
	for year in year_list:
		worksheet_frequency_by_year.write(row,column,year)
		row += 2
	row = 0
	for annual_list in annual_word_frequency_list:
		column = 1
		for tuple in annual_list:
			worksheet_frequency_by_year.write(row, column, tuple[0])
			worksheet_frequency_by_year.write(row + 1, column, ':%.2f\n' % tuple[1])
			column += 1
		row += 2

	workbook.save('./Excel_Workbook.xls')