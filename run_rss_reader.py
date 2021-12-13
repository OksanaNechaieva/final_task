import sys
import rss_reader as rss

rss_result = rss.run(sys.argv[1])

print(rss_result)