FLAG = --onefile
APPNAME = puta

install: build move clean

build: main.py
	pyinstaller $(FLAG) main.py

move:
	@mv dist/main ~/.bin/$(APPNAME)

clean:
	@if [ -a build ]; then rm -r build; fi
	@if [ -a dist ]; then rm -r dist; fi
	@if [ -a main.spec ]; then rm -r main.spec; fi
	@if [ -a __pycache__ ]; then rm -r __pycache__; fi

uninstall:
	@rm ~/.bin/$(APPNAME)

edit:
	nvim -p main.py core.py config.py progressbar.py
