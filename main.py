#!/usr/bin/python
import urllib
import xmltodict
import unicodecsv
import re
from bs4 import BeautifulSoup
import httplib
import base64
import csv
import json

# make sure these two files are in the same folder as this script
# input file, Name column with company names to search
INPUT_FILE = 'company.csv'
# output file, 4 columns with results of the search
OUTPUT_FILE = 'extract.csv'

headers = {
    # Request headers - enter your Bing key!!
    'Ocp-Apim-Subscription-Key': 'enter your bing search key here',
}

with open(INPUT_FILE, 'r') as csvfile:
    	fieldnames = ['Name']
    	reader = csv.DictReader(csvfile)

        # look for company names to build search query
        for row in reader:
            searchQuery = row['Name']
            # company name + " immigration ban"
            searchQuery = searchQuery + " immigration ban"
            print searchQuery
            params = urllib.urlencode({
                # Request parameters
                'q': searchQuery,
                'count': '5',
                'mkt': 'en-us',
                'safeSearch': 'Moderate',
                'freshness': 'Week',
            })
            print "searching..."
            try:
                conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
                conn.request("GET", "/bing/v5.0/news/search?%s" % params, "{body}", headers)
                response = conn.getresponse()
                data = response.read()
                parsed_data = {}
                parsed_data = json.loads(data)
                parsed_data = parsed_data["value"]
                print len(parsed_data)

                for v in parsed_data:
                    print(json.dumps(v["description"], indent=4, separators=(',', ': ')))
                    print(json.dumps(v["url"], indent=4, separators=(',', ': ')))

                    with open(OUTPUT_FILE, 'a') as csvfileW:
                        fieldnamesW = ['Name', 'Link Name', 'Link Description', 'Link']
                        writer = unicodecsv.DictWriter(csvfileW, fieldnames=fieldnamesW)
                        writer.writerow({'Name': row['Name'], 'Link Name': v["name"], 'Link Description': v["description"], 'Link': v["url"]})

                conn.close()
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))
