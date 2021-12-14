# RSS reader

###How to run
####1. To run rss reader use command: 

    python run_rss_reader.py <url>

Different flags could be specified, use `--help` to see full usage.

###Another run option
####2. In case to use like distribution package use follow commands:
   
    python setup.py bdist_msi  

and 

    pip install -e .

Now you can run rss reader with `rss_reader <url>`. All previous flags can be used.
