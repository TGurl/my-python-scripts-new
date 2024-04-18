FLAG = --onefile
APPNAME = fetch

install: build clean

build: main.py
	@echo "--> Building app"
	pyinstaller $(FLAG) main.py
	@echo "--> Moving app"
	@mv dist/main ~/.bin/$(APPNAME)
	@printf ">> Done\n";

clean:
	@echo "--> Cleaning folder"
	@if [ -a build ]; then rm -r build; fi;
	@if [ -a dist ]; then rm -r dist; fi;
	@if [ -a main.spec ]; then rm -r main.spec; fi;
	@if [ -a __pycache__ ]; then rm -r __pycache__; fi;
	@printf ">> Done\n";

uninstall:
	@echo "--> Removing $(APPNAME)"
	@rm ~/.bin/$(APPNAME)
	@printf ">> Done\n"
