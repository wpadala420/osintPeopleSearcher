import FacebookParse
import instagram
import jsonpickle
from Person import Person
from rejestr import RegistrySearcher
import twitter2
from IMBn import IMDbSearch
from Wiki import WikiSearch


class BigSearch:

    def __init__(self):
        self.found=[]

    def printData(self):
        for i in self.found:
            print(i.name + ' ' + i.surname)
            if i.title:
                print('\t\t Tytuł: ' + i.title)
            if i.branches:
                print('\t\t Dziedziny: ')
                for j in i.branches:
                    print('\t\t\t\t- '+ j)
            if i.dateOfBirth:
                print('\t\tData urodzenia:\t\t'+ i.dateOfBirth)
            if i.registries:
                print('\t\tDane z rejestrów:')
                for k in i.registries:
                    for l,m in k.items():
                        print('\t\t\t\t{} - {}'.format(l, m))
            if i.twitter:
                print('\t\tTwitter:')
                for a1,a2 in i.twitter.items():
                    print('\t\t\t\t{} - {}'.format(a1, a2))

            if i.instagram:
                print('\t\tInstagram:')
                for a1,a2 in i.instagram.items():
                    print('\t\t\t\t{} - {}'.format(a1, a2))

            if i.linkedin:
                print('\t\tLinkedIn:')
                for a1,a2 in i.linkedin.items():
                    print('\t\t\t\t{} - {}'.format(a1,a2))

            if i.facebook:
                print('\t\tFacebook:')
                for a1,a2 in i.facebook.items():
                    print('\t\t\t\t{} - {}'.format(a1,a2))

            if i.imdb:
                print('\t\tIMDb:')
                for a1,a2 in i.imdb.items():
                    print('\t\t\t\t{} - {}'.format(a1,a2))

            if i.wiki:
                print('\t\tWikipedia:')
                for a1,a2 in i.wiki.items():
                    print('\t\t\t\t{} - {}'.format(a1,a2))




    def BigSearch(self,name):
        insta=instagram.InstagramSearcher()
        rejestry=RegistrySearcher()
        insta.search(name)
        rejestry.searchData(name)
        face=FacebookParse.FaceBookSearcher(name)
        face.getNameFromFb()
        face.searchData()
        tt=twitter2.TwitterSearch()
        tt.search(name)
        imd=IMDbSearch()
        imd.search(name)
        wik=WikiSearch()
        wik.search(name)
        self.found.extend(insta.peopleFound)
        self.found.extend(rejestry.peopleFound)
        self.found.extend(face.people)
        self.found.extend(tt.found)
        self.found.extend(imd.found)
        self.found.extend(wik.found)

name=input()
search=BigSearch()
search.BigSearch(name)
search.printData()