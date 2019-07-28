from twitter import *
import requests
import Person

class TwitterSearch:

    def __init__(self):
        self.found=[]


    def search(self,name):
        twitter=Twitter(auth=OAuth('1107675488498184192-hRhlVdT8qdjbeEdaxT8QTrEbPUbeRR',
                                   'QTYb9H0hlpIx40jBsxfvNmNhr0qRuNazdN7K2bmMxrLni',
                                   'jIQwToZWxWIy2BbPyGLVkpDEf',
                                   'GzTjo3ZKXxpqsVDRMMQRdRbaKi1x6M2GlvmlKighbZxSeFnNjD'))


        results = twitter.users.search(q = '"{}"'.format(name))

        for i in results:
            osoba=Person.Person()
            osoba.setName(i['name'].split(' ')[0])
            osoba.setSurname(i['name'].split(' ')[1])
            osoba.twitter['nickname']=i['screen_name']
            if i['description'] is not '':
                osoba.twitter['role']=i['description']
            osoba.twitter['url']='https://twitter.com/{}'.format(i['screen_name'])
            osoba.twitter['sites']=[]
            if 'url' in i['entities']:
                for j in i['entities']['url']['urls']:
                    osoba.twitter['sites'].append(j['expanded_url'])
            osoba.twitter['tweets']=[]
            if 'status' in i:
                tweet={}
                if 'created_at' in j['status']:
                    tweet['utworzono']=j['created_at']
                tweet['zawartosc']=j['status']['text']
                if 'user_mentions' in j:
                    tweet['wspomniane_osoby']=[c['screen_name'] for c in j['user_mentions']]
                osoba.twitter['tweets'].append(tweet)
            if 'profile_image_url_https' in i:
                osoba.twitter['profile_image_url']=i['profile_image_url_https']
            self.found.append(osoba)



