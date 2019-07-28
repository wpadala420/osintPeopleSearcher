import requests
from Person import Person
from bs4 import BeautifulSoup

class RegistrySearcher:

    def __init__(self):
        self.peopleFound=[]

    def startSearch(self,name):
        req = requests.get('https://rejestr.io/api/search.json?page=1&perPage=100&app=&q={}'.format(name))
        dictionary = req.json()
        people = []
        pagesNumber = int(int(dictionary['total']) / 100)
        if int(dictionary['total']) % 100 > 0:
            pagesNumber = pagesNumber + 1

        for i in range(pagesNumber):
            req = requests.get(
                'https://rejestr.io/api/search.json?page={}&perPage=100&app=&q={}'.format(str(i + 1), name))
            if req.status_code == 200:
                dictionary = req.json()
                for k in dictionary['items']:
                    if k['class'] == 'Person' or 'SciencePerson':
                        people.append(k)
            else:
                passed = (i - 1) * 100
                page = (passed / 50) + 1
                for j in range(2):
                    req = requests.get(
                        'https://rejestr.io/api/search.json?page={}&perPage=50&app=&q={}'.format(str(page), name))
                    dictionary = req.json()
                    page = page + 1
                    for k in dictionary['items']:
                        if k['class'] == 'Person' or 'SciencePerson':
                            people.append(k)
        ludzie = []
        for a in people:
            if a['class'] == 'Person':
                person = Person()
                person.setName(a['data']['first_name'])
                person.setDateOfBirth(a['data']['birthdate'])
                person.setSurname(a['data']['last_name'])
                krs = {}
                krs['krsId'] = a['data']['krs_id']
                person.addName(a['data']['first_name'])
                if a['data']['second_names']:
                    person.addName(a['data']['second_names'])
                if a['data']['registries'].count('krs') > 0 :
                    if 'krs' in a['items']['registries'] and 'organizations_shortlist' in  a['items']['registries']['krs']['data']:
                        organizations = a['items']['registries']['krs']['data']['organizations_shortlist']
                        orgList = []
                        for o in organizations:
                            orgList.append(o['name_short'])
                        krs['organizations'] = orgList
                        person.addRegistryData(krs)
                        person.setUrl(
                            'https://rejestr.io/osoby/{}/{}'.format(a['items']['registries']['krs']['data']['person_id'],
                                                            a['slug']))
                    elif a['data']['registries'].count('ipn') > 0:
                        if 'ipn' in a['items']['registries'] and 'data' in a['items']['registries']['ipn']:
                            ipn={}
                            ipn['birthplace']=a['items']['registries']['ipn']['data']['birthplace']
                            ipn['birthday']=a['items']['registries']['ipn']['data']['birthdate']
                            ipn['father_name']=a['items']['registries']['ipn']['data']['fathers_name']
                            person.addRegistryData(ipn)
                            url='https://rejestr.io/osoby/{}/{}'.format(a['data']['id'],a['slug'])
                            person.setUrl(url)
                ludzie.append(person)



            elif a['class'] == 'SciencePerson':
                dataDict = a['data']
                person = Person()
                fullName = dataDict['name'].split(' ')
                person.setName(fullName[0])
                person.setSurname(fullName[len(fullName) - 1])
                person.setTitle(dataDict['titles'])
                person.setBranch(dataDict['branches'])
                for i in range(len(fullName)):
                    if i is not len(fullName) - 1:
                        person.addName(fullName[i])
                url = 'https://rejestr.io/nauka/{}/{}'.format(a['data']['id'], a['slug'])
                person.setUrl(url)
                ludzie.append(person)

        return ludzie

    def searchAdditionalData(self):
        for i in self.peopleFound:
            if i.rejestrUrl:
                reg=requests.get(i.rejestrUrl)
                content=reg.content
                soup=BeautifulSoup(content,'html.parser')
                body=soup.body
                addData={}
                elemsKrs=body.find_all('div',{'class' : 'chapter krs mt-2'})
                elemsIpn=body.find_all('div',{'class' : 'chapter ipn mt-2'})

    def searchData(self,name):
        self.peopleFound=self.startSearch(name)







