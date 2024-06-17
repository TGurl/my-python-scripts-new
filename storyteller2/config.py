import os

class Config:
    title = 'StoryTeller - The slutty generation'
    version = '0.1'
    build = '20240609'
    stdir = os.path.join('~', 'stories')
    current = ''
    globalnotes = 'global_notes.md'
    snippets = 'snippets.md'
    configpath = os.path.join('~', '.config', 'transgirl', 'storyteller.yaml')
