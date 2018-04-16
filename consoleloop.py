import webscraper
import shortcuts

quicksearch = shortcuts.openlist()
commands = {
    "quit":"quits program and saves search command set as is EX. quit",
    "rename":"renames first specified search command as second one EX. rename emails Emails",
    "searchcommands":"prints current list of search commands EX. searchcommands",
    "addsearch":"adds a search command specified EX. addsearch Emails [a-z0-9\\.\\-+_]+@[a-z0-9\\.\\-+_]+\\.[a-z]+",
    "deletesearch":"deletes a search command specified EX. deletesearch Emails",
    "map":"maps a website to use for the searches EX. map http://www.bing.com",
    "searchpage":"searches for any mapped pages containing the specified string or pattern in its code EX. searchpage microsoft",
    "search":"searches for any specified strings or patterns. Designed to use regular expression EX. search [a-z0-9\\.\\-+_]+@[a-z0-9\\.\\-+_]+\\.[a-z]+",
    "output":"outputs the latest results from a search or page search. text file name can be specified as string after output command but also defults to output if not defined EX. output EX. output hello.txt",
}
##Required for threading
def console():
    urls=[]
    while True:
        check = input("What would you like to do?: ")
        test = check.split()
        if test[0] == "quit":
            shortcuts.savelist(quicksearch)
            break

        elif test[0] == "commands" or test[0] == "help":
            command()
        
        elif test[0] == "rename":
            rename(test)
        
        elif test[0] == "searchcommands":
            searchcommands()
                
        elif test[0] == "addsearch":
            addcommand(check)

        elif test[0] == "deletesearch":
            deletecommand(check)
            
        elif test[0] == "map":
            urls = map(check)
            
        elif test[0] == "searchpage" or test[0] == "searchpages":
            results = searchpage(check,urls)
            
            ##Print out all pages found containing specified pattern
            print("Locations of \""+test[1]+"\"")
            if len(results) > 0:
                for i in results:
                    print(i)
            else:
                print("no results")
        
        elif test[0] == "search":
            results = search(check,urls)
    
            ##Print out all the results found and how many were found
            if len(results) > 0:
                for i in results:
                    print(i)
                print(len(results),"results")
            else:
                print("No Results")
        
        elif test[0] == "output":
            output(check,results)

        print()

def command():
    for i in commands:
        print(i+":"+commands[i])
def rename(test):
    quicksearch[test[2]] = quicksearch[test[1]]
    del quicksearch[test[1]]
def searchcommands():
    temp = quicksearch.keys()
    for i in temp:
        print(i)
def addcommand(check):
    test = check.split(" ",2)
    quicksearch[test[1]] = test[2]

def deletecommand(check):
    test = check.split()
    del quicksearch[test[1]]

def map(check):
    ##Get all the urls in a website
    test = check.split()
    if not "http://" in test[1]:
        test[1] = "http://"+test[1]
    urls = webscraper.mapWebsite([test[1]])
    print(len(urls),"pages")
    return urls

def searchpage(check,urls):
    ##Example of search function
    ##From the specified url list, gets all urls containing specified string pattern
    test=check.split(" ",1)
    if test[1] in quicksearch:
        results = webscraper.searchPages(urls,quicksearch[test[1]])
    else:
        results = webscraper.searchPages(urls,test[1])

def search(check,urls):
    test=check.split(" ",1)
    if test[1] in quicksearch:
        results = webscraper.search(urls,quicksearch[test[1]])
    else:
        ##Get all the searched results contained in the webpages specified
        results = webscraper.search(urls,test[1])
    return results

def output(check,results):
    test=check.split(" ",1)
    if len(test)>1:
        text_file = open(test[1]+".txt", "w")
    else:
        text_file = open("Output.txt", "w")
        for i in results:
            text_file.write(i+",")
    text_file.close()
