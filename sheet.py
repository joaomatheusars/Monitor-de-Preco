from openpyxl import Workbook, load_workbook
from datetime import date
import os

class Sheet():
    def __init__(self, fileName: str):
        self.filename = f'{self.format_filename(fileName)}.xlsx'
        self.workbook = self.load_workbook()    
        self.create_dir()
        self.check_file_execel()
     
    def format_filename(self, fileName: str):
        caracters = ['\'', '/', ':', '*', '?', '"', '<', '>', '|']
        for caracter in caracters:
            if caracter in fileName:
                fileName = fileName.replace(caracter, "")  
                
        return fileName
                
    def create_dir(self):
        if not os.path.exists('sheets'):
            os.mkdir('sheets')
    
    def check_file_execel(self):
        if not os.path.exists(f'sheets/{self.filename}'):
            ws = self.workbook.active
            ws.append(['Nome', 'Data', 'Preço', 'A Vista'])
            self.save_workbook()
    
    def load_workbook(self):
        if not os.path.exists(f'sheets/{self.filename}'): return Workbook()
        return load_workbook(f'sheets/{self.filename}') 
            
    def save_workbook(self):
        self.workbook.save(f'sheets/{self.filename}')
    
    def create_rows(self, data: list):
        ws = self.workbook.active
        ws.append(data)
        self.save_workbook()
        
    def check(self, data: list):        
        today = date.today()
        day = today.strftime("%d/%m/%Y")   
        last_row = len(range(self.workbook['Sheet'].max_row))
        
        if self.workbook['Sheet'][f'A{last_row}'] == 'Placa de Vídeo RTX 4060 Ti Eagle Gigabyte NVIDIA GeForce, 8 GB GDDR6, DLSS, Ray Tracing - GV-N406TEAGLE-8GD G10':
            print('data',self.workbook['Sheet'][f'B{last_row}'].value == day)
            print('preço',self.workbook['Sheet'][f'C{last_row}'].value == data[2])
            print('avista',self.workbook['Sheet'][f'D{last_row}'].value == data[3])

        # VERIFICA SE EXISTE VALORES IGUAIS PARA NÃO REPETIR.        
        if not self.workbook['Sheet'][f'B{last_row}'].value == day:
            self.create_rows(data)
            
        if self.workbook['Sheet'][f'B{last_row}'].value == day and not self.workbook['Sheet'][f'C{last_row}'].value == data[2] and not self.workbook['Sheet'][f'D{last_row}'].value == data[3]: 
            self.create_rows(data)
