# from bs4 import BeautifulSoup
# import requests
import pandas as pd
import time


def GetData():

    table = pd.read_html("http://10.241.9.103/049/mainabc.htm?page_number=1")


    procent = (table[0]['Wert'])/100
    numeTanc = table[0]['Messstelle']

    df = pd.DataFrame({'NumeTanc':numeTanc,'Procent':procent})
    
    
    return df

