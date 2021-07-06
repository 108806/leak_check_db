import os

BANNED_CHARS = { ' ', '\t', '\n', '\r' }
REPLACED = lambda s : ''.join(
	[x if x not in BANNED_CHARS else '_' for x in s])


def ren_all():
	bd_files = os.listdir()
	for d in bd_files:
		if BANNED_CHARS & set(d):
			os.rename(d, REPLACED(d))

	bd_files = tuple(x for x in os.listdir()
		if os.path.isdir(x))
	for d in bd_files:
		sub_files = os.listdir(d)
		os.chdir(d)
		for s in sub_files:
			if BANNED_CHARS & set(s):
				os.rename(s, REPLACED(s))
				print(f'[*] RENAMED {s} to {REPLACED(s)}')
		os.chdir('..')


ren_all()

