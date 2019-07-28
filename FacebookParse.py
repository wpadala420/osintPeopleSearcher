from googleSearch import getFbProfilesUrls, getNameAdnSurname
import requests
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from Person import Person


def checkData(s1,s2):
    nasm=getNameAdnSurname(s1)
    if s2.find(nasm.get('name')) is not -1 and s2.find(nasm.get('surname')) is not -1:
        return True
    else:
        return False


class FaceBookSearcher:
    def __init__(self,name):
        self.people=[]
        self.links=getFbProfilesUrls(name)
        self.goal=name

    def ifInclude(self, url):
        for i in self.links:
            if i is url:
                return True
        return False

    def getNameFromFb(self):
        for j in self.links:
            raw_html=requests.get(j)
            cont=raw_html.content
            soup=BeautifulSoup(cont,'html.parser')
            body=soup.body
            elem=body.find_all('a', {'href': j })
            ifAdded=False
            for i in elem:
                 person=Person()
                 person.setName(i.text)
                 person.facebook['url']=j
                 self.people.append(person)
                 ifAdded=True
            if ifAdded:
                raw_html = requests.get(j)
                cont = raw_html.content
                soup = BeautifulSoup(cont, 'html.parser')
                body = soup.body
                elem = body.find_all('ul', {'class': 'uiList profile-friends _4kg'})
                for o in elem:
                    for k in o:
                        el = k.find_all('div', {'class': 'profileFriendsText'})
                        for f in el:
                            za=f.find_all('a')
                            for x in za:
                                if checkData(self.goal, x.text):
                                    if self.ifInclude(x['href']) is False and x['href'].find('sk-sk') is -1 and \
                                    x['href'].find('pl-pl') is -1:
                                        self.links.append(x['href'])
                self.links=list(set(self.links))



    def searchData(self):
        opts = Options()
        opts.add_argument('--headless')

        browser = Chrome('chromedriver.exe', chrome_options=opts)
        browser.get('https://facebook.com')
        form=browser.find_element_by_id('email')
        form.send_keys('vojtekk94@o2.pl')
        form=browser.find_element_by_id('pass')
        form.send_keys('kochampalictrawke')
        browser.find_element_by_id('loginbutton').click()
        for i in self.people:
            browser.get(i.facebook['url'])
            req=browser.page_source
            soup=BeautifulSoup(req,'html.parser')
            photo_url=''
            photo_desc=''
            elem=soup.find('a',{'class' : '_2nlw _2nlv'})
            i.name=elem.text
            elem=soup.find('img', {'class': '_11kf img'})
            if elem is not None:
                photo_url=elem['src']
                photo_desc=elem['alt']
            i.facebook['profile_photo']=(photo_url,photo_desc)
            elems=soup.find_all('img',{'class' : 'scaledImageFitWidth img'})
            i.facebook['photos_urls']=[]
            for e in elems:
                i.facebook['photos_urls'].append(e['src'])
            i.facebook['favourites']={}
            keys=soup.find_all('div',{'class' : 'labelContainer'})
            m=soup.find_all('div', {'class' : 'mediaPortrait'})
            browser.get('{}/{}'.format(i.facebook['url'], 'about'))
            cont=browser.page_source
            soup=BeautifulSoup(cont,'html.parser')
            infos=soup.find_all('div',{'class' : '_c24 _50f4'})
            i.facebook['data']=[]
            for el in infos:
                val=soup.find('a')
                i.facebook['data'].append(el.text)
            interests=soup.find_all('div' , {'class' : '_30f'})
            i.facebook['interests']={}
            for it in interests:
                t=it.find_all('span', { 'class' : '_3sz'})
                if t:
                    for g in t:
                        i.facebook['interests'][g.text]=[]
                        p=it.find_all('a', {'class' : '_gx7'})
                        for z in p:
                            i.facebook['interests'][g.text]=z.text

        browser.close()



