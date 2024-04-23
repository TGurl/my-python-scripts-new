#!/usr/bin/env python
import os
import sys
import stat
import json


class InitPy():
    def __init__(self):
        self.cur_dir = os.getcwd()
        self.util_dir = os.path.join("/", "data", "dev", "python", "utils")
        self.colors_file = 'colors.py'
        self.utils_file = 'utils.py'

    def step_title(self, message, dot='+'):
        print(f"  {dot} {message}")

    def write_makefile(self, project_name, debug=False):
        filename = "Makefile2" if debug else 'Makefile'
        filename = os.path.join(self.cur_dir, filename)
        pname = project_name.lower() + 'core.py'

        if not os.path.exists(filename):
            self.step_title('writing makefile')
            lines = [
                    'FLAG = --onefile',
                    f'APPNAME = {project_name.lower()}\n',
                    'install: build move clean\n',
                    'build: main.py',
                    '\tpyinstaller $(FLAG) main.py\n',
                    'move:',
                    '\t@mv dist/main ~/.bin/$(APPNAME)\n',
                    'clean:',
                    '\t@if [ -a build ]; then rm -r build; fi',
                    '\t@if [ -a dist ]; then rm -r dist; fi',
                    '\t@if [ -a main.spec ]; then rm -r main.spec; fi',
                    '\t@if [ -a __pycache__ ]; then rm -r __pycache__; fi\n',
                    'uninstall:',
                    '\t@rm ~/.bin/$(APPNAME)\n',
                    'edit:',
                    f'\tnvim -p main.py {pname} utils.py colors.py'
                    ]

            with open(filename, 'w', encoding='utf-8') as makefile:
                for line in lines:
                    makefile.write(line + '\n')
        else:
            self.step_title('makefile already exists in cwd.', dot='-')

    def write_pyproject(self):
        filename = os.path.join(self.cur_dir, 'pyrightconfig.json')
        if not os.path.exists(filename):
            self.step_title('writing pyrightconfig.json')
            data = {'executionEnvironments' : [{ 'root': '.'}]}
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file)
        else:
            self.step_title('pyrightconfig.json already exists in cwd.', dot='-')

    def write_core(self, project_name, debug=False):
        project_name = project_name + 'Core'
        pname = project_name.lower()
        corepy = f"{pname}2.py" if debug else f"{pname}.py"
        s = 4 * ' '
        filename = os.path.join(self.cur_dir, corepy)
        if not os.path.exists(filename):
            self.step_title(f"writing {corepy}")
            lines = ['import os\n',
                     'from utils import TransgirlUtils\n\n',
                     f"class {project_name}(TransgirlUtils):",
                     f'{s}def __init__(self):',
                     f'{s}{s}super().__init__()\n',
                     ]

            with open(filename, 'w', encoding='utf-8') as file:
                for line in lines:
                    file.write(line + '\n')

    def write_skel(self, project_name, debug=False):
        mainpy = 'main2.py' if debug else 'main.py'
        pname = project_name + 'Core'
        corepy = pname.lower()
        s = 4 * ' '
        filename = os.path.join(self.cur_dir, mainpy)
        if not os.path.exists(filename):
            self.step_title("writing main.py")
            lines = ['#!/usr/bin/env python',
                     'import os\n',
                     f'from {corepy} import {pname}\n\n',
                     f"class {project_name}({pname}):",
                     f'{s}def __init__(self):',
                     f'{s}{s}super().__init__()\n',
                     f'{s}def run(self):',
                     f'{s}{s}print("You can start coding now, the skeleton has been erected!")',
                     f'{s}{s}print("Happy coding, you little slut!")\n\n',
                     'if __name__ == "__main__":',
                     f"{s}app={project_name}()",
                     f"{s}app.run()"
                     ]
            with open(filename, 'w', encoding='utf-8') as file:
                for line in lines:
                    file.write(line + '\n')
            rights = stat.S_IRWXU + stat.S_IRGRP + stat.S_IXGRP + stat.S_IROTH + stat.S_IXOTH
            os.chmod(filename, rights)
        else:
            self.step_title('main.py already exists in cwd.', dot='-')

    def link_utils(self):
        files = [self.colors_file, self.utils_file]
        for file in files:
            src = os.path.join(self.util_dir, file)
            dst = os.path.join(self.cur_dir, file)
            if not os.path.exists(dst):
                self.step_title(f"linking {file}")
                os.symlink(src, dst)
            else:
                self.step_title(f"{file} already symlinked in cwd.", dot='-')

    def run(self, project_name):
        self.write_makefile(project_name=project_name, debug=False)
        self.write_pyproject()
        self.write_skel(project_name=project_name, debug=False)
        self.write_core(project_name=project_name, debug=False)
        self.link_utils()
        print()
        self.step_title('Done, happy coding!', dot='!')


if __name__ == '__main__':
    print('>> Initialize Python Project <<')

    if len(sys.argv) != 2:
        print("Usage: initpy <ProjectTitle>", end='\n\n')
        print('You forgot to give me a new project title!')
        sys.exit()

    if '-h' in sys.argv:
        print("Usage: initpy <ProjectTitle>", end='\n\n')
        print('!!! Make sure you run this in the correct folder !!!')
        sys.exit()

    app = InitPy()
    app.run(sys.argv[1])
