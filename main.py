# -*- coding: utf-8 -*-

# Python2.X encoding wrapper
import codecs,sys,MeCab,copy,time, re, pickle
# import nltk
import pprint, json, corenlp
reload(sys)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.setdefaultencoding('utf-8')
print "defaultencoding : ", sys.getdefaultencoding()

from node import *
cache = {}

def getnode(data, left, right, f0, f1):
	if right.data == '0':
		return left
	elif cache.has_key("<%s,%s,%s>" % (data, f0, f1)):
		# print "cache exist\n"
		return cache["<%s,%s,%s>" % (data, f0, f1)]
	
	new_node = Node('%s(%s)' %(data[0], data[1]))
	new_node.left = left
	new_node.right = right
	left.parent = (new_node, 0)
	right.parent = (new_node, 1)
	cache["<%s,%s,%s>" %(data, f0, f1)] = new_node

	return new_node

def seqbdd(f):
	
	f.sort()
	f0 = []
	f1 = []
	if f == [[]]:	
		return Node('1')
	if f == []:		
		return Node('0')
	if f[0] == []:
		del f[0]
	x = f[0][0]

	for i in range(len(f)):
		if f[i][0] == x:
			f1.append(f[i][1:])
		else:
			f0.append(f[i][:])

	r  = getnode(x, seqbdd(f0), seqbdd(f1), f0, f1)
	return r



	#Parser3種類	

def core_nlp_parser(file, query):
	corenlp_dir = "/Users/piranon/Documents/StanfordParser/stanford-corenlp-full-2013-06-20"
	properties_file = "./user.properties"
	parser = corenlp.StanfordCoreNLP(
		corenlp_path = corenlp_dir,
		properties = properties_file)
	tagged = []
	with codecs.open(file, 'r', 'utf-8') as f:
		snt = f.readlines()
	snt = list(set(snt))
	for i, line in enumerate(snt):
		if len(line) > 400:
			continue
		elif u'!' in line or u'?' in line:
			continue
		line = line.strip()
		line_tagged = []
		result_nlp = json.loads(parser.parse(line))
		dependencies = [d for d in result_nlp[u'sentences'][0][u'indexeddependencies'][:]]
		for i, d in enumerate(dependencies):
			dependencies[i] = {
				'tag'  : d[0],
				'w1'   : d[1].split(u'-')[0],
				'w1_i' : d[1].split(u'-')[1],
				'w2'   : d[2].split(u'-')[0],
				'w2_i' : d[2].split(u'-')[1]
				}
		for d in dependencies:
			if d['w1'] == query:
				del d['w1']
				query_index = int(d.pop('w1_i'))
				try:
					d['index'] = int(d.pop('w2_i'))
					d['word'] = d.pop('w2')
				except ValueError:
					d.clear()
			elif d['w2'] == query:
				del d['w2']
				query_index = int(d.pop('w2_i'))
				try:
					d['word'] = d.pop('w1')
					d['index'] = int(d.pop('w1_i'))
				except ValueError:
					d.clear()
			else:
				d.clear()
		while dependencies.count({}) > 0:
			dependencies.remove({})

		lemmas = [x[1]['Lemma'] for x in result_nlp[u'sentences'][0][u'words']]
		dependencies.append({'tag':'TARGET', 'word':query, 'index':query_index})
		print lemmas

		for dic in sorted(dependencies, key=lambda x: x['index']):
			print dic
			if dic['word'] == query:
				print lemmas[dic['index']-1], 'TARGET'
				line_tagged.append((lemmas[dic['index']-1], 'TARGET'))
			else:
				print lemmas[dic['index']-1], dic['tag']
				line_tagged.append((lemmas[dic['index']-1], dic['tag']))

		# for i, w in enumerate([x[1]['Lemma'] for x in result_nlp[u'sentences'][0][u'words']]):
		# 	if w == query:
		# 		line_tagged.append((w, 'TARGET'))
		# 		continue
		# 	for d in dependencies:
		# 		if w in d:
		# 			line_tagged.append((w, d[0]))
		# 			break
		# 	else:
		# 		#文章全部をPOSで入力するとき
		# 		# line_tagged.append((w, result_nlp[u'sentences'][0][u'words'][i][1][u'PartOfSpeech']))

		# 		#TARGET動詞との関係がある単語のみのとき
		# 		pass
		tagged.append(line_tagged)
	return tagged

def nltk_tagger(file):
	f = codecs.open(file, 'r', 'utf-8')
	word_tagged = []
	for line in f.readlines():
		line = nltk.word_tokenize(line)
		word_tagged.append(nltk.pos_tag(line))
	f.close()
	return word_tagged

def mecab_tagger(file):
	tagger = MeCab.Tagger('-Ochasen')
	f = codecs.open(file)
	tagged = []
	lines = list(set(f.readlines()))
	f.close()
	for line in lines:
		# enc = line.encode('utf-8')
		node = tagger.parseToNode(line)
		line_tagged = []
		while node:
			if node.feature.split(",")[1] == "格助詞":
				line_tagged.append((u"%s" %node.surface, "%s" %(node.feature.split(",")[7] + node.feature.split(",")[1])))
			elif node.feature.split(",")[1] != "*":
				if node.feature.split(",")[0] in node.feature.split(",")[1]:
					line_tagged.append((u"%s" %node.surface, "%s" %node.feature.split(",")[1]))
				else:
					line_tagged.append((u"%s" %node.surface, "%s%s" %(node.feature.split(",")[1], node.feature.split(",")[0]))) 
			else:
				line_tagged.append((u"%s" %node.surface, "%s" %node.feature.split(",")[0]))
			node = node.next
		tagged.append(line_tagged[1:-1])
	return tagged

def KNP_tagger(file):
	knp = pyknp.KNP()
	tagged = []
	with codecs.open(file, 'r', 'utf-8') as f:
		lines = f.readlines()
	lines = list(set(lines))
	for line in lines:
		line_tagged = []
		result = knp.parse(u"%s" %line.strip())
		for mrph in result.mrph_list():
			if mrph.bunrui == '格助詞':
				line_tagged.append([mrph.midasi, u"%s%s" %(mrph.genkei, mrph.bunrui)])
			elif not mrph.bunrui == '*':
				line_tagged.append([mrph.midasi, mrph.bunrui])
			else:
				line_tagged.append([mrph.midasi, mrph.hinsi])
		for x in result.tag_list()[-1].fstring.split(u':'):
			if u"動" in x and len(x) < 3:
				line_tagged[-1][1] += u"(%s)" %x
				break
		tagged.append(line_tagged)
	return tagged

def numbering(sentences, mode):
	for words in sentences:
		for i in range(len(words)):
			words[i] = list(words[i])
			if words[i][1] == ':':
				words[i][1] = 'ETC'
			if mode == 'a':
				words[i].append(u'%s' %i)
			else:
				words[i].append(u'%s' %(len(words) - i - 1))
	return sentences

def remove_word(sentences):
	for words in sentences:
		for w in words:
			del w[0]
	return sentences

def set_list(nest):
	temp = []
	for words in nest:
		if words not in temp:
			temp.append(words)
	return temp

def pickle_write(obj, name):
	with open('./pickle/%s.pickle' %name, 'w') as f:
			pickle.dump(obj, f)

def pickle_load(name):
	with open('./pickle/%s.pickle' %name, 'r') as f:
			return pickle.load(f)

def reset():
	global cache
	cache = {}
	after_tree = None
	before_tree = None

def main(fn):
	"""入力文の整備→SeqBDD作成"""
	# s = time.clock()
	# if mode == 'c':
	# 	word_jp = mecab_tagger(fn)		#入力文をparse
		# word_with_tag = core_nlp_parser(fn, query)
	# else:
	query = u'observe'
		# word_with_tag = nltk_tagger(fn)
	# word_with_tag = core_nlp_parser(fn, query)
		#parseした入力をpickleでファイル出力しておく
	# pickle_write(word_with_tag, 'observe')
	# s = time.clock()
	# 	#pickleファイルを読み込んで、parse済みオブジェクトを取り出し
	word_with_tag = pickle_load('observe')
	# e = time.clock()
	# print "\nREAD PICKLE FILE:%.8f [sec]\n" %(e - s)

	print 'Input text:%d' %len(word_with_tag)

	s = time.clock()
	after_query = []
	for i in range(len(word_with_tag)):
		for j in range(len(word_with_tag[i])):
			if word_with_tag[i][j][0] == query:
				after_query.append(word_with_tag[i][j:])
				# after_query[-1][0] = (query, 'TARGET')

	after_numed = numbering(after_query, 'a')
	# after_numed = numbering(word_jp, 'a')
	# after_numed = numbering(word_with_tag, 'a')

	rank_a = copy.deepcopy(after_numed)
	after = set_list(remove_word(after_numed))
	after_tree = seqbdd(after)
	e = time.clock()
	print "\nMAKE SEQBDD:%.8f [sec]\n" %(e - s)

	s = time.clock()
	#SeqBDDをNetworkXのDiGraphに変換
	after_tree.make_digraph()
	e = time.clock()
	print "\nSEQBDD => DiGraph:%.8f [sec]\n" %(e - s)

	s = time.clock()
	#入力文を使って枝を重み付け&ノードのラベル付け
	for sentence in rank_a:
		after_tree.rank(sentence)
	e = time.clock()
	print "\nLABELED:%.8f [sec]\n" %(e - s)

	s = time.clock()
	#1−枝をすべて削除
	after_tree.remove_rank1()
	e = time.clock()
	print "\nREMOVE 1-EDGES:%.8f [sec]\n" %(e - s)

	s = time.clock()
	#ノードラベルを圧縮
	after_tree.node_comp(query)
	e = time.clock()
	print "\nNODE COMPRESS:%.8f [sec]\n" %(e - s)

	s = time.clock()
	#パターンを抽出
	before_query_list, patterns = after_tree.get_patterns_a(word_with_tag, query)
	e = time.clock()
	print "\nPATTERN EXTRACTED:%.8f [sec]\n" %(e - s)

	#画像ファイルに出力
	after_tree.draw_graph(query+'test', 'a')

	# print '*'*20 ,'FINISH %s' %fn, '*'*20

	after_tree.reset_graph()
	# print '\n~~~~~~~FINISH AFTER PATTERN~~~~~~~~~~\n\n'

	# pickle_write(patterns, query+'_after_patterns')
	# pickle_write(before_query_list, query+'_before_snt_list')

	# patterns = pickle_load(query+'_after_patterns')
	# before_query_list = pickle_load(query+'_before_snt_list')

	print 'sum:', sum([len(x) for x in before_query_list.values()])
	print len(patterns), len(before_query_list)
	# print pp(before_query_list)

	reset()

	all_pattern = []
	for i, before_query in before_query_list.items():
		# print before_query
		# print patterns[i]

		# before_query = []
		# for i in range(len(word_with_tag)):
		# 	for j in range(len(word_with_tag[i])):
		# 		if word_with_tag[i][j][0] == query:
		# 			before_query.append(word_with_tag[i][:j])

		# before_numed = numbering(word_jp, 'b')
		before_numed = numbering(before_query, 'b')
		rank_b = copy.deepcopy(before_numed)
		before = set_list(remove_word(before_numed))
		before_tree = seqbdd(before)

		before_tree.make_digraph()


		#入力文を使って枝を重み付け&ノードのラベル付け
		for j, sentence in enumerate(rank_b):
			# print sentence
			# print i, j
			# if i == 5 and j == 32:
			# 	before_tree.draw_graph(query + 'before_test', 'b')
			before_tree.rank(sentence)

		#1−枝をすべて削除
		before_tree.remove_rank1()

		#ノードラベルを圧縮
		before_tree.node_comp(query)

		#パターンを抽出
		print "***後半パターン***\n\n"

		before_patterns = before_tree.get_patterns_b()
	
		for p in before_patterns:
			all_pattern.append(patterns[i] + u'//' + p + u'\n')

		#画像ファイルに出力
		# s = time.clock()
		# before_tree.draw_graph(query + u'%d' %i, 'b')
		# e = time.clock()
		# print "\nDraw Graph to png-file:%.8f [sec]\n" %(e - s)

		# print '*'*20 ,'FINISH %s\n' %fn, '*'*20

		before_tree.reset_graph()
		reset()

	# print all_pattern
	with codecs.open('%s.full.txt' %query, 'w', 'utf-8') as f:	
		f.writelines(all_pattern)


if __name__ == '__main__':
	# main(sys.argv[1])

	# main('makaseru_long_70.txt', 'b')
	main('input/observe.input.txt')
	# main('input/observe.input.txt', 'b')
	# main('setti_long.txt', 'b')

