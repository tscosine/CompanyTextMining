import jieba as jb
import yaml

if __name__ == '__main__':
	with open('./config.yml') as f:
		cf = yaml.load(f.read())
	seg_list = jb.cut("我来到北京清华大学", cut_all=cf['cut_all'])
	for seg in seg_list:
		print(seg)