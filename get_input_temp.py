# -*- coding: utf-8 -*-

# Python2.X encoding wrapper
import codecs,sys,os,glob
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def main(target):
	snt = []
	files = glob.glob(r'/Users/piranon/Documents/corpus/bnc/raw/*')
	for f in files:
		with codecs.open(f, 'r', 'utf-8') as f1:
			snt.extend(['%s.\n' %l for l in f1.read().split('.')[3:] if target in l.split(' ')])
	print len(snt)

	with codecs.open('input/%s.input.txt' %target, 'w', 'utf-8') as f1:
		f1.writelines(snt)

if __name__ == '__main__':
	main(u'observe')