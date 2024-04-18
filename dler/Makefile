APPNAME = dler
FLAGS = --onefile --name $(APPNAME)

install: build move clean

build: main.py
	@echo "BUILD: Start..."
	pyinstaller $(FLAGS) main.py
	@echo "BUILD: Done"

move:
	@echo "MOVE: Start..."
	@mv dist/$(APPNAME) ~/.bin/
	@echo "MOVE: DONE"

clean:
	@echo "CLEAN: Starting"
	@if [ -a build ]; then rm -r build; fi;
	@if [ -a dist ]; then rm -r dist; fi;
	@if [ -a $(APPNAME).spec ]; then rm -r $(APPNAME).spec; fi;
	@if [ -a __pycache__ ]; then rm -r __pycache__; fi;
	@echo "CLEAN: Done";

uninstall:
	@echo "UNINSTALL: $(APPNAME)"
	@rm ~/.bin/$(APPNAME)
	@echo "UNINSTALL: Done";

edit:
	nvim -p main.py utils.py colors.py
