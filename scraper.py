import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import Counter
import nltk

unique_urls = set() #keeps track of all unique urls we encounter 
subdomains = set() #keeps track of all subdomains of ics.uci.edu
blacklist = set() #list of trap websites
max_words = 0 #number of words on the longest webpage
max_webpage = "" #the url of the longest webpage
common_words = {} #50 most common words among all webpages


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    f = open("report", "w+") #create file for report
    global unique_urls
    global max_words
    global max_webpage
    
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
        
        #gather all text on webpage
        text_paragraphs = (''.join(s.findAll(text=True)) for s in soup_content.findAll('p')) #CITE SOURCE
        text_divs = (''.join(s.findAll(text=True)) for s in soup_content.findAll('div'))
        
        #convert to nltk text to tokenize
        nltk_text = nltk.Text(text_paragraphs)
        nltk_text2 = nltk.Text(text_divs)
        #number of words on webpage
        num_words = len(nltk_text) + len(nltk_text2)
        
        #look for hyperlinks on webpage
        for r in soup.find_all('a'):            
            #defragment the url
            if r.get('href') != None and r.get('href') != "#": #none type error? 
                defragment = r.get('href').split("#")
                #print(defragment)
                #update max webpage if necessary
                if num_words > max_words:
                    max_words = num_words
                    max_webpage = defragment[0]
            
                #50 most common words in all domains, use code from hw1 #3 or nltk or
            
                #add defragmented url to hyperlinks list
                hyperlinks.append(defragment[0])
    
    #write info to report file
    f.seek(0)
    f.write("unique urls: ")
    f.write(str(len(unique_urls))) #test unique urls
    f.write("\n")
    f.write("subdomains of ics.uci.edu: ")
    f.write(str(len(subdomains))) #test
    f.write("\n")
    f.write("longest webpage: ")
    f.write(str(max_webpage))
    f.close() #test file writin when server up
    
    return hyperlinks

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    
    global unique_urls
    
    #only crawl URLs with these domains
    only = ['ics.uci.edu/',
            'cs.uci.edu/',
            'informatics.uci.edu/',
            'stat.uci.edu/', 'today.uci.edu/department/information_computer_sciences/']
    
    #CHECKS
    #Crawl pages with high textual information content
    #Detect and avoid infinite traps
    #Detect and avoid sets of similar pages with no info
    #Detect and avoid dead URLs that return a 200 status but no data
    #Detect and avoid crawling very large files, especially if they have low information value     
    
    if url in unique_urls:
            return False #ensure the same url not entered again
      
    #only proceed with url if has correct domain
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
                unique_urls.add(url)#add to unique urls to mark as traversed
                if "ics.uci.edu" in url:
                    subdomains.add(url)#add to list of subdomains
                return True

        except TypeError:
            print ("TypeError for ", parsed)
            raise
    else:
        return False
