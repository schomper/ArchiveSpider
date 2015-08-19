#! /usr/bin/python3

from bs4 import BeautifulSoup
import urllib.request
from nltk.corpus import stopwords
import os

def get_year_links(url):
    """ Get the links of all the year tabs.

    Keyword arguments:
    url -- url of the site to look for year tabs
    """
    f = urllib.request.urlopen(url)
    soup = BeautifulSoup(f.read())
    nav = soup.find("div", { "class" : "header subheader" })
    
    links = []

    for link in nav.findAll("a", href=True):
        link = 'http://www.abc.net.au' + link["href"]
        links.append(link)

    return links

def process_year(year_url):
    """ Get link for every day in the year.
    
    Keyword arguments:
    year_url -- the url of the year page.
    """
    f = urllib.request.urlopen(year_url)
    soup = BeautifulSoup(f.read())
    nav = soup.find("div", { "class" : "c75l" })
    links = []

    for link in nav.findAll("a", href=True):
        link = 'http://www.abc.net.au' + link["href"]
        links.append(link)

    return links

def process_day(day, year_name):
    """ Get the all the links to articles posted on a specified day.
    
    Keyword arguments:
    day_url -- url of the day's first page
    year_name -- name of the year to which the day belongs
    """
    article_list = []

    day_name =  day.split('/')[-1].split(',')[2] + '_' + day.split('/')[-1].split(',')[1] + '.txt'
    day_url = day

    file_name = 'output/' + year_name + '/' + day_name 


    if os.path.exists(file_name):
        print('\tDay %s %s exists.' % (day_name, year_name))
        return
    
    print('\tDay: %s %s.' % (day_name, year_name))

    f = urllib.request.urlopen(day)
    soup = BeautifulSoup(f.read())
    nav = soup.find("div", { "class" : "nav pagination" })
    articles = soup.find('ul', {'class' : 'article-index'})
    next_list = nav.find_all('a', {'class' :'next'})
    day = day + next_list[0]['href']

    for link in articles.findAll("a", href=True):
        link = 'http://www.abc.net.au' + link["href"]
        if (not '/topic/' in link) and (not link in article_list):
            article_list.append(link)
    
    while len(next_list) != 0:
        
        f = urllib.request.urlopen(day)
        soup = BeautifulSoup(f.read())

        nav = soup.find("div", { "class" : "nav pagination" })
        articles = soup.find('ul', {'class' : 'article-index'})
    
        next_list = nav.find_all('a', {'class' :'next'})
        if len(next_list):
            day = day.split('?')[0] + next_list[0]['href']

        for link in articles.findAll("a", href=True):
            link = 'http://www.abc.net.au' + link["href"]
            if not '/topic/' in link:
                article_list.append(link)

    
    f_ptr = open(file_name, 'w')

    for article in article_list:
        write_article(article, f_ptr)


def write_article(url, f_ptr):
    """ Write the information about the article to a file.

    Keyword arguments:
    url -- url of the article to write to file
    file_name -- name of the file to which to write
    """

    try: 
        f = urllib.request.urlopen(url)
    except:
        print('Skipping')
        return

    soup = BeautifulSoup(f.read())
    section = soup.find('div', {'class':'c75l'})
    
    try:
        title = section.find('h1').getText()
    except:
        return

    body = section.findAll('p')
    print('\t\t' + title)
    f_ptr.write('<DOC>\n')
    f_ptr.write('<DOC_NAME>' + title + '</DOC_NAME>\n')
    
    f_ptr.write('<TEXT>\n')
    for para in body:
        para = para.getText()
        cached_stop_words = stopwords.words("english")
        para = ' '.join([word for word in para.split() if word not in cached_stop_words])
        f_ptr.write(para + ' ')

    f_ptr.write('\n</TEXT>\n')
    f_ptr.write('</DOC>\n')

if __name__ == "__main__":
    
    url = 'http://www.abc.net.au/news/archive/'    
    year_links = get_year_links(url)

    for year in year_links:
        year_name = year.split('/')[-1]
        
        print('In year: ' + year_name)
        if not os.path.exists('output/' + year_name):
            os.makedirs('output/' + year_name)
        
        days = process_year(year)

        for day in days:
            process_day(day, year_name)
