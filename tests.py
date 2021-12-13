import rss_reader
from rss_reader import Channel, Image, Item, args
import unittest
import xmltodict
import requests
import json
import feedparser


class Test_Channel(unittest.TestCase):

    def test_run_rss_with_simple_link(self):
        """test response with url and without flags"""
        my_url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
        limit= None
        args.limit = None
        args.json = False
        xml_text = requests.get(my_url).text
        my_ordered_dict = xmltodict.parse(xml_text)
        image2 = Image(my_ordered_dict['rss']['channel']['image']['title'],
                       my_ordered_dict['rss']['channel']['image']['link'],
                       my_ordered_dict['rss']['channel']['image']['url'])

        channel = Channel(my_ordered_dict['rss']['channel']['title'], my_ordered_dict['rss']['channel']['link'],
                          image2, limit)

        for item in my_ordered_dict['rss']['channel']['item']:
            channel.items.append(Item(item['title'], item['description'], item['link'], item['pubDate']))

        expected = channel.__str__()

        actual = rss_reader.run(my_url)

        self.assertEqual(expected, actual)

    def test_run_rss_with_limitflag(self):
        """test response with url and without limit flag 4"""
        args.limit = 4
        args.json = False
        limit = 4

        my_url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
        xml_text = requests.get(my_url).text
        my_ordered_dict = xmltodict.parse(xml_text)
        image2 = Image(my_ordered_dict['rss']['channel']['image']['title'],
                       my_ordered_dict['rss']['channel']['image']['link'],
                       my_ordered_dict['rss']['channel']['image']['url'])

        channel = Channel(my_ordered_dict['rss']['channel']['title'], my_ordered_dict['rss']['channel']['link'],
                          image2, limit)

        for item in my_ordered_dict['rss']['channel']['item']:
            channel.items.append(Item(item['title'], item['description'], item['link'], item['pubDate']))

        expected = channel.__str__()

        actual = rss_reader.run(my_url)

        self.assertEqual(expected, actual)

    def test_run_rss_with_jsonflag(self):
        """test response with url and with json flag"""
        args.json = True
        args.limit = None
        limit = None
        my_url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
        xml_text = requests.get(my_url).text
        my_ordered_dict = xmltodict.parse(xml_text)
        image2 = Image(my_ordered_dict['rss']['channel']['image']['title'],
                       my_ordered_dict['rss']['channel']['image']['link'],
                       my_ordered_dict['rss']['channel']['image']['url'])

        channel = Channel(my_ordered_dict['rss']['channel']['title'], my_ordered_dict['rss']['channel']['link'],
                          image2, limit)

        for item in my_ordered_dict['rss']['channel']['item']:
            channel.items.append(Item(item['title'], item['description'], item['link'], item['pubDate']))

        json_data = json.dumps(my_ordered_dict, indent=2)

        expected = json_data
        actual = rss_reader.run(my_url)

        self.assertEqual(expected, actual)

    def test_run_rss_with_jsonflag_and_limit(self):
        """test response with url and with json flag"""
        args.limit = 4
        args.json = True
        limit = 4

        my_url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
        xml_text = requests.get(my_url).text
        my_ordered_dict = xmltodict.parse(xml_text)
        image2 = Image(my_ordered_dict['rss']['channel']['image']['title'],
                       my_ordered_dict['rss']['channel']['image']['link'],
                       my_ordered_dict['rss']['channel']['image']['url'])

        channel = Channel(my_ordered_dict['rss']['channel']['title'], my_ordered_dict['rss']['channel']['link'],
                          image2, limit)
        for item in my_ordered_dict['rss']['channel']['item']:
            channel.items.append(Item(item['title'], item['description'], item['link'], item['pubDate']))

        expected = ""
        NewsFeed = feedparser.parse(my_url)
        for news in range(0, args.limit):
            expected += json.dumps(NewsFeed.entries[news], indent=2)

        actual = rss_reader.run(my_url)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
