#! /bin/python3

################################################################################
# A Python script to webscrape match information from cricbuzz.com and output as
# 1> A numbered, colour-coded list of available matches
# 2> Plain output of match selected using argument. Get status by :
#   send-notify "SCORE" "$(cric.py <num> | awk -f\( '{print $NF }' )"
################################################################################

import requests
from bs4 import BeautifulSoup

list = []
req = requests.get("https://www.timeanddate.com/astronomy/night/india/new-delhi", headers={"Accept-Language": "en-US,en;q=0.6"})
soup = BeautifulSoup(req.content, "html.parser")
#print( soup.prettify)

    #res = soup.find( class_ = "cb-col cb-col-100")
#res = soup.find( 'table' , class_ = 'tb-wc zebra sep fw' )
res = soup.find( 'table' , class_ = 'tb-wc zebra sep fw' )

for ele in res.find_all('tr'):
    for entry in ele.find_all(['td','th']):
        print(f'{entry.text:^15}', end="")
    print()
    #print(*arr , sep='\t', end='\n')
#print(res.text)
"""
import pandas
tables = pandas.read_html('https://www.timeanddate.com/astronomy/night/india/new-delhi', headers={"Accept-Language": "en-US,en;q=0.6"})
tables[1]
"""
#for item in tables:
    #print(item)
