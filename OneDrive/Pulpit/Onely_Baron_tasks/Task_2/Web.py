from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class Web_scraping():
    #Class contains methods and function operated with web sites.
    #Main task is extracted links to articles from google search sites
    
    def __init__(self, keyword):
        """ 
        Constructor
        -------
        Parameters:
        keyword (string) - string contains keyword
            - example: "president"
        -------
        Atrributes:
        kwd - keyword 
        URL - URL to google search site 
            - example: "https://www.google.com/search?q=site:https://www.searchenginejournal.com/ president"
        """    
        #URL_part1 - string conaitns URL to google search site: searchenginjournal.com
        URL_part1 = "https://www.google.com/search?q=site:https://www.searchenginejournal.com/ "
        self.kwd=keyword
        _URL = ""
        _URL = str(URL_part1+self.kwd)
        self.URL = _URL

    def get_cookies(URL):
        """
        Function returns chrome driver that will issue commands using the wire protocol.
        -------
        Arguments:
        URL - URL to google search site 
            - example: "https://www.google.com/search?q=site:https://www.searchenginejournal.com/ president"

        """
        #path_to_chrome_drirver - string conatins location to ChromeDriver 92.0.4515.107
        path_to_chrome_driver = "C:/Users/micha/OneDrive/Pulpit/chromedriver_win32/chromedriver.exe"
        _chrome = webdriver.Chrome(path_to_chrome_driver)
        _chrome.get(URL)
        _chrome.find_element_by_xpath("//button[@id='L2AGLb']").click()
        return _chrome

    def click_next_page(driver):
        """
        Function generets new(next) page on google search site.
        Function returns:
            - boolen - 1 if it is end of pages, 0 if it is some pages to scrap
            - driver - chrome webdriver
        -------
        Parameters:
        driver - Chrome webdriver        
        """
        try:

            _element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "pnnext"))
                )
            _element.click()
            return 0, driver
        except:

            print("Last Page")
            return 1, driver
        

    def get_links(URL):
        """
        Function scraps all links form google search site.
        Function returns: 
            _links (list) - list of links pointing to web site
                - example: ["https://www.cas.com","https://www.cxad.com"] 
            _qty (int) - number of scraped pages;
                - example: 1
        -------
        Parameters:
        URL - Chrome webdriver        
        """
        _chrome = Web_scraping.get_cookies(URL)
        _chrome.get(URL)
        _links = []
        _link = ""
        _qty = 0
        _end = 0
        while(_end == 0):
            _qty+=1
            _results = _chrome.find_elements_by_xpath("//div[@class='g']") #generate list of classes which contains articles
            for _result in _results:
                _link = _result.find_element_by_tag_name("a") 
                _link = _link.get_attribute("href") #Getting link to article
                _links.append(_link)
            _end, _chrome = Web_scraping.click_next_page(_chrome) #generate new page
        _chrome.quit() #close chrome driver
        return _links, _qty

    
class Save():
    #Class contains methods and functions that save parameters into different files
        
    def save_to_csv(links, kwd):
        """
        Method saves parameters into csv file. Named by kwd (keyword).
        CSV file contains keyword (name of colum) and list of links.
        -------
        links (list) - list of strings
            - example: ["https://www.cas.com","https://www.cxad.com"]        
        keyword (string) - string contains keyword
            - example: "president"
        """
        _df = pd.DataFrame(links, columns=[str(kwd)])
        _df.to_csv(str(kwd+".csv"))

    def save_results(kwd, number_of_results):
        """
        Method saves objects into csv file.
        CSV file contains keyword and number of results in each row.
        ----------
        keyword (string) - string contains keyword
            - example: "president"
        number_of_results (int) - total number of results 
            - example: 1
        """
        _df = pd.DataFrame(data = [[kwd, number_of_results]], columns = ["keyword","Numeber of results"])
        try:

            _df1 = pd.read_csv('Number of results.csv')
            _df = pd.concat([_df1,_df],axis = 0)
            _df.to_csv('Number of results.csv', index=False)
        except FileNotFoundError:

            _df.to_csv('Number of results.csv', index=False)