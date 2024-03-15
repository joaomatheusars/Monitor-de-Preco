from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

link = 'https://www.kabum.com.br/produto/418271/cadeira-gamer-dt3-nero-ate-140kg-com-almofada-reclinavel-braco-4d-cilindro-de-gas-classe-4-preto-13747-2'
options = Options()     
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(link)

p = driver.find_element(By.CLASS_NAME, 'sc-5492faee-2.ipHrwP.finalPrice').text
print(p)