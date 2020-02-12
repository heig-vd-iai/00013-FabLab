build: main_window.py

%.py: %.ui
	pyuic5 $< -o $@

clean:
	$(RM) main_window.py