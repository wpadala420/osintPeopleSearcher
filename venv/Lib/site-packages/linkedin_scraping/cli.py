# -*- coding: utf-8 -*-
import click
from .crawler import process
from .spider import LinkedInPeopleSpider


@click.command()
@click.option('-u', prompt='LinkedIn E-Mail', help='Username used for LinkedIn authentication.')
@click.option('-p', prompt='LinkedIn Password', help='Password used for LinkedIn authentication.', hide_input=True,
              confirmation_prompt=False)
@click.option('-k', prompt='Search keyword', help='The search keyword, used for searching on LinkedIn.',
              default="fuhrparkleiter")
def main(u, p, k):
    # Save the username and Password in a global variable
    process.crawl(LinkedInPeopleSpider, username=u, password=p, keyword=k)
    process.start()
