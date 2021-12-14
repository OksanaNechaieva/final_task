import sys
import rss_reader as rss

def result():
    rss_result = rss.run(sys.argv[1])
    print(rss_result)

result()