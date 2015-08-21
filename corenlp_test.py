# -*- coding: utf-8 -*-

# Python2.X encoding wrapper
import codecs,sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

import pprint, json, corenlp

corenlp_dir = "/Users/piranon/Documents/StanfordParser/stanford-corenlp-full-2013-06-20"
properties_file = "./user.properties"
parser = corenlp.StanfordCoreNLP(
	corenlp_path=corenlp_dir,
	properties = properties_file)

result_json = json.loads(parser.parse('He could observe the results at the same time'))
pprint.pprint(result_json)
pprint.pprint(result_json[u'sentences'][0])