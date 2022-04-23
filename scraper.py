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
    
    # report findings
    global unique_urls
    global max_words
    global max_webpage
    
    try: 
        f = open("report", "w+") #create file for report
        
        # preset report findings in case server crashes and we have to start it up again
        #will need to strip lines to get only numbers/url
        unique_urls = int(f.readline().strip("\n").replace("unique urls: ", "")
        max_words = int(f.readline().strip("\n").replace("subdomains of ics.uci.edu: ", "")
        max_webpage = f.readline().strip("\n").replace("longest webpage: ", ""
        #stores the scrapped hyperlinks 
        hyperlinks = []

        if resp.status != 200:
            print('error: ', str(resp.error)) #prints out what kind of error it is
        elif resp.status == 200 and resp.raw_response.content == None: 
            #assuming None when no data, should we blacklist when 200 or just do nothing?
            blacklist.add(resp.url) #also add url?
        else:
            #status is 200
            #use BeautifulSoup to access contents easier
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
                    #update max webpage if necessary
                    if num_words > max_words:
                        max_words = num_words
                        max_webpage = defragment[0]

                    #50 most common words in all domains, use code from hw1 #3 or nltk or

                    #add defragmented url to hyperlinks list
                    hyperlinks.append(defragment[0])

        #write info to report file
        f.seek(0)
        f.write("unique urls: " + str(len(unique_urls)) + "\n")
        f.flush()
        f.write("subdomains of ics.uci.edu: " + str(len(subdomains)) + "\n")
        f.flush()
        f.write("longest webpage: " + str(max_webpage) + "\n")
        f.flush()
    except Exception as e:
        print("error occurred", e)
    finally:
        f.close() #test file writin when server up

    return hyperlinks

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    
    global unique_urls
    
    #only crawl URLs with these domains
    only = [".ics.uci.edu/",
            ".cs.uci.edu/",
            ".informatics.uci.edu/",
            ".stat.uci.edu/", "today.uci.edu/department/information_computer_sciences/"]
    
    #CHECKS
    #Crawl pages with high textual information content
    #Detect and avoid infinite traps
    #Detect and avoid sets of similar pages with no info
    #Detect and avoid dead URLs that return a 200 status but no data
    #Detect and avoid crawling very large files, especially if they have low information value     
    
    if url in unique_urls or blacklist:
            print("already visited or blacklisted")
            return False #ensure the same url not entered again
      
    #only proceed with url if has correct domain
    if any(link in url for link in only):
        print(url)
        print("^ should have correct domain")
        try:
            parsed = urlparse(url)
            if parsed.scheme not in set(["http", "https"]):
                return False
            if re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
                return False
            else:
                print(url)
                print("^just added to unique urls")
                unique_urls.add(url)#add to unique urls to mark as traversed
                if ".ics.uci.edu" in url:
                    subdomains.add(url)#add to list of subdomains
                return True

        except TypeError:
            print ("TypeError for ", parsed)
            raise
    else:
        return False
