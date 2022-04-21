import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    #only crawl URLs with this domain, move only to is_valid
    only = ['ics.uci.edu/', 'cs.uci.edu/', 'informatics.uci.edu/', 'stat.uci.edu/', 'today.uci.edu/department/information_computer_sciences/']
    #stores the scrapped hyperlinks 
    hyperlinks = []
    #total_count in frontier for unique links ? #1
    
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    if resp.status != 200:
        print('error') #DO we need to do anything here?
    else:
        #if status is 200
        #use BesutifulSoup to access contents easier
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        #look for hyperlinks
        for r in soup.find_all(href=True):
            print(r) #checking first before continuing code
            #defragment r
            #check if word count is max (global) beautiful soup #2
            #50 most common words in all domains, use code from hw1 #3
            #How many subdomains in the ics.uci.edu domain #4 (global counter?) WRITE ANSWERS IN FILE IN CASE SERVER DIES
            
            #add r to hyperlinks !
    return hyperlinks

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    
    #move only here
    #use regex, if link not in only return false
    
    #Crawl pages with high textual information content
    #Detect and avoid infinite traps
    #Detect and avoid sets of similar pages with no info
    #Detect and avoid dead URLs that return a 200 status but no data
    #Detect and avoid crawling very large files, especially if they have low information value
    
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
