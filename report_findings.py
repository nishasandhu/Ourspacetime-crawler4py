import re
from urllib.parse import urlparse

def sort_domains():
    subdomains = []
    #key = subdomain ie vision.ics.uci.edu 
    #value = num of pages w/key subdomain
    counted_subdomains = dict()
    
    with open("report", "r") as file:
        unique_urls = file.readlines()[3:]
        for url in unique_urls:
            #if url contains the domain - ics.uci.edu
            if ".ics.uci.edu" in url:
                subdomains.append(url)
            
        
        for url in subdomains:
            parsed = urlparse(url)
            #netloc gets the domain from the url
            if parsed.netloc in counted_subdomains:
                #if subdomain exists in the dictionary - increase the count
                counted_subdomains[parsed.netloc] = counted_subdomains[parsed.netloc] + 1
            else:
                counted_subdomains[parsed.netloc] = 1
                
                
        #write findings to report
       
        
        print("Number of subdomains: "+str(len(counted_subdomains)))
        for subdomain in sorted(counted_subdomains):
            print("%s : %d" %(subdomain,counted_subdomains[subdomain]))
        
if __name__ == "__main__":
    sort_domains()