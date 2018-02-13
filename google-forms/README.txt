Pre-requisites:
1. Python 2.7 installation
	https://www.youtube.com/watch?v=hoc8TK96WoY
2. Selenium
	Please open command prompt, and run:
		pip install selenium
3. Requests
	Please open command prompt, and run:
		pip install requests
4. LXML
	Please open command prompt, and run:
		pip install lxml
5. Firefox
	https://www.mozilla.org/en-US/firefox/new/
6. Knowledge of how to run a script through cmd
	3.1. How to open a directory in command prompt
		https://www.youtube.com/watch?v=sjaCgavMO18
	3.2. How to open command prompt in any folder
		https://www.youtube.com/watch?v=f0AVu21qfz8
7. File with emails. Please open emails.csv and enter one email per line into the file. The program will use these emails while filling the forms. Ensure that the number of emails here exceed the number of times you want to fill the forms.

<-------------------DO NOT PROCEED UNTIL YOU HAVE EVERYTHING INSTALLED----------------------------->


How to execute the script:
1. Ensure that all pre-requisites are installed.
2. Open the folder with the script formfiller.py
3. Open command prompt in that directory
4. Run the script with:
	python formfiller.py
5. When prompted, enter the number of times you want to fill the form.
6. The program will automatically fill the number of times you've chosen.
7. The log is stored in log.csv
