-----------------------------------------------------------------------------------------
|											|	
|			       Amazon Seller Central Bot				|
|				       v 1.00						|
|											|
-----------------------------------------------------------------------------------------

Bot Functionality:
1. Opens up Amazon Seller Central.
2. Pauses for 90 seconds for the operator to login and complete recaptcha, phone verification etc.
3. Goes to messages and sets filter to "All Messages".
4. Opens each chat.
5. If chat has already been scraped, it skips and goes to the next one.
6. If chat has not been scraped, it adds info to the csv file.


How to install:
1. Check if you have python installed already.
	Go to terminal/command prompt and run python -V
	If there's an output telling the version details as 2.7.xx skip steps 
2. Install python 2.7.(please google for a solution on your operating system)
3. Open terminal/command prompt and run the following command:
	pip install selenium
4. If on windows, double click scraper.py to run the bot. On linux/mac, please open terminal
in the current folder and run:
	python scraper.py

In case you face any issues please let me know! I'll be happy to assist you with any extra
revisions/changes that you'd like. 
