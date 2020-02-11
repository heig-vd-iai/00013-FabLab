build:
	pyuic5 main-window.ui -o main-window.py

clean:
	$(RM) main-window.py