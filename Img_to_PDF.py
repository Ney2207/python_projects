import os
import img2pdf
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class PDF:
	def __init__(self, ventana):
		self.ventana = ventana
		self.ventana.title('Image to PDF converter')
		self.ventana.geometry('480x120')
		
		self.path_label = tk.Label(self.ventana, text = 'Ingrese la dirección de las imágenes: ')
		self.path_label.grid(row = 0, column = 1)
		
		self.path_entry = tk.Entry(self.ventana, width = 25)
		self.path_entry.grid(row=0, column=2)
		
		self.path_browse = tk.Button(self.ventana, text='Browse', command=self.ask_sources_path)
		self.path_browse.grid(row=0, column=3)
		
		self.name_label = tk.Label(self.ventana, text='Ingresa el nombre para el archivo: ')
		self.name_label.grid(row=1, column=1)

		self.name_entry = tk.Entry(self.ventana, width=20)
		self.name_entry.grid(row=1, column=2)
		
		self.destination_label = tk.Label(self.ventana, text='Carpeta de destino: ')
		self.destination_label.grid(row=2, column=1)
		
		self.destination_entry = tk.Entry(self.ventana, width=25)
		self.destination_entry.grid(row=2, column=2)
		self.destination_entry.insert(0, os.getcwd())
		
		self.destination_browse = tk.Button(self.ventana, text='Browse', command=self.ask_destination_path)
		self.destination_browse.grid(row=2, column=3)
		
		self.generate_btn = tk.Button(self.ventana, text="Generar PDF", command=self.generate_pdf)
		self.generate_btn.grid(row=3, column=2)
		
	def ask_sources_path(self):
		self.path_entry.delete(0, 'end')
		self.path_entry.insert(0, filedialog.askdirectory())
		
	def ask_destination_path(self):
		self.destination_entry.delete(0, 'end')
		self.destination_entry.insert(0, filedialog.askdirectory())
		
	def generate_pdf(self):
		img_list = []
		path = self.path_entry.get()
		
		if path == '':
			tk.messagebox.showerror('', 'Ingrese la dirección de las imágenes')
			return
		elif not os.path.isdir(path):
			tk.messagebox.showerror('', 'La dirección de las imágenes es inválida')
			return
		
		files = sorted(os.listdir(path))
		
		for img in files:
			if img.endswith(('.jpg', '.jpeg', '.png')):
				with open(os.path.join(path, img), 'rb') as f:
					img_list.append(f.read())
					
		if not img_list:
			tk.messagebox.showerror('', 'Esta carpeta no contiene imágenes compatibles')
			return
						
		if not self.name_entry.get():
			tk.messagebox.showerror('Error', 'Por favor, ingrese un nombre para el archivo')
			return
			
		destination_path = self.destination_entry.get()
		if destination_path == '':
			destination_path = os.getcwd()
		elif not os.path.isdir(destination_path):
			try:
				os.makedirs(destination_path)
				
			except OSError as e:
				tk.messagebox.showerror('Error', 'Ingrese un nombre válido para la ruta')
				return
			
		if '/' in self.name_entry.get():
			tk.messagebox.showerror('Error', 'El nombre de archivo no es válido')
			return
		else:	
			name = os.path.join(destination_path, self.name_entry.get() + '.pdf')
		file_name = self.name_entry.get() + '.pdf'
		
		if os.path.exists(name):
			replace = tk.messagebox.askokcancel('¿Reenplazar archivo?', f'El archivo \"{file_name}\" ya existe\n¿Desea reemplazarlo?')
			if not replace:
				return
				
		progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
		progress_bar.start()
		
		with open(name, 'wb') as f:
			f.write(img2pdf.convert(img_list))
		
		progress_bar.stop()	
		
		self.path_entry.delete('0', 'end')
		self.name_entry.delete('0', 'end')
		tk.messagebox.showinfo('', 'PDF listo')
				
if __name__ == '__main__':
	root = tk.Tk()
	app = PDF(root)
	root.mainloop()
