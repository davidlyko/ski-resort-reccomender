from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

#Creating the Recommender scale

# Web scraping for trails -- Mtn Creek Specific
url = "https://www.mountaincreek.com/mountainreport"

content = requests.get(url).text
# Parse the html content
soup = BeautifulSoup(content, "html.parser")

open_trails = soup.find("span", {"class": "trail_lift_open"}).text
print(open_trails)

total_trails = soup.find("span", {"class": "trail_lift_total"}).text
numeric_filter = filter(str.isdigit, total_trails)
total_trails = "".join(numeric_filter)
print(total_trails)

#app.run(host='0.0.0.0', port=81)