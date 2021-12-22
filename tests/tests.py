import rss_reader
from rss_reader import args
import unittest


class Test_Channel(unittest.TestCase):

    def test_run_rss_with_no_flags(self):
        """test response with xml and without flags"""
        args.limit = None
        args.json = False
        args.to_pdf = None
        page = open('data/test_cache.xml', 'r')
        no_flags = open('data/channel_with_no_limit.txt', 'r+')
        expected = no_flags.read()
        actual = rss_reader.run(page.read())
        self.assertEqual(expected, actual)

        page.close()
        no_flags.close()

    def test_run_rss_with_limitflag(self):
        """test response with limit flag 4"""
        args.limit = 3
        args.json = False
        args.to_pdf = None
        page = open('data/test_cache.xml', 'r')
        limit_flag = open('data/channel_with_limit3.txt', 'r+')
        expected = limit_flag.read()
        actual = rss_reader.run(page.read())
        self.assertEqual(expected, actual)

        page.close()
        limit_flag.close()

    def test_run_rss_with_jsonflag(self):
        """test response with json flag and no limit"""
        args.json = True
        args.limit = None
        args.to_pdf = None

        page = open('data/test_cache.xml', 'r')
        json_flag = open('data/channel_in_json_no_limit.txt', 'r+')
        expected = json_flag.read()
        actual = rss_reader.run(page.read())
        self.assertEqual(expected, actual)

        page.close()
        json_flag.close()

    def test_run_rss_with_jsonflag_and_limit(self):
        """test response with json flag and limit"""
        args.limit = 3
        args.json = True
        args.to_pdf = None

        page = open('data/test_cache.xml', 'r')
        json_flag = open('data/channel_in_json_limit3.txt', 'r+')
        expected = json_flag.read()
        actual = rss_reader.run(page.read())
        self.assertEqual(expected, actual)

        page.close()
        json_flag.close()

    def test_run_rss_with_to_pdf_flag(self):
        """test response with to_pdf flag"""
        args.limit = None
        args.json = False
        args.to_pdf = "data/temp/RSS.pdf"

        page = open('data/test_cache.xml', 'r')
        rss_reader.run(page.read())
        self.assertTrue('data/temp/RSS.pdf')

        page.close()


    def test_run_rss_with_to_html_flag(self):
        """test response with to_pdf flag"""
        args.limit = None
        args.json = False
        args.to_html = "data/temp/RSS.html"

        page = open('data/test_cache.xml', 'r')
        rss_reader.run(page.read())
        self.assertTrue('data/temp/RSS.html')

        page.close()





if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
