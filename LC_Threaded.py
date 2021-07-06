import os, sys, ctypes, argparse, time, codecs
import numpy as np
import multiprocessing as mp
from functools import lru_cache

USAGE = """
$python3 LC.py -u USERNAME_2_SEARCH_4 --i
$python3 LC.py -u USERNAME_2_SEARCH_4 --i --e info log html doc

This script simply makes a list of dirs, and files in every each of them (1 recursion level only),
and then goes into every dir and open every file one by one and searches for given username/substring in all the (assumably text) files there. 
It is supposed to work with large leak databases stored in one dir.
"""



parser = argparse.ArgumentParser()
parser.add_argument('-unames', '-u' ,
	help 	=	'Username(s) to search',
	type 	=	str,
	nargs	=	'+',
	required=	True
	)

parser.add_argument('--ignore_case', '--i',
	help 	=	'Ignore the case or not.',
	action 	=	'store_true'
	)

parser.add_argument('--extensions', '-e',
	help 	=	'Accepted file extensions to add to default list, ie "log"',
	type 	=	str,
	nargs   = 	'+',
	required= 	False
	)




args = parser.parse_args()

file_extensions = ['csv', 'txt', 'html', 'sql', 'exp', 'tml'] 
if args.extensions:
	file_extensions = file_extensions + args.extensions

print(args)
print(args.extensions)
USERNAMES = np.array([bytes(x, 'utf8') for x in args.unames])
print(USERNAMES)


logdir = 'logdir'+str(int(time.time()))
os.mkdir(logdir)
resultfile		= open( logdir+os.sep+'results'+'.txt', 'a+')
tempfile_lines	= open( logdir+os.sep+'tempfile_lines'+'.txt', 'a+' )
tempfile_match 	= open( logdir+os.sep+'tempfile_match'+'.txt', 'a+' )
resultfile.writelines([x.decode()+'\n' for x in USERNAMES])



DONE, ALL_FILES = [], []


lru_cache(maxsize=None, typed=True)
def WORKER(FILE:str):

	global logdir
	resultfile		= open( logdir+os.sep+'results'+'.txt', 'a+')
	tempfile_lines	= open( logdir+os.sep+'tempfile_lines'+'.txt', 'a+' )
	tempfile_match 	= open( logdir+os.sep+'tempfile_match'+'.txt', 'a+' )


	MATCHES, TESTED = 0, 0

	DIRNAME = os.path.dirname(FILE)
	
	if FILE.split('.')[-1] in file_extensions:
		f 	= open(FILE, 'rb')

		fl 	= f.readlines(2097152)
		
		while fl:

			TESTED += len(fl)
			# keep original line with caps untouched!
			for line in fl:

				if args.ignore_case:
					lowline = line.lower()
				else: lowline = line			

				for u in USERNAMES:
					if u in lowline:
						print('\n[*] POTENTIAL LEAK:', 
							u, line, DIRNAME, FILE)
						dec0dedline = line.decode('UTF-8', errors='replace').replace('\r\n', '').strip()
						resultfile.write(
							f"{u.decode('utf8', errors='replace')} : {dec0dedline} @ {DIRNAME} -> {FILE}\n")
						MATCHES += 1
			fl 	= f.readlines(2097152)

		#print(f'[*] {len(DONE)} / {len(ALL_FILES)} --> {FILE} #L:{TESTED} : {MATCHES}'+' '*16, flush=False, end = '\r' )
		tempfile_lines.write( f'{TESTED}\n' )
		if MATCHES: tempfile_match.write( f'{MATCHES}\n')
		f.close()
		DONE.append(FILE)




lru_cache(maxsize=None, typed=True)
def leakCheck():
	
	def status():
		t1 = open(tempfile_lines.name, 'r').readlines()
		t2 = open(tempfile_match.name, 'r').readlines()

		lines 	= sum([int(x) for x in t1])
		matches	= sum([int(x) for x in t2])

		print(f'[*] Lines:{lines}\t\tMatches:{matches}',
		 flush=False, end='\r')



	start = time.time()
	base_dirs = [x for x in os.listdir() if os.path.isdir(x)]
	base_dirs = [x for x in base_dirs if 'logdir' not in x]
	base_dirs.append(os.getcwd())

	print('[*] DIRS TO CHECK: ', base_dirs)

	global 		ALL_FILES
	
	for d in base_dirs:
		sub_dir_files 	= 	[x for x in os.listdir(d) if os.path.isfile(d+os.sep+x)]
		
		portion = []
		for file in sub_dir_files:
			#print(f'[*] {sub_dir_files.index(file)} / {len(sub_dir_files)} --> {file} #L:{TESTED} : {MATCHES}'+' '*16, flush=False, end = '\r' )
			absolute = d+os.sep+file
			portion.append(absolute)
			if len(portion) > 3:
				ALL_FILES.append(portion)
				portion = []
		if portion: ALL_FILES.append(portion) # Leftovers

	#print(ALL_FILES)

	for F in ALL_FILES:
		with mp.Pool(processes=8) as pool:
			proc = pool.map(WORKER, F)
			status()
		pool.join()

	#TEST RUN
	end = time.time()
	print(f'{end-start} elapsed.')
	status()
	sys.exit(1)

if __name__ == '__main__':
	leakCheck()

logfile.close()




