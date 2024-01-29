from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from sheet import Sheet
from datetime import date
from interface import function

NAME = ['//*[@id="__next"]/main/article/section/div[2]/div[1]/div/h1', '//*[@id="__next"]/main/article/section/div[3]/div[1]/div/h1']
REGULARPRICE = ['//*[@id="blocoValores"]/div[3]/b']
PRICE = ['//*[@id="blocoValores"]/div[2]/div[1]/div/h4']

class Kabum():
    def __init__(self, link):
        options = Options()     
        options.add_argument("--headless")
        self.link = link
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(link)
        self.take_data()
    
    def find_data(self, options: list):
        for xpath in options:
            try:
                value = self.driver.find_element(By.XPATH, xpath).text
                return value
            except:
                pass
        
        return ""
       
    def take_data(self):
        data = []
        
        name = self.find_data(NAME)
        regularPrice = self.find_data(REGULARPRICE)
        price = self.find_data(PRICE)
        
        today = date.today()
        day = today.strftime("%d/%m/%Y")        
        
        data.append(name)
        data.append(day)
        data.append(regularPrice)
        data.append(price)

        self.create_sheet(name, data)
    
    def create_sheet(self, name, data):
        Sheet(name).verifica(data)
        function.config_sheet_file(self.link)  