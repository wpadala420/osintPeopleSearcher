# -*- coding: utf-8 -*-
import json
import os
import dpath.util
import tablib
from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from .items import User
from parser import strip_tags


class LinkedInPeopleSpider(InitSpider):
    name = 'LinkedInPeopleSpider'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    dataset = None

    def __init__(self, username='', password='', keyword='', *args, **kwargs):
        super(LinkedInPeopleSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["https://www.linkedin.com/vsearch/fj?keywords={}".format(keyword)]
        self.username = username
        self.password = password

    def init_request(self):
        # This function is called before crawling starts.
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        # Generate a login request.
        return FormRequest.from_response(
            response,
            formdata={'session_key': self.username, 'session_password': self.password},
            callback=self.check_login_response
        )

    def check_login_response(self, response):
        # Check the response returned by a login request to see if we aresuccessfully logged in.
        if "Sign Out" in response.body:
            self.log("\n\n\nSuccessfully logged in. Let's start crawling!\n\n\n")
            # Now the crawling can begin.
            return self.initialized()
        else:
            # Something went wrong, we couldn't log in, so nothing happens.
            self.log("\n\n\nFailed, Bad times :(\n\n\n")
            print self.username
            print "Login failed!"

    def make_dataset(self):
        self.dataset = tablib.Dataset()
        self.dataset.headers = ["first_name", "last_name", "position", "company", "city", "country"]

    def parse(self, response):
        self.log("\n\n\n We got data! \n\n\n")
        self.make_dataset()
        json_response = json.loads(response.body)
        f = open(os.getcwd() + '/linkedin_users.csv', 'w')
        for person in dpath.util.get(json_response, '/content/page/voltron_unified_search_json/search/results'):

            # Try to get the person dict -> continue if not found
            try:
                person_dict = dpath.util.get(person, "/person")
            except:
                continue

            item = User(
                first_name=person_dict.get("firstName", "LinkedIn"),
                last_name=person_dict.get("lastName", "Member"),
            )

            # Try to split the position and company
            if person_dict.get("fmt_headline", None):
                position_company = strip_tags(person_dict["fmt_headline"])
                if " bei " in position_company:
                    position_company = position_company.partition(" bei ")
                else:
                    position_company = position_company.partition(" at ")
                item['position'] = position_company[0]
                item['company'] = position_company[2]

            if person_dict.get("fmt_location", None):
                city_country = person_dict["fmt_location"]
                if " und Umgebung," in city_country:
                    location = person_dict["fmt_location"].partition(" und Umgebung,")
                else:
                    location = person_dict["fmt_location"].partition(" Area,")
                item['city'] = location[0]
                item["country"] = location[2]

            self.dataset.append([item.get(field) for field in self.dataset.headers])
        f.write(self.dataset.csv)
        print("File generated at: {}".format(os.path.abspath(f.name)))
