#!/usr/bin/env python
import os
import sys
import json
import readchar

from utils import TransgirlUtils
from time import sleep


class Storyteller(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.appname = 'Storyteller'
        self.appwidth = 65
        self.config = os.path.expanduser(os.path.join("~", ".config", "transgirl", "storyteller.json"))
        self.story_folder = os.path.expanduser(os.path.join("~", "stories"))

    def load_config(self):
        with open(self.config, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def save_config(self, data):
        with open(self.config, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

    def banner(self, slogan=False):
        self.show_title(appname=self.appname, width=self.appwidth)
        if slogan:
            self.cprint(self.random_slogan(), new_line=True, width=self.appwidth)

    def exit_gracefully(self):
        self.banner()
        self.default_message("Was it a good story? Did you masturbate? You whore!")
        sys.exit()

    def collect_all_stories(self) -> list:
        library = []
        for entry in os.scandir(self.story_folder):
            _, ext = os.path.splitext(entry.name)
            if ext == ".md" and not "_notes" in entry.name and entry.name != 'snippets.md':
                library.append(entry.path)
        library.sort()
        return library

    def edit_story(self, story_id, continue_story=False):
        config = self.load_config()
        if not continue_story:
            config['last_edited'] = story_id - 1
            self.save_config(config)

        global_notes = os.path.join(self.story_folder, 'global_notes.md')
        snippets = os.path.join(self.story_folder, 'snippets.md')
        library = self.collect_all_stories()
        story = library[story_id - 1]
        notes = story.replace('.md', '_notes.md')
        os.system(f"vim -p + {story} {notes} {global_notes} {snippets}")

    def continue_last_story(self):
        config = self.load_config()
        self.edit_story(config['last_edited'], continue_story=True)

    def start_a_new_story(self):
        config = self.load_config()
        global_notes = os.path.join(self.story_folder, 'global_notes.md')
        snippets = os.path.join(self.story_folder, 'snippets.md')

        self.banner()
        msg = self.colorize('%y>>%R What title did you have in mind? : ')
        story_title = input(msg)
        if story_title == '':
            story_title = 'working title'
            self.printr("Couldn't come up with a good title, could you? Stupid cow!")
            sleep(1.5)
            self.clear_lines()
        new_story_content = [
                f'# {story_title.title()}\n',
                '_an erotic tale by Transgirl_\n\n',
                '---\n\n',
                '_This is a work of fiction. Any resemblance to any person living or dead is_\n',
                '_purely coincidental. All characters are presumed to be of legal age. It is_\n',
                '_also presumed all sexual acts are consensual and/or legal._\n\n',
                '---\n\n',
                '## Chapter One\n\n'
                ]
        new_notes_content = [
                f'# Notes For {story_title.title()}\n\n',
                'place your story notes here...\n'
                ]
        story_file = story_title.lower().replace(' ', '_') + '.md'
        notes_file = story_file.replace('.md', '_notes.md')

        story_path = os.path.join(self.story_folder, story_file)
        notes_path = os.path.join(self.story_folder, notes_file)
        with open(story_path, 'w', encoding='utf-8') as story:
            for line in new_story_content:
                story.write(line)

        with open(notes_path, 'w', encoding='utf-8') as notes:
            for line in new_notes_content:
                notes.write(line)
        config['last_edited'] += 1
        self.save_config(config)
        os.system(f"vim -p + {story_path} {notes_path} {global_notes} {snippets}")

    def delete_a_story(self):
        while True:
            library = self.collect_all_stories()
            if not library:
                config = self.load_config()
                config['last_edited'] = -1
                self.save_config(config)
                break
            total_stories = len(library)
            indent = len(str(total_stories))
            keys_allowed = ['r']
            self.banner()
            self.printr('Which story do you want to delete?', new_line=True)
            for idx, story in enumerate(library, start=1):
                story_title = story.split('/')[-1].replace(".md", "").replace("_", " ").title()
                nl = True if idx == total_stories else False
                self.printr(f"[%g{idx:{indent}}%R] {story_title}", new_line=nl)
                keys_allowed.append(str(idx))
            spaces = (indent - 1) * ' '
            self.printr(f"[%r{spaces}r%R] Return to main menu", new_line=True)
            print(self.colorize('%y>>%R '), end='', flush=True)

            key = readchar.readchar().lower()
            if key not in keys_allowed:
                print('')
                self.clear_lines()
                self.error_message("That's the wrong key, you cunt!", dot='!')
                sleep(1.5)
            elif key == 'r':
                break
            else:
                sid = int(key) - 1
                config = self.load_config()
                print(sid, config['last_edited'])
                if sid == config['last_edited']:
                    config['last_edited'] = -1
                    self.save_config(config)

                story = library[sid]
                notes = story.replace('.md', '_notes.md')
                os.remove(story)
                os.remove(notes)
                break

    def edit_global_notes(self):
        notes = os.path.join(self.story_folder, 'global_notes.md')
        os.system(f"vim + {notes}")

    def edit_snippets(self):
        snippets = os.path.join(self.story_folder, 'snippets.md')
        os.system(f"vim + {snippets}")

    def show_menu(self):
        while True:
            config = self.load_config()
            library = self.collect_all_stories()
            if config['last_edited'] != -1:
                last_edited = library[config['last_edited']].split('/')[-1].replace('.md', '').title()
            else:
                last_edited = ''
            total_stories = len(library)
            indent = len(str(total_stories))
            keys_allowed = ['q', 'n', 'd', 'g', 's']
            self.banner()
            self.default_message("What is it you want to do, slut?", new_line=True)
            for idx, story in enumerate(library, start=1):
                story_title = story.split('/')[-1].replace(".md", "").replace("_", " ").title()
                nl = True if idx == total_stories else False
                self.printr(f"[%g{idx:{indent}}%R] {story_title}", new_line=nl)
                keys_allowed.append(str(idx))

            spaces = (indent - 1) * ' '
            if config['last_edited'] != -1:
                keys_allowed.append('c')
                self.printr(f'[%g{spaces}c%R] Continue %i{last_edited}%R')
            self.printr(f'[%g{spaces}n%R] Start a new story')
            self.printr(f"[%g{spaces}d%R] Delete a story", new_line=True)
            self.printr(f'[%g{spaces}g%R] Edit global notes')
            self.printr(f'[%g{spaces}s%R] Edit snippets', new_line=True)
            self.printr(f'[%r{spaces}q%R] Quit', new_line=True)
            print(self.colorize('%y>>%R '), end='', flush=True)

            key = readchar.readchar().lower()
            if key not in keys_allowed:
                print('')
                self.clear_lines()
                self.error_message("That's the wrong key, you cunt!", dot='!')
                sleep(1.5)
            elif key == 'q':
                break
            elif key == 'n':
                self.start_a_new_story()
            elif key == 'c':
                self.continue_last_story()
            elif key == 'd':
                self.delete_a_story()
            elif key == 'g':
                self.edit_global_notes()
            elif key == 's':
                self.edit_snippets()
            else:
                self.edit_story(int(key))
        self.exit_gracefully()

    def run(self):
        self.show_menu()


if __name__ == '__main__':
    app = Storyteller()
    app.run()
