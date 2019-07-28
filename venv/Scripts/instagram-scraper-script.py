#!C:\Users\Wojtek\PycharmProjects\scrap\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'instagram-scraper==1.5.41','console_scripts','instagram-scraper'
__requires__ = 'instagram-scraper==1.5.41'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('instagram-scraper==1.5.41', 'console_scripts', 'instagram-scraper')()
    )
