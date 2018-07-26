# --*-- coding:utf-8 --*--

title = '''
========================================================
+        Download Fasta format file from pdbID         +
+   Recept a txt format file with pdbID line by line   +
========================================================
'''
mode_string = '''
==============================================
+   Select a mode, just change the number:   +
+   1 all(Download chain A and chain B)      +
+   2 some(Download only chain A)            +
+   3 clear(Simplify header information)     +
+   4 quit(Do not download)                  +
==============================================
'''

import os
import sys
from urllib import request


__author__ = 'Wei'
__date__ = '2018-07-25'
__mail__ = 'hanwei@shanghaitech.edu.cn'


#get html from PDBID
class Get_HTML():
	def __init__(self, file_in, file_fold):
		self.file_in = file_in
		self.file_fold = file_fold
	
	#build a new folder, and get id list
	def change_fold(self):
		#if file_in not exist, try again 
		while True:
			try:
				pdbID = open(self.file_in, 'r')
				break
			except FileNotFoundError as e:
				self.file_in = input('%s not exist! try again: ' 
									 % self.file_in)
		pdb_list = pdbID.readlines()
		#build a new fold if you need
		if self.file_fold != '':
			try:
				os.mkdir(self.file_fold)
			except FileExistsError as e:
				pass
			finally:
				os.chdir(self.file_fold)
		pdbID.close()
		return(pdb_list)
	
	#download the page
	def get_page(self, id_list):
		for id in id_list:
			url1 = 'https://www.rcsb.org/pdb/download/viewFastaFiles.do?structureIdList='
			url2 = '&compressionType=uncompressed'
			id = id.strip()
			#This is url of the fasta sequence
			url = url1 + id + url2
			html = request.Request(url)
			page = request.urlopen(html).read()
			page = page.decode('utf-8')
			yield(page) #return a generation

			
#select a mode write to outfile
class Write_MODE():
	def __init__(self, mode, page, name):
		self.mode = mode
		self.page = page
		self.name = name
	
	#mode 2, retain chain A
	def retain_A(self):
		page_str = ''
		page_list = self.page.strip().split('>')[1:]
		for sequ in page_list:
			header = sequ.split('\n')[0]
			chain = (header.split(':')[1]).split('|')[0]
			#if chain A it will write to outfile
			if chain =="A":
				page_str += '>' + sequ
		return(page_str)
	
	#mode 3, retain simplify header information, only name
	def simplify_header(self):
		page_str = ''
		page_list = self.page.strip().split('>')[1:]
		for sequ in page_list:
			sequ_list = sequ.split('\n')
			sequ_list[0] = '>' + sequ_list[0].split(':')[0]
			for line in sequ_list:
				page_str += (line + '\n')
		return(page_str)
	
	#write to outfile
	def to_write(self):
		files = open(self.name, 'a')
		if self.mode == 1:
			pass
		elif self.mode == 2:
			self.page = self.retain_A()
		elif self.mode == 3:
			self.page = self.simplify_header()
		else:
			print('Do not download anything')
			sys.exit()
		files.write(self.page)


#main function
def main():
	print(title)
	file_id = input('Place input you txt format file: ')
	fold = input('Now, folder name(Press Enter to not set up): ')
	file_name = input('Now, outfile name: ')
	print(mode_string)
	mode = int(input('The mode number as you want: '))
	Get_html = Get_HTML(file_id, fold)
	pdb_list = Get_html.change_fold()
	page = Get_html.get_page(pdb_list)
	count, num = 1, len(pdb_list)
	for line in page:
		mark = str(count) + '/' + str(num)
		Write_mode = Write_MODE(mode, line, file_name)
		Write_mode.to_write()
		count += 1
		print('\rMode %d to write %s' % (mode, mark), end='')
	
	
if __name__ == '__main__':
	main()
