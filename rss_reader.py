import argparse
import xmltodict
import sys
import requests
import json
import feedparser
import logging

# url for test purpose
# https://timesofindia.indiatimes.com/rssfeedstopstories.cms


logger = logging.getLogger('RSS_Logger')
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='RSS reader', exit_on_error=False)
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
# send version uprade with each itteration
parser.add_argument('--json', default=False, action="store_true", help='Print result as JSON in stdout')
# print output info in json format
parser.add_argument('--verbose', '-ver', action="store_true", help='Outputs verbose status messages')
# logging
parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
# identify how many news should be in output
parser.add_argument('source', nargs='?', help='RSS URL')
#print(parser)

args = ()
try:
    """Check if there is no arguments for limit flag """
    args = parser.parse_args()
except Exception as error:
    logger.error('No arguments for limit' + '\n')
    print("Expected one argument for --limit")
    exit()


class Channel:
    """"class to represent content of the xml file for news"""
    items = []
    def __init__(self, title, link, image, limit):
        self.title = title
        self.link = link
        self.image = image
        self.limit = limit

    def __str__(self):
        """override the str method for channel objects"""
        result = "Title: " + channel.title + "\n" + \
                 str(image) + "\n" + \
                 "Link: " + channel.link + "\n"
        i = 0
        logger.info(' Display news with limitation: ' + str(args.limit) + '\n')

        for item in self.items:
            if self.limit is None or i < self.limit:
                result = result + "\n\n" + "News #" + str(i + 1) + "\n" + "Title: " + item.title + "\n" + \
                         "Link" + item.link + "\n" + \
                         "Description: " + str(item.description) + "\n\n"
                i += 1
            else:
                break
        return result


class Image:
    """"class to represent images in the xml file"""

    def __init__(self, title, link, url):
        self.title = title
        self.link = link
        self.url = url

    def __str__(self):
        """override the str method for image objects"""
        result = "Image info: " + image.title + ", " + image.link + ", " + image.url + "\n"
        return result


class Item:
    """"class to represent each news in the xml file"""

    def __init__(self, title, description, link, pubDate):
        self.title = title
        self.description = description
        self.link = link
        self.pubDate = pubDate


if not args.verbose:
    logger.disabled = True

xml_text = requests.get(sys.argv[1]).text
my_ordered_dict = xmltodict.parse(xml_text)
image = Image(my_ordered_dict['rss']['channel']['image']['title'], my_ordered_dict['rss']['channel']['image']['link'],
              my_ordered_dict['rss']['channel']['image']['url'])
channel = Channel(my_ordered_dict['rss']['channel']['title'], my_ordered_dict['rss']['channel']['link'], image,
                args.limit)

logger.info(' Insert info into channel object ' + '\n')

for item in my_ordered_dict['rss']['channel']['item']:
    channel.items.append(Item(item['title'], item['description'], item['link'], item['pubDate']))
logger.info(' Insert info into item object for news info ' + '\n')

if args.json == True and args.limit != None:
    logger.info(' json flag enabled with limit news = ' + str(args.limit) + '\n')
    # printing as a json string with output limitations with indentation level = 2
    NewsFeed = feedparser.parse(sys.argv[1])
    for news in range(0, args.limit):
        print(json.dumps(NewsFeed.entries[news], indent=2))

elif args.json == True and args.limit == None:
    logger.info(' json flag enabled without limitation \n')
    # printing as a json string without output limitations with indentation level = 2
    json_data = json.dumps(my_ordered_dict, indent=2)
    print("JSON data is:")
    print(json_data)

elif not args.json:
    # print all information from the channel object
    print(channel)
