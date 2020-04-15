import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from selenium.webdriver.common.action_chains import ActionChains
import math
import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
import time


d=0
header = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
options = Options()
options.headless = True
browser = webdriver.Chrome('chromedriver.exe',options=options)

f = open("test.csv", "w")
f.truncate()
writer = csv.writer(f)
writer.writerow(["No","Product Title","Processor","RAM","Internal Storage","Price","Seller Rating","Seller Name","Seller Location","Link"])
f.close()

keyword = 'mi 9t pro'

def set_url(key):
    URL_toko = 'https://www.tokopedia.com/find/'+key+'?sc=24&page=1'
    URL_buka = 'https://www.bukalapak.com/c/handphone/hp-smartphone/?search[keywords]='+key+'&search[new]=1'
    URL_shopee = 'https://shopee.co.id/search?facet=1211&keyword='+key
    URL_laza = 'https://www.lazada.co.id/beli-handphone/?q='+key
    return URL_toko,URL_buka,URL_shopee,URL_laza
URL_toko,URL_buka,URL_shopee,URL_laza = set_url(keyword) 
def count_page(URL):
    if re.search('tokopedia',URL,re.IGNORECASE):
        page = requests.get(URL,headers=header) 
        soup = BeautifulSoup(page.content,'html.parser')
        count_item = soup.find(attrs={"class":"_1lUX-bZg"}).get_text()
        total_item = count_item.split()[count_item.split().index('Menampilkan')+1]
        divide_total = math.ceil(int(total_item)/60)
        print(total_item)
        return divide_total
    elif re.search('bukalapak',URL,re.IGNORECASE):
        page = requests.get(URL,headers=header) 
        soup = BeautifulSoup(page.content,'html.parser')
        count_page = soup.find("span",{"class":"last-page"})
        return count_page.get_text()
    elif re.search('shopee',URL,re.IGNORECASE):
        browser.get(URL)
        time.sleep(6)
        soup = BeautifulSoup(browser.page_source,'html.parser')
        count_page = soup.find(attrs={"class":"shopee-mini-page-controller__total"}).get_text()
        return count_page
    elif re.search('laza',URL,re.IGNORECASE):
        i = 0
        condition2 = False
        print(URL)
        browser.get(URL)
        soup = BeautifulSoup(browser.page_source,'html.parser')
        print(hasattr(soup,'span'))
        try:
            count_item = soup.find("div",{"class":"c1DXz4"})
            count_item = count_item.find('span')
            count_item = count_item.get_text()
        except :
            if condition2 == True:
                pass
            condition1 = False
            try_solve_laza = 0
            #soup = BeautifulSoup(browser.page_source,'html.parser')
            source_element = browser.find_element_by_css_selector('span#nc_2_n1z')
            move = ActionChains(browser)
            move.click_and_hold(source_element).move_by_offset(300, 0).release().perform()
            time.sleep(3)
            click_element = browser.find_elements_by_xpath("//a[@href='javascript:__nc.reset()']")[0]
            if click_element:
                for i in range(5):
                    if condition1 == True:
                        condition2 = True
                        pass
                    else:
                        print("condition1 wrong")
                    try_solve_laza=try_solve_laza+1
                    print(try_solve_laza)
                    if try_solve_laza%5==0:
                        try:
                            count_item = soup.find("div",{"class":"c1DXz4"})
                            count_item = count_item.find('span')
                            count_item = count_item.get_text()
                        except:
                            try_solve_laza=0
                            time.sleep(10)
                            condition1 = True
                            continue
                    try:
                        
                        click_element.click()
                        time.sleep(3)
                        source_element = browser.find_element_by_css_selector('span#nc_2_n1z')
                        move = ActionChains(browser)
                        move.click_and_hold(source_element).move_by_offset(300, 0).release().perform()
                        time.sleep(3)
                        click_element = browser.find_elements_by_xpath("//a[@href='javascript:__nc.reset()']")[0]
                    except:
                        condition1 = True
                        continue
                    if condition1 == True : pass
                    #break
        print(i)
        if i == 4:
            time.sleep(30)
            browser.get(URL)
            soup = BeautifulSoup(browser.page_source,'html.parser')
            count_item = soup.find("div",{"class":"c1DXz4"})
            count_item = count_item.find('span')
            count_item = count_item.get_text()

        s = sum(map(int,re.findall(r'\b\d+\b',count_item)))
        count_item = math.ceil(s/40)
        print(count_item)
        return count_item
    

print("Line 124")        
count_page(URL_shopee)
def find_price(key):
    count_page()
    

print("Line 130")      
def multi_replace(text,condit):
    for i in condit:
        text = text.replace(i,'')
    return text

print("Line 136")   
for x in range(1,2):
    print("Line 138")
    URL = 'https://www.tokopedia.com/find/mi-9t-pro?page='+str(x) 
    print("THIS WORK?")
    print(URL)
    page = requests.get(URL,headers=header) 
    soup = BeautifulSoup(page.content,'html.parser')
    print(soup)
    title = soup.findAll("div",{"class":"_2OBup6Zd"})
    price = soup.findAll("span",{"class":"_3fNeVBgQ"})  
    for each_title in title:
        output_href = each_title.find("a").get('href')
        output_title = each_title.find("h3",{"class":"Ka_fasQS"}).get_text()
        output_seller_location = each_title.find("span",{"class":"UY2SWg6T"}).get_text()
        output_seller_name = each_title.find("span",{"class":"_1GDgKs4K"}).get_text()
        output_price = each_title.find("span",{"class":"_3fNeVBgQ"}).get_text()
        conditional_price = ['Rp','.',' ']
        output_price = multi_replace(output_price,conditional_price)
        #print(output_price)
        output_rating= each_title.find("span",{"class":"_3-hbLA9j"})
        if output_rating is None:
            output_rating = "None"
        else:
            output_rating= each_title.find("span",{"class":"_3-hbLA9j"}).get_text()
        #print(output_rating)
        
        if re.search('9t pro',output_title,re.IGNORECASE):
            if re.search('bukan',output_title,re.IGNORECASE):
                model = "MI 9T PRO"
                Proc = "SDM 855"
                if re.search(r'\b6gb\b',output_title,re.IGNORECASE) or re.search(r'\b6 gb\b',output_title,re.IGNORECASE):
                   RAM = "6 GB"
                elif re.search(r'\b8gb\b',output_title,re.IGNORECASE) or re.search(r'\b8 gb\b',output_title,re.IGNORECASE):
                   RAM = "8 GB"
                if re.search(r'\b64gb\b',output_title,re.IGNORECASE) or re.search(r'\b64 gb\b',output_title,re.IGNORECASE):
                   ROM = "64 GB"
                elif re.search(r'\b128gb\b',output_title,re.IGNORECASE) or re.search(r'\b128 gb\b',output_title,re.IGNORECASE):
                   ROM = "64 GB"
                elif re.search(r'\b256gb\b',output_title,re.IGNORECASE) or re.search(r'\b256 gb\b',output_title,re.IGNORECASE):
                   ROM = "256 GB"  
            else:
                model = "MI 9T PRO"
                Proc = "SDM 855"
                if re.search(r'\b6gb\b',output_title,re.IGNORECASE) or re.search(r'\b6 gb\b',output_title,re.IGNORECASE):
                   RAM = "6 GB"
                elif re.search(r'\b8gb\b',output_title,re.IGNORECASE) or re.search(r'\b8 gb\b',output_title,re.IGNORECASE):
                   RAM = "8 GB"
                if re.search(r'\b64gb\b',output_title,re.IGNORECASE) or re.search(r'\b64 gb\b',output_title,re.IGNORECASE):
                   ROM = "64 GB"
                elif re.search(r'\b128gb\b',output_title,re.IGNORECASE) or re.search(r'\b128 gb\b',output_title,re.IGNORECASE):
                   ROM = "64 GB"
                elif re.search(r'\b256gb\b',output_title,re.IGNORECASE) or re.search(r'\b256 gb\b',output_title,re.IGNORECASE):
                   ROM = "256 GB"  
        elif re.search('k20 pro',output_title,re.IGNORECASE):
            if re.search('Bukan K20 Pro',output_title,re.IGNORECASE) or re.search('Bukan Redmi K20 Pro',output_title,re.IGNORECASE):
                model = "K 20/MI 9T"
                Proc = "SDM 730"
                if re.search(r'\b6gb\b',output_title,re.IGNORECASE) or re.search(r'\b6 gb\b',output_title,re.IGNORECASE):
                   RAM = "6 GB"
                elif re.search(r'\b8gb\b',output_title,re.IGNORECASE) or re.search(r'\b8 gb\b',output_title,re.IGNORECASE):
                   RAM = "8 GB"
                if re.search(r'\b64gb\b',output_title,re.IGNORECASE) or re.search(r'\b64 gb\b',output_title,re.IGNORECASE):
                   ROM = "64 GB"
                elif re.search(r'\b128gb\b',output_title,re.IGNORECASE) or re.search(r'\b128 gb\b',output_title,re.IGNORECASE):
                   ROM = "64 GB"
                elif re.search(r'\b256gb\b',output_title,re.IGNORECASE) or re.search(r'\b256 gb\b',output_title,re.IGNORECASE):
                   ROM = "256 GB"
            else:
                model = "K20 PRO"
                Proc = "SDM 855"
                if re.search(r'\b6gb\b',output_title,re.IGNORECASE) or re.search(r'\b6 gb\b',output_title,re.IGNORECASE):
                   RAM = "6 GB"
                elif re.search(r'\b8gb\b',output_title,re.IGNORECASE) or re.search(r'\b8 gb\b',output_title,re.IGNORECASE):
                   RAM = "8 GB"
                if re.search(r'\b64gb\b',output_title,re.IGNORECASE) or re.search(r'\b64 gb\b',output_title,re.IGNORECASE):
                   ROM = "64 GB"
                elif re.search(r'\b128gb\b',output_title,re.IGNORECASE) or re.search(r'\b128 gb\b',output_title,re.IGNORECASE):
                   ROM = "64 GB"
                elif re.search(r'\b256gb\b',output_title,re.IGNORECASE) or re.search(r'\b256 gb\b',output_title,re.IGNORECASE):
                   ROM = "256 GB"    
        else:
            model = "K 20/MI 9T"
            Proc = "SDM 730"
            if re.search(r'\b6gb\b',output_title,re.IGNORECASE) or re.search(r'\b6 gb\b',output_title,re.IGNORECASE):
               RAM = "6 GB"
            elif re.search(r'\b8gb\b',output_title,re.IGNORECASE) or re.search(r'\b8 gb\b',output_title,re.IGNORECASE):
               RAM = "8 GB"
            if re.search(r'\b64gb\b',output_title,re.IGNORECASE) or re.search(r'\b64 gb\b',output_title,re.IGNORECASE):
               ROM = "64 GB"
            elif re.search(r'\b128gb\b',output_title,re.IGNORECASE) or re.search(r'\b128 gb\b',output_title,re.IGNORECASE):
               ROM = "64 GB"
            elif re.search(r'\b256gb\b',output_title,re.IGNORECASE) or re.search(r'\b256 gb\b',output_title,re.IGNORECASE):
               ROM = "256 GB" 
                
        d=d+1;
        file = open("test.txt","a")
        file.write(str(d)+" "+each_title.get_text())
        file.close()
        with open('test.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([d,output_title,model,Proc,RAM,ROM,output_price,output_rating,output_seller_name,output_seller_location,output_href])
        
        
        #print(output_href)
       
#print(title)
#title2 = soup.findAll("span",{"itemprop":"name"})