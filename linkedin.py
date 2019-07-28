from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from Person import Person

name=input()
opts = Options()
#opts.add_argument('--headless')


browser = Chrome('chromedriver.exe', chrome_options=opts)
browser.get('https://linkedin.com')

form=browser.find_element_by_id('login-email')



form.send_keys('wojciech.padala@gmail.com')
form=browser.find_element_by_id('login-password')
form.send_keys('zaq1@WSX')
browser.find_element_by_id('login-submit').click()
form=browser.find_element_by_tag_name('input')
form.send_keys('Damian Rusinek')
browser.get('https://www.linkedin.com/search/results/all/?keywords={}%20{}&origin=TYPEAHEAD_ESCAPE_HATCH'.format(name.split(' ')[0], name.split(' ')[1]))
content=browser.page_source
soup=BeautifulSoup(content,'html.parser')
elems=soup.find_all('div',{'class' : 'search-result__wrapper'})
for i in elems:
    osoba=Person()
    osoba.linkedin['url']='https://www.linkedin.com{}'.format(i.find('a',{'class' : 'search-result__result-link ember-view'})['href'])
    browser.get(osoba.linkedin['url'])
    cont=browser.page_source
    soup=BeautifulSoup(cont,'html.parser')
    elem=soup.find('div', {'class' : 'mt4 display-flex ember-view'})
    print(elem)
    name=elem.find()


#browser.close()