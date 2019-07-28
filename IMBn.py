import imdb
from Person import Person



class IMDbSearch:

    def __init__(self):
        self.found=[]

    def search(self,name):
        im=imdb.IMDb()
        for p in im.search_person(name):
            osoba=Person()
            osoba.name=p['name']
            for k,l in p.items():
               if k != 'name':
                   osoba.imdb[k]=l
            self.found.append(osoba)



