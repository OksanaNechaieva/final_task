import argparse
import xmltodict
import json
import logging
from fpdf import FPDF
from dateutil.parser import *
import pathlib

# url for test purpose
# https://timesofindia.indiatimes.com/rssfeedstopstories.cms

logger = logging.getLogger('RSS_Logger')
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='RSS reader', exit_on_error=False)
parser.add_argument('--version', action='version', version='%(prog)s 4.0')
# send version uprade with each itteration
parser.add_argument('--json', default=False, action="store_true", help='Print result as JSON in stdout')
# print output info in json format
parser.add_argument('--verbose', action="store_true", help='Outputs verbose status messages')
# logging
parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
# identify how many news should be in output
parser.add_argument('--to_html', type=pathlib.Path,  help='Creates new HTML file for output data')
# creating new html file
parser.add_argument('--to_pdf', type=pathlib.Path, help='Creates new PDF file for output data')
# creating new pdf file
group = parser.add_mutually_exclusive_group()
group.add_argument('--date', type=int,
                   help='Fetch news for specified date, use info from the cache, can\'t be used with URL')
# # identify news for specified publish date.
group.add_argument('source', nargs='?', help='RSS URL')
# url for parsing

args = ()

try:
    """Check if there is no arguments for flag """
    args = parser.parse_args()
except argparse.ArgumentError as error:
    logger.error('No arguments specified or specified argument has incorrect type. Use --help to see details' + '\n')
    exit()


class Channel:
    """"class to represent content of the xml file for news"""

    def __init__(self, title, link, image, limit):
        self.title = title
        self.link = link
        self.image = image
        self.limit = limit
        self.items = []

    def __str__(self):
        """override the str method for channel objects"""
        result = "Title: " + self.title + "\n" + \
                 str(self.image) + "\n" + \
                 "Link: " + self.link + "\n"
        i = 0
        logger.info(' Display news with limitation: ' + str(args.limit) + '\n')

        for item in self.items:
            if self.limit is None or i < self.limit:
                result = result + "\n\n" + "News #" + str(i + 1) + "\n" + "Title: " + item.title + "\n" + \
                         "Link: " + item.link + "\n" + \
                         "Description: " + str(item.description) + "\n" + "Published: " + item.pubDate + "\n\n"
                i += 1
            else:
                break
        return result

    def json_converter(self):
        print(args.json)
        i = 0
        result = {'channel': {'title': self.title, 'image': self.image.json_image_info(), 'link': self.link}}

        for item in self.items:
            if self.limit is None or i < self.limit:

                items_dict = {'item': {'title': item.title, 'link': item.link, 'description': item.description,
                                       'pubDate': item.pubDate}}

                result['channel'].update({'item ' + str(i + 1): items_dict})
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
        result = "Image info: " + self.title + ", " + self.link + ", " + self.url + "\n"
        return result

    def json_image_info(self):
        result = {'image': {'title': self.title, 'link': self.link, 'url': self.url}}
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


def run(xml_text):
    # xml_text = requests.get(url).text
    # f = open('xml_cache.xml', "w")
    # f.write(xml_text)
    # my_ordered_dict=[]
    my_ordered_dict = xmltodict.parse(xml_text)
    # print(my_ordered_dict)

    image = Image(my_ordered_dict['rss']['channel']['image']['title'],
                  my_ordered_dict['rss']['channel']['image']['link'],
                  my_ordered_dict['rss']['channel']['image']['url'])
    channel = Channel(my_ordered_dict['rss']['channel']['title'], my_ordered_dict['rss']['channel']['link'], image,
                      args.limit)

    logger.info(' Insert info into channel object ' + '\n')

    text = ""

    if args.date is None:
        """"Output data for specified published date"""
        for item in my_ordered_dict['rss']['channel']['item']:
            channel.items.append(Item(item['title'], item['description'], item['link'], item['pubDate']))
        logger.info(' Insert info into item object for news info ' + '\n')
    elif args.date is not None:
        for item in my_ordered_dict['rss']['channel']['item']:
            temp = (parse(item['pubDate'], ignoretz=True)).date()
            pubdate = str(temp).split('-')
            # print(pubdate)
            result = ''
            for i in pubdate:
                result += str(i)
            if result == str(args.date):
                channel.items.append(Item(item['title'], item['description'], item['link'], item['pubDate']))

        logger.info(' Insert info into item object for news info with specified date ' + '\n')

    if args.json == True and args.limit is not None:
        """Output data in json format with selected limit"""
        logger.info(' json flag enabled with limit news = ' + str(args.limit) + '\n')
        # printing as a json string with output limitations with indentation level = 2
        json_data = json.dumps(channel.json_converter(), indent=2)
        print("JSON data is:")
        text += json_data

    elif args.json == True and args.limit is None:
        """Output all data in json format"""
        logger.info(' json flag enabled without limitation \n')
        # printing as a json string without output limitations with indentation level = 2
        json_data = json.dumps(channel.json_converter(), indent=2)
        print("JSON data is:")
        text += json_data

    elif not args.json:
        """"Output data in CLI"""
        # print all information from the channel object
        text += str(channel)

    if args.to_pdf is not None:
        """"Output data in PDF file"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=24)
        pdf.cell(200, 10, txt=channel.title, ln=1, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=channel.link, ln=1, align='C')
        pdf.image('image_name.png', x=60, y=30, w=100, h=40, type='', link='')
        pdf.cell(200, 30, txt=' ', ln=1, align='L')

        i = 0
        for item in channel.items:
            if args.limit is None or i < args.limit:

                pdf.cell(200, 10, txt=' ', ln=1, align='L')
                pdf.cell(200, 10, txt='News #' + str(i + 1), ln=1, align='L')
                pdf.cell(200, 10, txt='Title: ' + item.title.encode('latin-1', 'ignore').decode(), ln=1, align='L')
                pdf.cell(200, 10, txt=item.title.encode('latin-1', 'ignore').decode(), ln=1, align='L')
                pdf.set_text_color(0, 150, 255)
                pdf.cell(100, 10, txt='Link:' + item.link.encode('latin-1', 'ignore').decode(), ln=1, align='L')
                pdf.set_text_color(0, 0, 0)
                if item.description is None:
                    pdf.cell(200, 10, txt='Description: ' + 'None', ln=1,
                             align='L')
                else:
                    pdf.cell(200, 10, txt='Description: ' + item.description.encode('latin-1', 'ignore').decode(),
                             ln=1, align='L')
                pdf.cell(200, 10, txt='Published:  ' + item.pubDate.encode('latin-1', 'ignore').decode(), ln=1,
                         align='L')
                i += 1
            else:
                break

        pdf.output(args.to_pdf)
        text = 'New PDF file with output data is created'

    if args.to_html is not None:
        """"Output data in HTML file"""
        i = 0
        news = ''
        for item in channel.items:
            if args.limit is None or i < args.limit:
                news = news + "<br><br>" + "News #" + str(i + 1) + "<br>" + "Title: " + item.title + "<br>" + \
                       "<a href=" + str(item.link) + " align='center'> Link to the news </a> <br>" + \
                       "Description: " + str(item.description) + "<br>" + "Published: " + item.pubDate + "<br>"
                i += 1
            else:
                break

        f = open(args.to_html, 'w')
        html_template = """<!DOCTYPE html>
        <html>
        <head>
        <title>""" + str(channel.title) + """</title>
        </head>
        <body>
        <h2 align="center">""" + str(channel.title) + """</h2>
        <a href=""" + str(channel.link) + """> Link to the site </a>
        <br>
        <img src=""" + str(channel.image.url) + """ alt="Logo"> </img>
        <br>
        <br>""" + news + """<p> 
        </body>
        </html>
        """
        # writing the code into the file
        f.write(html_template)
        # close the file
        f.close()
        text = 'New HTML file with output data is created'

    return text
