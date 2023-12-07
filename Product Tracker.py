import requests
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep
import smtplib

URL = "https://www.amazon.in/Ultimate-Nutrition-Prostar-100-Protein/dp/B000GK11U2/ref=sxts_sxwds-bia-wc-drs1_0?cv_ct_cx=prostar&dchild=1&keywords=prostar&pd_rd_i=B002EVPVCK&pd_rd_r=2fb33a26-ccb1-44cb-bb59-2170ee41b535&pd_rd_w=Koo3l&pd_rd_wg=vuRkW&pf_rd_p=78f37dea-5179-4893-a60a-ddc09ef44708&pf_rd_r=Q91X3ZP1BKPZ9HGFEZNG&qid=1599928873&sr=1-1-4c689def-da13-4510-8a81-e2efd0bc1178&th=1"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}

prod_tracker= pd.read_csv('Product Tracker.csv')
prod_tracker_URLS = prod_tracker.URL

def check_price():

    for x, product in enumerate(prod_tracker_URLS):

        page = requests.get(prod_tracker.URL[x], headers = headers)
        soup = BeautifulSoup(page.content, 'html.parser')
 
        title = soup.find(id = 'productTitle').get_text()
        try:
            price = soup.find(id = 'priceblock_ourprice').get_text()
        except:
            price = ''
        converted_price = float(price[2:].replace(',',''))
        print(title.strip(), ' ', converted_price)
        try:
            if(converted_price < prod_tracker.Threshold[x]):          
                send_mail(title, converted_price)
        except:
            pass
        
def send_mail(title, price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    username = ''
    pwd = ''
    
    server.login(username, pwd)
    
    subject = 'Prices Down'
    body = f"Price down for {title.strip()}, new price is {price}, check it at {URL}"
    
    msg = f"Subject: {subject} \n\n{body}"
    
    server.sendmail('eccentricsage07@gmail.com', 'singh.gaurav10@gmail.com', msg)
    print('Hey Email has been sent')

    server.quit()
    
    
check_price()
    # time.sleep(60*60*24)