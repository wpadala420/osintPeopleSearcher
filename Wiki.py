import wikipediaapi
from Person import Person

class WikiSearch:
    def __init__(self):
        self.found=[]


    def search(self,name):
        wiki=wikipediaapi.Wikipedia('pl')
        se=wiki.page(name)
        if se.exists():
            osoba=Person()
            osoba.name=name
            osoba.wiki['info']=se.summary
            osoba.wiki['categories']=se.categories
            self.found.append(osoba)




