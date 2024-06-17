import os

from config import Config
from pyfzf.pyfzf import FzfPrompt


class Core:
    def __init__(self):
        pass

    def expand_folder(self, folder:str) -> str:
        return os.path.expanduser(folder)

    def collect_stories(self) -> list:
        stories = []
        blacklist = ['.md_', '.bak', '.backup', '.txt']
        folder = self.expand_folder(Config.stdir)
        for entry in os.scandir(folder):
            _, ext = os.path.splitext(entry.name)
            if "_notes" in entry.name or not entry.is_file() or 'snip' in entry.name:
                continue
            if '.md' in entry.name and ext not in blacklist:
                stories.append(entry.path)
        stories.sort()
        return stories

    def select_story(self):
        stories = self.collect_stories()
        story = FzfPrompt().prompt(stories, '--reverse --exact')
        if story:
            self.open_story(story[0])

    def open_story(self, filename:str):
        gn = os.path.join(self.expand_folder(Config.stdir), Config.globalnotes)
        notes = filename.replace('.md', '_notes.md')
        os.system(f'vim -p -n + {filename} {notes} {gn}')

