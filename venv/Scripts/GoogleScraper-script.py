#!C:\Users\Wojtek\PycharmProjects\scrap\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'GoogleScraper==0.2.4','console_scripts','GoogleScraper'
__requires__ = 'GoogleScraper==0.2.4'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('GoogleScraper==0.2.4', 'console_scripts', 'GoogleScraper')()
    )
