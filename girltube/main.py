#!/usr/bin/env python
from database import Database

class GirlTube:
    def __init__(self):
        self.db = Database()

    def run(self):
        self.db.preflight_checks()
        category = input('New category : ')

        if not self.db.check_categories(category):
            self.db.add_category(category)
            print(category, 'added')
        else:
            print(category, 'already existed')


if __name__ == '__main__':
    app = GirlTube()
    app.run()
