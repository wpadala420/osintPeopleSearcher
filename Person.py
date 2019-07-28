class Person(object):

    def __init__(self):
        self.name=''
        self.names=[]
        self.surname=''
        self.title=''
        self.branches=[]
        self.dateOfBirth=''
        self.registries=[]
        self.rejestrUrl=''
        self.twitter={}
        self.instagram={}
        self.photosNumber=0
        self.photos=[]
        self.linkedin={}
        self.facebook={}
        self.imdb={}
        self.wiki={}

    def setName(self, name):
        self.name=name

    def setSurname(self,surname):
        self.surname=surname

    def setTitle(self,title):
        self.title=title

    def setBranch(self,branch):
        self.branches=branch

    def setDateOfBirth(self,date):
        self.dateOfBirth=date

    def addName(self,name):
        self.names.append(name)

    def addRegistryData(self,data):
        self.registries.append(data)

    def setUrl(self,url):
        self.rejestrUrl=url

    def printData(self):
        print('Imie: {}\n'.format(self.name))
        print('Nazwisko: {}\n'.format(self.surname))
        print('Imiona:')
        for i in self.names:
            print('\t {}'.format(i))
        print('\n')
        print('Data urodzenia: {}\n'.format(self.dateOfBirth))
        if self.title != '':
            print('Tytuł: {}\n'.format(self.title))
        if len(self.branches) is not 0:
            print('Dziedziny: ')
            for d in self.branches:
                print('\t {}'.format(d))
        print('Dane z rejestrów : \n')
        print(self.registries)
        print(self.rejestrUrl)

    def fuze(self, person):
        pass

