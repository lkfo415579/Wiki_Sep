def number_file(dir):
	with open(dir) as f:
		return sum(1 for _ in f)
#
def read_wiki_dic():
	n_dic = 'wiki_dic_fake.txt'
	wiki_words = []
	with open(n_dic , 'r') as file:
		run = 0
		for line in file:
			run += 1
			line = line.strip()
			void_line = line.split('|',1)
			wiki_words.append([void_line[0],void_line[1]]);
	print '########Total : %d Words in wiki_dic########' % run
	return wiki_words
	#[en,zh]
#
import re, mmap
#bilingual_words[en,zh]
def PreProRE(word):
	import string
	invalidChars = set(string.punctuation.replace("_", ""))
	#
	inval_list = []
	for char in word:
		if char in invalidChars:
			#print "Invalid"
			inval_list.append(char)
		#else:
			#print "Valid"
		#print char
	for inval_char in inval_list:
		word = word.replace(inval_char,'\\'+inval_char)
		
	return word
		
def RE_search(title,files):
	phrase = '<doc.*?title="'+title+'">(?:[^\n]*(\n+))*?<\/doc>'
	for file_name in files:
		with open(file_name, 'r+') as f:
			data = mmap.mmap(f.fileno(), 0)
			mo = re.search(phrase, data)
			if mo:
				content = mo.group()
				print file_name
				break
	try:
		return content
	except:
		return False
	#when it gets first one , it will be stooped.
	
found = 0
def search(bi_word,f_en,f_zh):
	zh = bi_word[1]
	en = bi_word[0]
	
	#preprocessing for both words
	en = PreProRE(en)
	zh = PreProRE(zh)
	#
	#first scan en
	#phrase = 'title="'+en+'"'
	en_content = RE_search(en,f_en)
	#second scan zh
	zh_content = RE_search(zh,f_zh)
	global found
	
	if en_content and zh_content:
		print 'Found!No:%d' % found
		found += 1
		return [en_content,zh_content]
	else:
		print 'Not Found!'
				
def read_wiki(Output_Name,Zh_input_folder,En_input_folder):
	print '########Reading Wiki' + ' From file "' + Zh_input_folder + ',' +En_input_folder+'"###########'
	
	from os import walk
	f_zh = []
	for (dirpath, dirnames, filenames) in walk(Zh_input_folder):
		f_zh.extend(filenames)
		break
	##
	f_en = []
	for (dirpath, dirnames, filenames) in walk(En_input_folder):
		f_en.extend(filenames)
		break
	
	#insert folder path into two path vars
	f_zh = [Zh_input_folder+'/'+element for element in f_zh]
	f_en = [En_input_folder+'/'+element for element in f_en]
	#
	output_zh = open(Output_Name+'.zh', "wa")
	output_en = open(Output_Name+'.en', "wa")
	
	wiki_words = read_wiki_dic()
	#finished read wiki_dic
	print '###Starting scan page from meta-data###'
	
	for bi_word in wiki_words:
		print 'Next Word!\n[%s,%s]' % (bi_word[0],bi_word[1])
		contents = search(bi_word,f_en,f_zh)
		print '---------------'
		#write into file
		if contents:
			en_line = contents[0]
			zh_line = contents[1]
			output_en.write(en_line)
			output_zh.write(zh_line)
	
	
	#close I/O files
	output_zh.close()
	output_en.close()
	
		
	print '########End###########'
	return 1
#
def wiki_sep():
	import sys
	import uniout
	
	if len(sys.argv) != 4:
		print 'Usage: python', sys.argv[0], 'Zh-input-folder' , 'En-input-folder' ,'Output-Name'
		exit()
	Zh_input_folder = sys.argv[1]
	En_input_folder = sys.argv[2]
	Output_Name = sys.argv[3]
	read_wiki(Output_Name,Zh_input_folder,En_input_folder)

if __name__ == "__main__":
	wiki_sep()