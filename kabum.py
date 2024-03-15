from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from sheet import Sheet
from datetime import date
from interface import function

NAME = ['sc-fdfabab6-6.jNQQeD']
REGULARPRICE = ['regularPrice']
PRICE = ['sc-5492faee-2.ipHrwP.finalPrice']
INFO = []

class Kabum():
    def __init__(self, link):
        options = Options()     
        options.add_argument("--headless")
        self.link = link
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(link)
        self.take_data()
    
    def find_data(self, options: list):
        for classname in options:
            try:
                value = self.driver.find_element(By.CLASS_NAME, classname).text
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
        Sheet(name).check(data)
        function.config_sheet_file(self.link)  