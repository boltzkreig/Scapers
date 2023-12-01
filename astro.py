#! /bin/python3

import pandas
tables = pandas.read_html('https://www.timeanddate.com/astronomy/night/india/new-delhi', headers={"Accept-Language": "en-US,en;q=0.6"})
tables[1]
