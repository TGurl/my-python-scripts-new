import os
from pathlib import Path

class Database:
    def __init__(self):
        self.categories = 'categories.db'
        self.urls = 'urls.db'
    
    def preflight_checks(self):
        if not os.path.exists(self.categories):
            Path(self.categories).touch()
        if not os.path.exists(self.urls):
            Path(self.urls).touch()

    def add_category(self, category:str):
        with open(self.categories, 'a', encoding='utf-8') as db:
            db.write(f"{category}\n")

    def add_url(self, title:str, category:int, url: str):
        pass

    def fetch_categories(self):
        alist = [line.strip() for line in open(self.categories)]
        return alist

    def check_categories(self, needle:str):
        categories = self.fetch_categories()
        found = False
        for category in categories:
            if category.lower() == needle.lower():
                found = True
        return found
