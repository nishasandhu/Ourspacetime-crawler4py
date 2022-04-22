import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import Counter
import nltk

unique_urls = set() #1 
subdomainds = set()
blacklist = set()
max_words = 0 #2
max_webpage = ""
common_words = {} #3


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    file_x = open("report", "w+")
    global unique_urls
    global max_words
    global max_webpage
    print("extracting")
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    #stores the scrapped hyperlinks 
    hyperlinks = []
    #total_count in frontier for unique links ? #1
    
    #change relative urls to absolute?
    
    if resp.status != 200:
        print('error') #DO we need to do anything here?
    else:
        #if status is 200
        #use BesutifulSoup to access contents easier
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        soup_content = BeautifulSoup(resp.raw_response.content)
        
        text_paragraphs = (''.join(s.findAll(text=True)) for s in soup_content.findAll('p')) #CITE SOURCE
        text_divs = (''.join(s.findAll(text=True)) for s in soup_content.findAll('div'))
        
        text = text_paragraphs + text_divs
        
        nltk_text = nltk.Text(text)
        
        num_words = len(nltk_text)
        
        #look for hyperlinks
        for r in soup.find_all('a'):
            #print(r.get('href'))
            #for r in soup.find_all(href=True):
            #print(r) #checking first before continuing code
            
            #defragment r
            if r.get('href') != "#": #none type error? 
                defragment = r.get('href').split("#")
                #print(defragment)
                if num_words > max_words:
                    max_words = num_words
                    max_webpage = defragment[0]
                    #num of words
            
                #50 most common words in all domains, use code from hw1 #3
            
                #add defrag url to hyperlinks
                hyperlinks.append(defragment[0])
    
    f.seek(0)
    f.write("unique urls: " + str((len(unique_urls))) #test unique urls works
    f.write("subdomains of ics.uci.edu: " + str((len(subdomains))) #test
    f.write("longest webpage: " + max_webpage)
    f.close() #test file writin when server up
    
    return hyperlinks

def is_valid(url):
    global unique_urls
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    
    #only crawl URLs with this domain
    only = ['ics.uci.edu/',
            'cs.uci.edu/',
            'informatics.uci.edu/',
            'stat.uci.edu/', 'today.uci.edu/department/information_computer_sciences/']
    
    #FIXME
    #Crawl pages with high textual information content
    #Detect and avoid infinite traps
    #Detect and avoid sets of similar pages with no info
    #Detect and avoid dead URLs that return a 200 status but no data
    #Detect and avoid crawling very large files, especially if they have low information value
            
    
    if url in unique_urls:
            return False #test that not duplicates entered
            
    if any(link in url for link in only):
        print(url)
        try:
            parsed = urlparse(url)
            if parsed.scheme not in set(["http", "https"]):
                return False
            if re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
                return False
            else:
                unique_urls.add(url)
                if "ics.uci.edu" in url:
                    subdomains.add(url)#add subdomains
                return True

        except TypeError:
            print ("TypeError for ", parsed)
            raise
    else:
        return False
