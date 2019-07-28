from MagicGoogle import MagicGoogle
import pprint
from bs4 import BeautifulSoup
import requests

class NotFoundPersonListError(Exception):
    """Not found list of people on facebook"""
    pass




def searchTags(s):
    tab=[]
    for a in range(len(s)):
        if s[a] is '<' and s[a+1] is not '/':
            nowy=''
            while s[a] is not '>':
                nowy=nowy+s[a]
                a=a+1
            nowy=nowy+s[a]
            if len(nowy)>5:
                tab.append(nowy)
            if a < len(s)-1:
                a=a+1
    return tab

def searchHrefs(s):
     tab=searchTags(s)
     hrefs=[]
     for i in tab:
         if i.find('href=') is not -1:
             link=''
             ind=i.find('href=')+5
             ind=ind +1
             while i[ind] is not '"':
                 link=link+i[ind]
                 ind=ind + 1
             hrefs.append(link)
     return hrefs

def getNameAdnSurname(n):
    dict={}
    dict['name']=''
    dict['surname']=''
    i=0
    while n[i] is not ' ':
        dict['name']=dict['name']+n[i]
        i=i+1
    i=i+1
    while i < len(n):
        dict['surname']=dict['surname']+n[i]
        i=i+1
    return dict




def getLinks(s,name):
    tab=searchHrefs(s)
    links=[]
    nasm=getNameAdnSurname(name)
    for i in tab:
        if (i.find('facebook.com') is not -1) and \
                ((i.find('people') or (i.find(nasm.get('name').lower()) is not -1 or i.find(nasm.get('name')) is not -1)
                 or (i.find(nasm.get('surname').lower()) is not -1) or i.find(nasm.get('surname')) is not -1 ) and
                 (i.find('pages') is -1 and i.find('photos')) is -1) and ((len(links) is 0) or
                                                                          (i.find(links[len(links)-1]) is -1)):
            links.append(i)
    return list(set(links))





def getFbListUrlbyGoogle(name):
    PROXIES=None
    mg=MagicGoogle(PROXIES)
    result=mg.search(query=name+' site:www.facebook.com')
    lista=list(result)
    gate={}
    flag=True
    it=0
    nasn=getNameAdnSurname(name)
    while flag is True and it < len(lista):
        if lista[it].get('title').find('Profiles') is not -1 and lista[it].get('title').find(nasn.get('name')) is not -1 \
                and lista[it].get('title').find(nasn.get('surname')) is not -1 and lista[it].get('title').find('Facebook')is not -1:
            gate=lista[it]
            flag=False
        else:
            it=it+1

    if gate is {}:
        return None
    else:
        return gate.get('url')


def getFbProfilesUrls(name):
    raw_html=requests.get('https://facebook.com/public/{}-{}'.format(name.split(' ')[0], name .split(' ')[1]))
    html2=raw_html.content
    html=BeautifulSoup(html2, 'html.parser')
    body=html.body
    elements=body.find_all('div', class_='hidden_elem')
    links=[]
    for a in elements:
        for i in getLinks(str(a),name):
            links.append(i)
    return links
