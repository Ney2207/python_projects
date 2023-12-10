import os
import time

def ask_folder():
	path = input('ingrese una dirección\n')
	
	if path == '':
		path = os.getcwd()
	elif not os.path.exists(path):
		print('Ruta no válida')
		ask_folder()
		
	return path
		
folder_to_scan = ask_folder()

all_files_list = os.listdir(folder_to_scan)

img_files_list = []

for file in all_files_list:
	if file.endswith(('.jpg', '.png', '.jpeg')):
		img_files_list.append(file)
		
def move_files(file_index, to_path):
	file_path = os.path.join(folder_to_scan, img_files_list[file_index])
	os.rename(file_path, to_path)	
		
binary_files_list = []

for file in img_files_list:
	with open(file, 'rb') as f:
		binary_files_list.append(f.read())
		
duplicated_files = 0
		
for i, file in enumerate(binary_files_list):
	for another_index, another_file in enumerate(binary_files_list):
		if another_index == i:
			continue
		else:
			if file == another_file:
				now = time.time()
				timestamp = time.strftime("%Y-%m-%d %H:%M", time.localtime(now))
				duplicates_folder = os.path.join(os.getcwd(), 'Duplicates')
				ima_no_folder = os.path.join(duplicates_folder, timestamp)
				os.makedirs(ima_no_folder, exist_ok=True)
				destiny_path = os.path.join(ima_no_folder, img_files_list[another_index])
				move_files(another_index, destiny_path)
				img_files_list.pop(another_index)
				binary_files_list.pop(another_index)
				duplicated_files += 1

print(duplicated_files, 'Duplicated files')
