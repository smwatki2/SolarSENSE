This matchmaker works kinda like Lab 3 of 421, those who are in it will understand.
Now this does closley resemble what Scott has pushed up in regards to the websever.
However this implements a little routing and keeps to separation of concern.

To use make sure to be in the main directory, this application does utilize a virtual environment
from python 3. 

To run:

	Be in main MatchMaker Folder

	source mmvirtualenv/bin/activate  <-- This will activate the virtual environment in python

	export FLASK_APP=matchmaker.py

	flask run

	if fails to run make sure to have following pacakges installed:
	pip install flask
	pip install flask_wtf

	after flask run, application should begin listening on

	localhost:5000

	

