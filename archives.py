import requests

class ArchiveSearcher:

    def __init__(self):
        self.links=[]
        self.tags=[]


    def search(self,name):
        url='https://archive.org/advancedsearch.php?q={}+{}&fl%5B%5D=identifier&sort' \
            '%5B%5D=&sort%5B%5D=&sort%5B%5D=&rows=50&page=1&output=json&save=yes'.format(name.split(' ')[0], name.split(' ')[1])

        result=requests.get(url).json()
        for i in result['response']['docs']:
            link='https://www.archive.org/details/{}'.format(i['identifier'])
            self.links.append(link)



s=ArchiveSearcher()
s.search('Andrzej Duda')
for i in s.links:
    print(i)