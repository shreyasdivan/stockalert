from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('UserEmail','Password')

file = pd.read_csv('C:\Python35\stock.csv')
'''
This file has the format:
eg:

Link                             Value Name
..googlefinance...voltas..       1000  Voltas
..yahoofinance...asian paints..  1100  Asian Paints

The link is the url of the web page you want to scrape the real-time stock value from
'''


for i,r in file.iterrows():
    link = r[0]
    web = requests.get(link).content
    soup = bs(web,'html.parser')

# Inspect the source of the web-page to get the id which shows you the price
# In this case it was a 'div' tag with id 'b_open'

    price = soup.find("div", attrs = {"id": "b_open"}).text
    price = float(price)
    if(price < r[1]):
        msg = MIMEMultipart()
        msg['From'] = 'FromAddress'
        msg['To'] = 'ToAddress'
        m='mystockalert:'+r[2] + ' below ' + str(r[1])
        msg['Subject'] = m
        server.sendmail('FromAddress','ToAddress',msg.as_string())
        
server.quit()

    
