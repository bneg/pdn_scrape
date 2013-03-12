#!/usr/bin/python
# Copyright (C) 2013 Jeremy Johnson
# Scrapes the PDN and outputs to HTML, ad-free
#
# Written by @beyondnegative
# Last edited: 3/11/2013
# 
"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  
If not, see http://www.gnu.org/licenses/gpl-3.0.html
"""
#
# Depends:
#   BeautifulSoup 
#   Requests 

import requests
import time
import string
from BeautifulSoup import BeautifulSoup
from datetime import date, timedelta, datetime


# ------ Load Global Values ------
# Yes, yes, I know. Global = Bad, Local = Good. Gimme a break, still learning .py
site = 'http://peninsuladailynews.com'
# fetch_days = 2  # How many previous days worth to pull
# Change these to a dict {ID : ["title", "Date", "Link"]}
links = [] # List of links from home
titles = [] # Pull title of links from home
stories = [] # Collect the stories
storyID = [] # Story IDs

# Scrape the home page for news links to follow
def scrape_home():
        page = requests.get(site)
        soup = BeautifulSoup(page.text)
        soup.prettify()
        for anchor in soup.findAll('a',{'class':'newsitem2'}):
                try:
                    #print "[+] Found article:"
                    title = anchor['title']
                    link = anchor['href']
                    dts = datetime.strptime(link[9:17], '%Y%m%d') # chop-chop goes the string
                    articleId = link[23:32] # more chop-chop, thx for consistent strings
                    # Debugging, printing output to screen
                    #print "Title: " + anchor['title']
                    #print "Date: " + str(dts)
                    #print "Link: " + anchor['href']
                    #print "ID: " + articleId
                    #print ""
                    #print dts
                    # Parse the link
                    # Pull out Date, ID, and full Link
                    if len(title) > 0: # If the link has a title, save into list
                            links.append(site + link)
                            titles.append(title)
                            storyID.append(articleId)

                except:
                    pass # Else, move on, don't save link

# Parse out date range news only
# FOR FUTURE FEATURE
def today_news():
        for link in linky:
                linkdate = link[38:46]
                try:
                        # Convert scraped numbers to date
                        dts = datetime.strptime(linkdate, '%Y%m%d') 
                        print dts
                except:
                        pass

# Come up with a range of days to fetch
## FOR FUTURE FEATURE
def eval_date(days_to_fetch):
        now = date.today()
        days = []
        for day in range(days_to_fetch):  # Do some date math
                archive_day=date.today() - timedelta(days = day)
                past_date = archive_day.strftime('%Y%m%d')
                days.append(past_date)
        return days

# Scrape an article once we have the linky
def scrape_article(link):
        r = requests.get(link)
        soup = BeautifulSoup(r.text)
        soup.prettify()
        story_text = soup.findAll('span',{'class':'StoryText'})
        stories.append(story_text)
        return True

def export_html():
    f = open('news.html', 'w')
    dash = {0x2014:u"-"} # Crazy unicode decode b.s.
    f.write("""<HTML>
    <HEAD>
    <TITLE>Peninsula News</TITLE>
    </HEAD>
    <BODY>
    <H2>Pen Daily News De-Crappified</H2>
    </BR>
    </BR>""")
    for i in range(len(titles)): 
        f.write('\n<H4><a href="#%s">%s</a></H3>\n' % (storyID[i], titles[i].translate(dash)))
    for i in range(len(titles)): 
        f.write('<HR>')
        f.write('<H3><a name="%s">%s</a></H3>\n' % (storyID[i], titles[i].translate(dash)))
        f.write("%s \n" % stories[i]) # Still dealing with "[" brackets at beg & end of item
    f.write('</BODY></HTML>')

""" Main """
def main():
    print "[+] Scraping Site"
    scrape_home()

    print "\t [+] " + str(len(links)) + " links found"
    print "\t [+] Downloading articles..."
    for link in links: # For each link, grab the assoc. article
        scrape_article(links[i])

    print "\t [+] Exporting to HTML..."
    export_html()
    print "[+] Done."
        
if __name__ == "__main__":
        main()


