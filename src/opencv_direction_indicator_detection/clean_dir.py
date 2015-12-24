import os
import sys

def main(clean_directory=''):
	cwd = os.getcwd()
	print('Your current working directory is:', cwd)
	clean_directory_joined = os.path.join(cwd, clean_directory)
	print('Cleaning directory:', clean_directory_joined)
	onlyfiles = [name for name in os.listdir(clean_directory_joined) if os.path.isfile(os.path.join(clean_directory_joined, name))]

	print(onlyfiles)

	for file_name in onlyfiles:
		path = os.path.join(clean_directory_joined, file_name)
		if 'written' in file_name:
			print('Removing file \'', path, '\'...', sep='')
			os.remove(path)

	print('Your working directory is clean.')

if __name__ == '__main__':
	main(sys.argv[1])
