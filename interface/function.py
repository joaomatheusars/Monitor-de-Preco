import os
from sheet import Sheet
from openpyxl import Workbook, load_workbook

def verify_link(link: str):
    if link.count('kabum'): return True
    
def config_file(link: str):
    if not os.path.exists('config.txt'):
        with open('config.txt','a+') as file:
            file.write(f'{link}\n')
    else:
        with open('config.txt', 'r') as file:
            lines = file.readlines()
        
        links = [l[:-1] for l in lines]

        if not link in links: 
            with open('config.txt', 'a+') as file:
                file.write(f'{link}\n')
                
def config_sheet_file(link: str):
    filename = 'sheets/links.xlsx'
    workbook = Workbook()
    links = []
    if not os.path.exists(filename):
        workbook.save(filename)
        
    wb = load_workbook(filename)
    ws = wb.active
    
    for row in wb['Sheet'].values:
        links.append(row[0])
    
    if not link in links:
        ws.append([link])
        wb.save(filename)
        
def get_links_sheets_file():
    filename = 'sheets/links.xlsx'
    links = []
    
    wb = load_workbook(filename)
    wb.active
    
    for row in wb['Sheet'].values:
        links.append(row[0])
        
    return links
                 
def monitor():
    with open("config.txt", 'r') as file:
        lines = file.readlines()
    
    return lines