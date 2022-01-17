from asyncio import sleep
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
api_key = ""

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

def create_webdriver(): 
    DRIVER_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    ser = Service(DRIVER_PATH)
    op = webdriver.ChromeOptions()
    op.add_argument('headless') #hide window from popping up
    driver = webdriver.Chrome(service=ser, options=op)
    return driver

# @param string
def add_mtn(name): 
    Mtns[name] = ["url", 0, 0]

# @param dictionary
def update_mtns(): 
    print("Gathering mountain info ...")
    driver = create_webdriver()
    for mountain in list(Mtns): 
        driver.get("https://www.onthesnow.com/")
        #main search bar that takes you to second search bar
        search_btn = driver.find_element(By.CLASS_NAME, "styles_btnSearch__1DkDs")
        search_btn.click()
        #search bar that actually takes input
        header = driver.find_element(By.CLASS_NAME, "styles_search__35w0k")
        search_bar = header.find_element(By.TAG_NAME, "input")
        search_bar.clear()
        search_bar.send_keys(mountain.replace("Resort", ""))
        search_bar.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            #first link after search
            header = driver.find_element(By.CLASS_NAME, "styles_link__Ibp28")  
        except: 
            #nothing came up in search
            Mtns.pop(mountain)
        else:     
            URL = header.get_attribute("href") #first search result link
            Mtns[mountain][0] = URL 
            driver.get(URL) 
            time.sleep(2)
            mountain_info = driver.find_elements(By.CLASS_NAME, "styles_value__ocDGV")
            update_key(mountain, mountain_info)

    driver.quit()

        
        

def update_key(mountain, mountain_info): 
    if( len(mountain_info) == 0): 
        return
    #if mtn has extra info
    if(len(mountain_info) > 3): 
        Mtns[mountain][1] = mountain_info[2].text
        Mtns[mountain][2] = mountain_info[3].text
    else: 
        Mtns[mountain][1] = mountain_info[1].text
        Mtns[mountain][2] = mountain_info[2].text

# @param zip_code = 5 digit int, max_distance = meters @return a list of nearby mountains by name
def update_mountain_names(zip_code, max_distance):
    gmaps = googlemaps.Client(key=api_key)
    
    geocode = gmaps.geocode(zip_code)
    lat = geocode[0]['geometry']['location']['lat']
    lng = geocode[0]['geometry']['location']['lng']
    loc = (lat, lng)

    places = gmaps.places_nearby(location = loc, keyword = "ski resort", radius = max_distance) 
    names = []
    for i in range(len(places["results"])):
        names.append(places["results"][i]["name"])

    return names
                

                
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
def main(): 
    print("Starting program")

    mountain_names = update_mountain_names(12442, 30000)
    print(mountain_names)
    for name in mountain_names: 
        add_mtn(name)
    update_mtns()
    print(Mtns)

main()

#app.run(host='0.0.0.0', port=81)


