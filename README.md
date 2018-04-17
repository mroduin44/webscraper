# webscraper
A web scraper and search tool

This program is a work in progress tool for web developers capable of mapping websites through their accessible links and searching the webpages mapped for strings and string patterns for testing purposes. This program was initially designed to be able to find all emails that appear on a website. Similarly, the program is also designed to find any pages containing specified errors defined by a string or string pattern

Current commands:
  1. quit : Quits program and saves search command set as is EX. quit
  2. rename : Renames first specified search command as second one EX. rename emails Emails
  3. searchcommands : Prints current list of search commands EX. searchcommands
  4. addsearch : Adds a search command specified EX. addsearch Emails [a-z0-9\\.\\-+_]+@[a-z0-9\\.\\-+_]+\\.[a-z]+
  5. deletesearch : Deletes a search command specified EX. deletesearch Emails
  6. map : Maps a website to use for the searches EX. map http://www.bing.com
  7. searchpage : Searches for any mapped pages containing the specified string or pattern in its code EX. searchpage microsoft
  8. search : Searches for any specified strings or patterns. Designed to use Python regular expression EX. search Emails
  9. outputresults : Outputs the latest results from a search or page search. If file name not specified, defults to output.txt
  10. outputmap : Outputs the mapped website in its entirity
