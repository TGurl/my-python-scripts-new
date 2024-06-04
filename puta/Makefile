FLAG = --onefile
APPNAME = arc

install: build move clean

build: main.py
	@echo "BUILD: Start..."
	pyinstaller $(FLAG) main.py
	@echo "BUILD: Done"

move:
	@echo "MOVE: Start..."
	@mv dist/main ~/.bin/$(APPNAME)
	@echo "MOVE: DONE"

clean:
	@echo "CLEAN: Starting"
	@if [ -a build ]; then rm -r build; fi;
	@if [ -a dist ]; then rm -r dist; fi;
	@if [ -a main.spec ]; then rm -r main.spec; fi;
	@if [ -a __pycache__ ]; then rm -r __pycache__; fi;
	@echo "CLEAN: Done";

uninstall:
	@echo "UNINSTALL: $(APPNAME)"
	@rm ~/.bin/$(APPNAME)
	@echo "UNINSTALL: Done";

edit:
	nvim -p main.py core.py
