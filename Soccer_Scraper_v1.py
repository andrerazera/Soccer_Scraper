

# %%
# Import Libraries -------------------------------------------------
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from collections import defaultdict
import re
import pandas as pd

# Set variable with a path for chromedriver.exe --------------------------------------
path_chromedriver = r"C:\Users\Andre\OneDrive - BRF S.A\Python Projects\PersonalProjects\004_Soccer_Scraper\chromedriver.exe"


URL = "https://www.flashscore.com/"

options = webdriver.ChromeOptions() #Set chromedriver options
options.add_argument("--headless") #Toggle hidden browser
driver = webdriver.Chrome(path_chromedriver, options=options) 

# Selenium get URL
driver.get(URL)
# Wait for page to fully render
sleep(5)


# Function to get future games ----------------------------------
def Nextday():
    xpath="//div[@id='live-table']/div/div[2]/div[3]/div" #click em tomorow!!!! funcionou
    link = driver.find_element_by_xpath(xpath)
    link.click()
    sleep(5)

# Call Function to go to next day, you can run this function many times to get number of days ahead
# toggle = 'OFF' #toggle function that clicks in tomorrow's matches link

# if toggle == 'ON':
#     Nextday()

results = BeautifulSoup(driver.page_source, "html.parser")

# Tags to scrape
classes =  {'Home_Team': re.compile('^event__participant event__participant--home*'),
          'Score': re.compile('^event__scores*'),
          'Away_Team': re.compile('^event__participant event__participant--away*'),
          'Event_one_line': re.compile('^event__match event__match--oneLine*')
          }
          
driver.quit()


# %%
lista=[]
dicionario={}


for i in classes:

    for tag in results.find_all(
        "div", {"class": classes[i]}
    ):
        lista.append(tag.text)
    dicionario[i] = lista
    # print(len(dicionario[i])) # Check to make sure that there is same number of registers for all registers in df
    lista=[]

df = pd.DataFrame(dicionario)


# %%
# Get status / hour of the matc
lista = []
for r in df['Event_one_line']:
    if r[0] == 'F':
        lista.append(r[0:6])
    else:
        lista.append(r[0:5])

df['Hour/Status'] = lista


# Get date series to df
class_date = re.compile('^calendar__datepicker*')

for tag in results.find_all("div", {"class": re.compile(class_date)}):
    date = tag.text

df['date'] = date

# Build output dataframe
df = df[['Home_Team','Away_Team','Score','Hour/Status','date']]


# %%
# Save Output file to Excel
df.to_excel('Output'+date.replace('/','.')+'.xlsx')


# Next Features intended:
    # Filter games of interest
    # Conect with google calendar with an API
    # Automation to run it regularly 