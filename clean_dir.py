import os

print('Your current working directory is:', os.getcwd())
onlyfiles = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd() ,f))]

for file_name in onlyfiles:
	if 'written' in file_name:
		print('Removing file \'', file_name, '\'...', sep='')
		os.remove(file_name)

print('Your working directory is clean.')
