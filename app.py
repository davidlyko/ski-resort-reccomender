from cgitb import text
from flask import Flask, render_template, request
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
mountain = "Hunter Mountain"

#get method to launch the URL
driver.get("https://www.onthesnow.com/")
time.sleep(3)
search_btn = driver.find_element(By.CLASS_NAME, "styles_btnSearch__1DkDs")
search_btn.click()
header = driver.find_element(By.CLASS_NAME, "styles_search__35w0k")
search_bar = header.find_element(By.TAG_NAME, "input")
search_bar.clear()
search_bar.send_keys(mountain)
search_bar.send_keys(Keys.RETURN)
time.sleep(8)
header = driver.find_element(By.CLASS_NAME, "styles_link__Ibp28")
URL = header.get_attribute("href") #first search result link

driver.get(URL) 
time.sleep(3)

mountain_info = driver.find_elements(By.CLASS_NAME, "styles_value__ocDGV")
for mtn in mountain_info: #prints in order: base depth, lifts, trails ---- Different stuff/amounts depending on mtn
    print(mtn.text)





#inputElement.send_keys('1234')
#inputElement.send_keys(Keys.RETURN)

#driver.quit()
@app.route('/about')
def about_page():
    return render_template('about_page.html')

@app.route('/', methods=['POST'])
def output_page():
    city = request.form['city']
    state = request.form['state']
    miles = request.form['miles']
    print(city)
    return render_template('output.html', first_name='Mountain Creek', first_distance='50', first_score='10', second_name='Killington', second_distance='100', second_score='9.5', third_name='Whiteface', third_distance='120', third_score='8.0', fourth_name='Okemo', fourth_distance='200', fourth_score='7.5', fifth_name='Stowe', fifth_distance='350', fifth_score='5.5')




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

