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
import googlemaps


app = Flask(__name__)
#Format: { "Moutain X" : [url, lifts open / total lifts, trails open / total trail]}
Mtns = {}

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

def create_webdriver(): 
    DRIVER_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    ser = Service(DRIVER_PATH)
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    return driver

# @param string
def add_mtn(name): 
    Mtns[name] = ["url", 0, 0]

# @param dictionary
def update_mtns(mtns): 
    for mountain in mtns: 
        driver = create_webdriver()
        driver.get("https://www.onthesnow.com/")
        time.sleep(3)
        search_btn = driver.find_element(By.CLASS_NAME, "styles_btnSearch__1DkDs")
        search_btn.click()
        header = driver.find_element(By.CLASS_NAME, "styles_search__35w0k")
        search_bar = header.find_element(By.TAG_NAME, "input")
        search_bar.clear()
        search_bar.send_keys(mountain)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(6)
        header = driver.find_element(By.CLASS_NAME, "styles_link__Ibp28")
        URL = header.get_attribute("href") #first search result link
        Mtns[mountain][0] = URL 
        driver.get(URL) 
        time.sleep(3)
        mountain_info = driver.find_elements(By.CLASS_NAME, "styles_value__ocDGV")
        update_key(mountain, mountain_info)
        driver.quit()

def update_key(mountain, mountain_info): 
    #if mtn has extra info
    if(len(mountain_info) > 3): 
        Mtns[mountain][1] = mountain_info[2].text
        Mtns[mountain][2] = mountain_info[3].text
    else: 
        Mtns[mountain][1] = mountain_info[1].text
        Mtns[mountain][2] = mountain_info[2].text

# @param location info 
def update_mountain_names(address):
    gmaps = googlemaps.Client(key='AIzaSyBW9c-mXKxyj3uxFUIrBL5VM3daUKciXVM')

    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=mongolian&inputtype=textquery&locationbias=circle%3A2000%4047.6918452%2C-122.2226413&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=YOUR_API_KEY"

    payload={}
    headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
                

                
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


#running main program methods
print("Starting program")
update_mountain_names("10 Crabapple Drive, York Haven, PA, 17370")
'''
mountain_names = ["Mountain Creek", "Hunter Mountain"]
i = 1
for name in mountain_names: 
    add_mtn(name)
    print("Added " + str(i) + " mountain (" + name + ")")
    i = i + 1

update_mtns(Mtns)
print(Mtns)


app.run(host='0.0.0.0', port=81)
'''

