# * coding: utf8 *

# Python2.X encoding wrapper
import codecs,sys,subprocess
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
import networkx as nx
import pygraphviz as pgv
import pydot
import re, pprint
from collections import Counter, defaultdict
global parent, root
parent = 0
flag_0 = 0
G = nx.DiGraph()
global countt
countt = 1

class Node:
	"""
	木のクラス：左右の子と自分自身のデータを持つ
	"""
	def __init__(self, data):
		"""
		木構造
		"""
		self.data = data
		self.left = None
		self.right = None
		self.parent = None

	def search_parent0_2(self):
		"""インスタンス変数"parent"を実装後に作った関数、大量入力に対応"""
		if self.parent[1] == 1:
			global parent
			parent = self.parent[0]
			return
		elif self.parent[0] == root:
			global flag_0
			flag_0 = 1
			global parent
			parent = self
			return
		self.parent[0].search_parent0_2()
		return

	def make_digraph(self):
		global root
		root = self
		self.bdd_to_digraph()

	def bdd_to_digraph(self):
		node_name = "%s//%s" %(self, self.data)
		if self.left:
			left_name = "%s//%s" %(self.left, self.left.data)
			if not self.left.data == '0':
				# if self.left.data == '1':
				# 	G.add_node(node_name, label = self.data)
				# 	G.add_edge(node_name, '1', label = 0)
				# el
				if self == root:
					G.add_node(node_name, label = self.data)
					G.add_node(left_name, label = self.left.data)
					G.add_edge(node_name, left_name, label = 0)
				else:
					self.search_parent0_2()		#0枝でなくなるまで親を探す
					parent_name = "%s//%s" %(parent, parent.data)
					if self.left.data == '1':
						left_name = '1'
					else:
						G.add_node(left_name, label = self.left.data)
					if flag_0 == 1: 
						G.add_edge(parent_name, left_name, label = 0)
						global flag_0
						flag_0 = 0
					else:
						G.add_edge(parent_name, left_name, label = 0, color = 'red')
				self.left.bdd_to_digraph()

		if self.right:
			right_name = "%s//%s" %(self.right, self.right.data)
			if self.right:
				if self.right.data == '1':
					G.add_node(node_name, label = self.data)
					G.add_edge(node_name, '1', label = 0, color = 'red')
				else:
					G.add_node(node_name, label = self.data)
					G.add_node(right_name, label = self.right.data)
					G.add_edge(node_name, right_name, label = 0, color = 'red')
			self.right.bdd_to_digraph()

	# def rank_a(self, S):
	# 	j = 0
	# 	label = '%s//%s'
	# 	S_word = [x[0] for x in S]
	# 	S_tag = ["%s(%s)" %(x[1],x[2]) for x in S]
	# 	all_paths = list(nx.all_simple_paths(G, label %(root, root.data), '1'))
	# 	pattern = re.compile(r'\(.*?\)')
	# 	for p in all_paths:
	# 		path = [u'(0)']
	# 		for node in p[:-1]:
	# 			node = node.split('//')[1]
	# 			path_dist = pattern.search(path[-1]).group()
	# 			node_dist = pattern.search(node).group()
	# 			if path_dist == node_dist:
	# 				path.pop(-1)
	# 			if int(path_dist[1:-1]) + 1 == int(node_dist[1:-1]) or path == []:
	# 				path.append(node)
	# 		if S_tag == path:
	# 			for i in range(len(p)-1):
	# 				edge = G.edge[p[i]][p[i+1]]
	# 				edge['label'] = edge['label'] + 1
	# 				if edge.has_key('color'):
	# 					G.node[p[i]]['label'] += '\n' + S_word[j]
	# 					j += 1
	# 			return 0

	# def rank_b(self, S, mode):
	# 	j = 0
	# 	label = '%s//%s'
	# 	S_word = [x[0] for x in S]
	# 	S_tag = ["%s(%s)" %(x[1],x[2]) for x in S]
	# 	all_paths = list(nx.all_simple_paths(G, label %(root, root.data), '1'))
	# 	pattern = re.compile(r'\(.*?\)')
	# 	for pa in all_paths:
	# 		pa.reverse()
	# 		pa.pop(0)
	# 	S_tag.reverse()
	# 	S_word.reverse()
	# 	# print '-'*100 , '\n', pp(S_tag), '\n','*'*100
	# 	for p in all_paths:
	# 		path = [u'(0)']
	# 		for node in p:
	# 			node = node.split('//')[1]
	# 			path_dist = pattern.search(path[-1]).group()
	# 			node_dist = pattern.search(node).group()
	# 			if path_dist == node_dist:
	# 				path.pop(-1)
	# 			if int(path_dist[1:-1]) + 1 == int(node_dist[1:-1]) or path == []:
	# 				path.append(node)
	# 		# print pp(path)
	# 		if S_tag == path:
	# 			# print pp(path)
	# 			# print 'test'
	# 			# print pp(p)
	# 			for i in range(len(p)-1):
	# 				# print p[i]
	# 				if mode == 'a':
	# 					edge = G.edge[p[i]][p[i+1]]
	# 				else:
	# 					edge = G.edge[p[i+1]][p[i]]
	# 				# print edge
	# 				edge['label'] = edge['label'] + 1
	# 				if edge.has_key('color'):
	# 					G.node[p[i]]['label'] += '\n' + S_word[j]
	# 					j += 1
	# 			return 0
	# 	# print 'Error'

	def rank_b(self, S, node = None):
		if not node:
			node = root
		node_name = '%s//%s' %(node, node.data)
		# left_name = '%s//%s' %(node.left, node.left.data)
		word = '%s(%s)' %(S[0][1],S[0][2])
		print G.node[node_name]['label'].split('\n')[0], word
		if G.node[node_name]['label'].split('\n')[0] == word:
			if not node.right.data == '1':
				G.node[node_name]['label'] += '\n' + S[0][0]
				G[node_name]['%s//%s' %(node.right, node.right.data)]['label'] += 1
				self.right.rank_b(S[1:], node.right)
			else:
				G.node[node_name]['label'] += '\n' + S[0][0]
				G[node_name]['1']['label'] += 1
		else:
			self.left.rank_b(S, node.left)

	def rank(self, S, node = None):
		if not node:
			node = root
		node_name = '%s//%s' %(node, node.data)
		try:
			left_name = '%s//%s' %(node.left, node.left.data)
			word = '%s(%s)' %(S[0][1],S[0][2])
			if G.node[node_name]['label'].split('\n')[0] == word:
				if not node.right.data == '1':
					G.node[node_name]['label'] += '\n' + S[0][0]
					G[node_name]['%s//%s' %(node.right, node.right.data)]['label'] += 1
					self.right.rank(S[1:], node.right)
				else:
					G.node[node_name]['label'] += '\n' + S[0][0]
					G[node_name]['1']['label'] += 1
			elif node == root:
				G[node_name][left_name]['label'] += 1
				self.left.rank(S, node.left)
			elif node.left.data == '0':
				pass
			elif G.node[left_name]['label'].split('\n')[0] == word:
				self.search_parent0_2()
				parent_name = "%s//%s" %(parent, parent.data)
				G[parent_name][left_name]['label'] += 1
				if flag_0 == 1:
					G[parent_name]["%s//%s" %(parent.left, parent.left.data)]['label'] -= 1
					global flag_0
					flag_0 = 0
				else:
					G[parent_name]["%s//%s" %(parent.right, parent.right.data)]['label'] -= 1
				self.left.rank(S, node.left)
			else:
				self.left.rank(S, node.left)
		except IndexError:
			# print 'IndexError', countt
			# global countt
			# countt += 1
			pass

	def remove_rank1(self):
		for edge in G.edges():
			if  G[edge[0]][edge[1]]['label'] <= 1:
				G.remove_edge(edge[0],edge[1])
			elif not G[edge[0]][edge[1]].has_key('color'):
				G.remove_edge(edge[0],edge[1])
		for node in G.nodes():
			if G[node] == {} and not node == '1':
				G.remove_node(node)
		if G.predecessors('1') == []:
			G.remove_node('1')
		# print 'nodes:',G.number_of_nodes()
		# print 'edges:',G.number_of_edges()

	def node_comp(self, query):
		for n in G.nodes():
			if not n == '1':
				labels = G.node[n]['label'].split('\n')
				tag, cnt = labels[0], Counter(labels[1:])
				# if float(cnt.most_common(1)[0][1])/sum(cnt.values()) == 1:
				if cnt.most_common(1)[0][0] == query:
					G.node[n]['label'] = (u"%s" %tag + r'\n' + "%s" %cnt.most_common(1)[0][0])
					G.node[n]['shape'], G.node[n]['fontcolor'] = 'doublecircle', 'red'
				else:		#ノード圧縮なしでいい気がする
					G.node[n]['label'] = tag + r'\n'
					for c in cnt.most_common():
						G.node[n]['label'] += r'%s:%d\n' %(c[0],c[1])


	def get_patterns_b(self):
		roots = []
		for n in G.nodes():
			if not nx.has_path(G, n, '1'):
				G.remove_node(n)
		# for n in nx.ancestors(G, '1'):
			elif G.predecessors(n) == []:
				roots.append(n)
		if roots == []:
			print '\n******No Pattern******\n'
		else:
			print '\n******Patterns******\n'
			print '\nExtracted Pattern <%i>' %len(roots)
		i = 0
		Ext_Patterns = []
		for n in roots:
			pattern = []
			if nx.has_path(G, n, '1'):
				for p in nx.dijkstra_path(G, n, '1')[:-1]:
					if G.node[p].has_key('fontcolor'):
						pattern.append(G.node[p]['label'].split(r'\n')[1])
					else:
						label = G.node[p]['label'].split(r'\n')[:-1]
						pattern.append('%s:{%s}' %(label[0].split('(')[0], ', '.join(label[1:])))
			# print '%d:' %i, u'//'.join(pattern)
			Ext_Patterns.append(u'//'.join(pattern))
			i += 1
		return Ext_Patterns

	def get_patterns_a(self, snts, query):
		leaves = []
		root_name = "%s//%s" %(root, root.data)
		for n in G.nodes():
			if not nx.has_path(G, root_name, n):
				G.remove_node(n)
		# for n in nx.descendants(G, root_name):
			elif n == '1':
				pass
			elif G.successors(n) == [] or G.successors(n) == ['1']:
				leaves.append(n)
		# if leaves == []:
		# 	print '\n******No Pattern******\n'
		# else:
		# 	print '\n******Patterns******\n'
		# 	print '\nExtracted Pattern <%i>' %len(leaves)
		p_path = []
		for path in [nx.dijkstra_path(G, root_name, n) for n in leaves]:
			p_path.append([p.split(u'//')[1][:-3] for p in path[1:]])

		#入力文章を振り分ける
		snt_divide = defaultdict(list)
		prop_p = defaultdict(list)	#ここも
		for s in snts:
			temp_p = (-1, "")
			before_t = sum([s[:i] for i, x in enumerate(s) if x[0] == query], [])
			after_t = sum([s[i+1:] for i, x in enumerate(s) if x[0] == query], [])
			if after_t == [] or before_t == []:
				pass
			else:
				after_POS = [x[1] for x in after_t]

				for i, p in enumerate(p_path):
					if len(p) > len(after_POS):
						continue
					elif p == after_POS[:len(p)] and len(temp_p[1]) < len(p):
						temp_p = i, p

				# print temp_p, after_POS		#ちょっと未定の調整箇所
				
				if temp_p[0] == -1:
					prop_p['-'.join(after_POS)].append(before_t)
				else:
					snt_divide[temp_p[0]].append(before_t)

		for key in prop_p.keys():
			if len(prop_p[key]) <= 1:
				del prop_p[key]

		# pprint.pprint(prop_p)


		i = 0
		Ext_Patterns = []
		for n in leaves:
			pattern = []
			if nx.has_path(G, root_name, n):
				for p in nx.dijkstra_path(G, root_name, n):
					if G.node[p].has_key('fontcolor'):
						pattern.append(G.node[p]['label'].split(r'\n')[1])
					elif G.node[p] == {}:
						pass
					else:
						label = G.node[p]['label'].split(r'\n')[:-1]
						pattern.append('<%s>:{%s}' %(label[0].split('(')[0], ', '.join(label[1:])))
			# print '%d:' %i, u'//'.join(pattern)
			Ext_Patterns.append(u'//'.join(pattern))

			i += 1

		# for i in range(len(Ext_Patterns)):
			# print Ext_Patterns[i], snt_divide[i]


		#あふれた文章をパターンとして取り直す
		temp_index = len(Ext_Patterns)
		for k, v in prop_p.items():
			pattern = []
			key = ['%s(%s)' %(k, i+1) for i, k in enumerate(k.split('-'))]
			for path in nx.single_source_dijkstra_path(G, root_name).values():
				path_POS = [p.split('//')[1] for p in path[1:] if not p == '1']
				if path_POS == key:
					for p in path:
						if G.node[p].has_key('fontcolor'):
							pattern.append(G.node[p]['label'].split(r'\n')[1])
						elif G.node[p] == {}:
							pass
						else:
							label = G.node[p]['label'].split(r'\n')[:-1]
							pattern.append('<%s>:{%s}' %(label[0].split('(')[0], ', '.join(label[1:])))
					break
			Ext_Patterns.append(u'//'.join(pattern))
			snt_divide[temp_index].extend(v)
			temp_index += 1
		return snt_divide, Ext_Patterns



	def draw_graph(self, name, mode):
		g = nx.to_agraph(G)
		# g.write("dot/test.dot")
		# file_n = name.split('.')[-2]
		g.draw("img/%s_%s.png" %(name, mode), prog='dot')

	def test_print(self):
		if self.left:
			self.left.test_print()
		print self.data
		if self.right:
			self.right.test_print()

	def reset_graph(self):
		G.clear()
		

def pp(obj):
  pp = pprint.PrettyPrinter(indent=4, width=160)
  str = pp.pformat(obj)
  return re.sub(r"\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)
