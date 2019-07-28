#!C:\Users\Wojtek\PycharmProjects\scrap\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'linkedin-scraping==0.1.2','console_scripts','linkscrap'
__requires__ = 'linkedin-scraping==0.1.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('linkedin-scraping==0.1.2', 'console_scripts', 'linkscrap')()
    )
