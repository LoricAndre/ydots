.PHONY: install

install: pyinstaller ydots.py
	pyinstaller ydots.py --onefile --noconsole --distpath /usr/local/bin

pyinstaller:
	pip install pyinstaller
