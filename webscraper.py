import requests
import re
from multiprocessing import Pool, TimeoutError, Pipe

##Function is designed to be used with EmailScrapeList function
##Function outputs all emails found back through the Pipe given
##Requires a Pipe for the Conn parameter
##Requires a string url for the url parameter
def searchThreads(conn,url,args):
    list=[]
    response = requests.get(url)
    temp=re.findall(args, response.text)
    conn.send(temp)
    conn.close()

##Function returns a list of all emails found in the urls specified
##Requires a list of urls for the url parameter
def search(url,args):
    output=[]
    temp=[]
    parent_conn, child_conn = Pipe()
    multiple_results=[]
    print("Please Wait...")
    with Pool(processes=4) as pool:
        multiple_results = [pool.apply_async(searchThreads,(child_conn,i,args))for i in url]
        for i in multiple_results:
            check="False"
            while check=="False":
                check=i.ready()
            temp.append(parent_conn.recv())
    for page in temp:
        for result in page:
            if not result in output:
                output.append(result)
    pool.close
    return output

##Function is designed to be used with mapWebsite function
##Function outputs all local links found back through the Pipe given
##Requires a Pipe for the conn parameter
##Requires a url in string format for the urls parameter
def mapWebThreads(conn,urls,mainPage):
    LocalRefs=[]
    output=[] 
    try:
        response = requests.get(urls)
        temp = re.findall(r"href=\"[:a-z0-9//\.\-+_]+",response.text)
        for link in temp:
            if mainPage in link:
                LocalRefs.append(link[6:])
            elif link[6] == "/":
                LocalRefs.append(mainPage+link[6:])
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        print("Error")
    conn.send(LocalRefs)
    conn.close()

##Function outputs a list containing all of the urls in the domain of a website higher than the start url
##Requires if __name__ == '__main__': in the main program for the multithreding to work
##Requires a list of string Urls for the url parameter
def mapWebsite(url):
    text_file = open("Output.txt", "w")
    parent_conn, child_conn = Pipe()
    mapped=[]
    process=[]
    mainPage=url[0]
    while len(url)>0:
        results=[]
        temp=[]
        print(len(mapped),"Mapped")
        if len(url)>128:
            process=url[0:128]
        else:
            process=url
        mapped=mapped+process
        print("Searching",len(process),"of",len(url),"links")
        with Pool(processes=4) as pool:
            multiple_results = [pool.apply_async(mapWebThreads,(child_conn,i,mainPage)) for i in process]
            for i in multiple_results:
                check="False"
                while check=="False":
                    check=i.ready()
                temp.append(parent_conn.recv())           
        test=[]
        for i in temp:
            test=test+i
        process=[]
        if len(url)>128:
            url=url[128:]
        else:
            url=[]
        for page in test:
            if not page in mapped and not page in url:
                text_file.write(page+"\n")
                url.append(page)
    text_file.close()
    return mapped
    
##Function outputs a list containing all of the urls containing the specified string pattern
##Requires if __name__ == '__main__': in the main program for the multithreding to work
##Requires a list of string Urls for the url parameter
##Requires a string pattern to search for for the arg parameter
def searchPages(url,arg):
    output=[]
    temp=[]
    parent_conn, child_conn = Pipe()
    multiple_results=[]
    print("Please Wait...")
    with Pool(processes=4) as pool:
        multiple_results = [pool.apply_async(searchpageThreads,(child_conn,i,arg))for i in url]
        for i in multiple_results:
            check="False"
            while check=="False":
                check=i.ready()
            temp.append(parent_conn.recv())
    for page in temp:
        if not page in output and not page is "":
            output.append(page)
    pool.close
    return output

##Function is designed to be used with emailScrapeList function
##Function outputs all urls containing the specified pattern back through the Pipe given
##Requires a Pipe for the Conn parameter
##Requires a url in string form for the url parameter
##Requires the specified string pattern to search for for the arg parameter
def searchpageThreads(conn,url,arg):
    list=[]
    response = requests.get(url)
    temp=re.findall(arg, response.text)
    if len(temp)>0:
        conn.send(url)
    else:
        conn.send("")
    conn.close()
    
    
##Function returns all local links found in the specified list of urls
##Requires list of string ulrs for urls parameter
def mapLocalLinks(urls):
    LocalRefs=[]
    output=[]
    for i in urls:
        response = requests.get(i)
        temp = re.findall(r"href=\"[:a-z0-9//\.\-+_]+",response.text)
        for link in temp:
            print(link[6:])
            if i in link:
                LocalRefs.append(link[6:])
            elif link[6] == "/":
                LocalRefs.append(i+link[6:])
    for link in LocalRefs:
        print(link)
        if not link in output:
            output.append(link)
    return output
    
##Function returns all emails found on a specified string url
##Requires a url as a string for the url parameter
def scrapeEmails(url):
    list=[]
    response = requests.get(url)
    temp=re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text)
    for i in temp:
        print(i)
    return temp

def mapLinks(urls):
    output=[]
    response = requests.get(urls)
    temp = re.findall(r"http[s//:]+[a-z0-9//\.\-+_]+",response.text)
    for link in temp:
        if not link in output:
            output.append(link)
    return output
