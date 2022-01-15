from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

app = Flask(__name__)
Mtns = {"Mountain Creek": ["https://www.mountaincreek.com/mountainreport",  0, 0], 
        "Hunter Mountain": ["https://www.huntermtn.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx", 0, 0],
        "Killington": ["https://www.killington.com/the-mountain/conditions-weather/current-conditions-weather", 0, 0]
        }

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

DRIVER_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

ser = Service(DRIVER_PATH)
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)
#get method to launch the URL
driver.get("https://www.onthesnow.com/")
time.sleep(5)
inputElements = driver.find_elements(By.CLASS_NAME, "styles_search__hLy4C")
inputElements[0].send_keys("Mountain Creek")

print(inputElements)
#inputElement.send_keys('1234')
#inputElement.send_keys(Keys.RETURN)

#driver.quit()



#Creating the Recommender scale

#def refresh_trail_data():
'''
# Web scraping for trails -- Mtn Creek Specific -- tested == good
content = requests.get(Mtns["Mountain Creek"][0]).text
# Parse the html content
soup = BeautifulSoup(content, "html.parser")
#open trails
Mtns["Mountain Creek"][1] = soup.find("span", {"class": "trail_lift_open"}).text
#total trails
total_trails = soup.find("span", {"class": "trail_lift_total"}).text
numeric_filter = filter(str.isdigit, total_trails)
Mtns["Mountain Creek"][2] = "".join(numeric_filter)


# Web scraping for trails -- Hunter Mtn Specific -- tested == good
content = requests.get(Mtns["Hunter Mountain"][0]).text
soup = BeautifulSoup(content, "html.parser")
Mtns["Hunter Mountain"][1] = soup.findAll("span", {"class": "c118__number1--v1"})[2].text
total_trails = soup.findAll("span", {"class": "c118__number2--v1"})[2].text
numeric_filter = filter(str.isdigit, total_trails)
Mtns["Hunter Mountain"][2] = "".join(numeric_filter)
'''
#print(Mtns)




#app.run(host='0.0.0.0', port=81)