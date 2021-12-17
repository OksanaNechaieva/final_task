import sys
import rss_reader as rss
from rss_reader import args
import requests
import xmltodict
import re


def result():
    # xml_text = requests.get(sys.argv[1]).text
    # rss_result = rss.run(xml_text)
    # print(rss_result)

    if args.date is not None:
        if len(str(args.date)) != 8:
            print("Date format is not correct. Input %Y%m%d - 8 symbols")
            exit()
        else:
            xml_text = (open('xml_cache.xml', "r")).read()
            rss_result = rss.run(xml_text)
            print(rss_result)

    elif args.date is None:
        xml_text = requests.get(sys.argv[1]).text
        # f=open('xml_cache.xml', "w")
        # f.write(xml_text)
        rss_result = rss.run(xml_text)
        print(rss_result)


result()
