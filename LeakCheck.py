import os, sys, ctypes, argparse, time, codecs
import numpy as np
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



logfile = open('logfile'+str(int(time.time()))+'.txt', 'a+')

args = parser.parse_args()

file_extensions = ['csv', 'txt', 'html', 'sql', 'exp', 'tml'] 
if args.extensions:
	file_extensions = file_extensions + args.extensions

print(args)
print(args.extensions)
USERNAMES = np.array([bytes(x, 'utf8') for x in args.unames])
print(USERNAMES)
logfile.writelines([x.decode()+'\n' for x in USERNAMES])


lru_cache(maxsize=None, typed=True)
def leakCheck():
	start = time.time()
	base_dirs = [x for x in os.listdir() if os.path.isdir(x)]
	print('[*] DIRS TO CHECK: ', base_dirs)

	MATCHES, TESTED = 0, 0
	for d in base_dirs:
		print(d)
		sub_dir_files = os.listdir(d)
		os.chdir(d)
		print('[*] Now in :', d)
		
		for file in sub_dir_files:
			print(f'[*] {sub_dir_files.index(file)} / {len(sub_dir_files)} --> {file} #L:{TESTED} : {MATCHES}'+' '*16, flush=False, end = '\r' )

			if file.split('.')[-1] in file_extensions:
				f 	= open(file, 'rb')
				fl 	= f.readlines(4096)
				while fl:
					TESTED += len(fl)
					# keep original line with caps untouched!
					for line in fl:
						#print(line)
						if args.ignore_case:
							lowline = line.lower()
						else: lowline = line			

						for u in USERNAMES:
							if u in lowline:
								print('\n[*] POTENTIAL LEAK:', 
									u, line, d, file)
								logfile.write(
									f'{u} : {line} @ {d} -> {file}\n')
								MATCHES += 1
					fl 	= f.readlines(4096)
				f.close()
		
		os.chdir('..')
		end = time.time()
		print(f'{end-start} elapsed. #{MATCHES}')

leakCheck()
