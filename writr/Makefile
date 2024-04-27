FLAG = --onefile
APPNAME = writr

install: copy clean

copy: main.py
	@cp main.py ~/.bin/$(APPNAME)

clean:
	@if [ -a __pycache__ ]; then rm -r __pycache__; fi

uninstall:
	@rm ~/.bin/$(APPNAME)

edit:
	nvim -p main.py colors.py
