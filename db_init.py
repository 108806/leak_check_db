import os, sys, argparse, time, codecs, pymongo, json, bson, multiprocessing.pool
import numpy as np
from functools import lru_cache

USAGE = """
THIS IS A DRY RUN (no real checks),
TO PUSH ALL THE LINES FROM THE SELECTED FILE EXTENSIONS TO MONGODB.
python3 db_init.py -u dryrunner1337
"""
__VERSION__ = 0.1


parser = argparse.ArgumentParser()
parser.add_argument('-unames', '-u' ,
	help 	=	'Username(s) to search',
	type 	=	str,
	nargs	=	'+',
	required=	True
	)


args = parser.parse_args()

file_extensions = ['csv', 'txt', 'html', 'sql', 'exp', 'tml'] 

print(args)
USERNAMES = np.array([bytes(x, 'utf8') for x in args.unames])
print(USERNAMES)


#	DB OPS:
client = pymongo.MongoClient()
db = client['L34K3D']
col = db['leax']

errlogfile = open(f'errlogfile-{int(time.time())}.txt', 'w+')



lru_cache(maxsize=None, typed=True)
def WORKER(array):
	client = pymongo.MongoClient()
	db = client['L34K3D']
	col = db['leax']
	try:
		#print(type(array), len(array))
		col.insert_many(array, ordered=False)
	except Exception as e:
    #TODO: Fix this, not working.
		if isinstance(e, pymongo.errors.DuplicateKeyError):
			print('[*] Duplicate...', flush=False, end='\r')





lru_cache(maxsize=None, typed=True)
def upLink():
	start = time.time()
	base_dirs = [x for x in os.listdir() if os.path.isdir(x)]
	print('[*] DIRS TO CHECK: ', base_dirs)

	TESTED, exiled = 0, set()
	subdata = [] #preserve subdata to avoid if check.
	
	for d in base_dirs:
		print(d)
		sub_dir_files = os.listdir(d)
		os.chdir(d)
		print('[*] Now in :', d)
		
		for file in sub_dir_files:
			print(f'[*] {sub_dir_files.index(file)} / {len(sub_dir_files)} --> {file} #L:{TESTED}'+' '*16, flush=False, end = '\r' )

			if file.split('.')[-1] in file_extensions:
				f 	= open(file, 'rb')
				fl 	= f.readlines(4194304)
				

				while fl:
					TESTED += len(fl)
					print(f'[*] {sub_dir_files.index(file)} / {len(sub_dir_files)} --> {file} #L:{TESTED}'+' '*16, flush=False, end = '\r' )

					
					data = []
					
					for line in fl:
						line = line.decode('UTF-8', 'replace').\
						replace('\r\n', '').strip()

						ssdata = {
						'lower' 	:	line.lower(),
						'original'	:	line,
						'src'		:	d+os.sep+file,
						'size'		:	len(line),
						}

						subdata.append(ssdata)
						if len(subdata) > 999: 
							data.append(subdata)
							if subdata.__sizeof__() > 1048576:
								print('[*] CHUNK MAY BE TO BIG : ', subdata.__sizeof__(), d+file)
								exiled.add(d+os.sep+file)
								errlogfile.writelines(exiled)
							subdata = []



					with multiprocessing.Pool(processes=8) as pool:
						res = pool.map(WORKER, data)


					try:
						fl 	= f.readlines(4194304)
					except Exception as e:
						print('[*] CANT STAT FILE:', f)
						exiled.add(d+os.sep+file)

				f.close()
		os.chdir('..')

	end = time.time()
	print(f'[*] EXILED files: {exiled}')
	print(f'{end-start} elapsed.')

upLink()
