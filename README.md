## Lightweight Selenium Scraper for Dread

The following is a brief introduction on how to use this code to scrape Dread.

### Requirements

You will find the necessary libraries and imports at the top of `main.py`.
I'm also using Tor Browser `v.11.0.9` (based on Mozilla Firefox `91.7.0esr`). I'm
running Selenium `4.1.3`. To begin using the code, you will need to set `DATA_PATH`
and set the location of the Firefox binary to use. In this case, the Tor Browser's
path.

### High-level Flow

The code has two routines to retrieve lists of URLs, and one to retrieve the
contents inside the URLs. To retrieve lists of URLs, we can either start by
navigating the pages from the homepage of Dread, or we can execute a search and
navigate the search results' pages. Thus, if desired, this process can be split
across two browsers, one to retrieve URLs, one to navigate through those URLs.

###Example Directory Structure

Following is a sample tree view for how your directory should look.
```
./dread-scraper/
    main.py
    ./data/
        ./search_term=scam/
            ./scrapes/
                ./<post_id_1>/
                    ./post.html
                .   
                .
                ./<post_id_n>/
            urls.txt
            PAGE
```
### Procedure

This scraper requires manual setup to get it to begin scraping, due to issues
with the Tor Browser software, as well as having to solve Dread's CAPTCHA. To do
this, I conduct the following procedure:

- First, terminate all Tor Browser instances you may have running. On my end, 
there seems to be a bug where Tor Browser will not connect to the Tor network
if launched by Selenium when there's another instance active.
- Once the Tor Browser is launched, wait for it to connect to the circuits. From
here, you can try navigating to a website as a test. I use `google.com`
- If working properly, navigate to Dread's main page with the `navigate_to_main()`
function. Here you will need to wait an arbitrary amount of time determined by Dread (typically,
between 1-3 mins.). After that, you will be redirected to a CAPTCHA which you need to solve
in under 1 min.
- Once you are on the mainpage of Dread you can begin retrieving links. You can, for example,
launch `get_post_links_through_main('1')` to begin retrieving all posts' links from each page,
starting from page 1. Note that, the main page of Dread indexes posts from various sub-Dreads.
This process usually works flawlessly for a while. At some point, though, Dread seems to ask
again for a CAPTCHA although I'm not entirely sure what triggers that yet.
- Once satisfied with the number of URLs that have been retrieved (or we have hit 500,
which is the number of pages that Dread indexes), we can proceed to navigate each URL and
save the source, using `get_source_pages_from_list('/path/to/search_term=scam/scrapes', '/path/to/search_term=scam/urls.txt')`
(example based on the above file structure). If everything is working properly, the `scrapes`
folder should start getting populated with folders named after the post IDs.
