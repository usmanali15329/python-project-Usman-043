from requests.api import request
import streamlit as st
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re



#################################################################    
#def formaturl(user_url):
#    if not re.match('(?:http|ftp|https)://', user_url):
#        return 'http://{}'.format(user_url)
#    return user_url

#adr=formaturl(user_url=st.text_input('[+] Enter Target URL To Scan: '))
###

#def fix_url(orig_link):
    # force scheme 
#    split_comps = urllib.parse.urlsplit(orig_link, scheme='https')
    # fix netloc (can happen when there is no scheme)
#    if not len(split_comps.netloc):
#        if len(split_comps.path):
            # override components with fixed netloc and path
#            split_comps = urllib.parse.SplitResult(scheme='https',netloc=split_comps.path,path='',query=split_comps.query,fragment=split_comps.fragment)
        
#    return urllib.parse.urlunsplit(split_comps)

#adr=fix_url(orig_link=st.text_input('[+] Enter Target URL To Scan: '))


###########################################################################################

def convert(user_url):
    #user_url = st.text_input('[+] Enter Target URL To Scan: ')
    if user_url.startswith('http://www.'):
        return 'http://' + user_url[len('http://www.'):]
    if user_url.startswith('www.'):
        return 'http://' + user_url[len('www.'):]
    if not user_url.startswith('http://'):
        return 'http://' + user_url
    

adr=convert(user_url=st.text_input('[+] Enter Target URL To Scan: '))



urls = deque([adr])
    
scraped_urls = set()
emails = set()

count = 0
try:
    while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()
        scraped_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
        

        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        st.write('[%d] Processing %s' %  (count,url))
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    st.write('[-] Closing!')

for mail in emails:
    st.write(mail)
