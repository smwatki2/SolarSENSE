from flask import render_template, redirect, url_for, session
from app import app
from app.forms import HomeForm
# from app.forms import QuestionForm

@app.route("/", methods=['GET','POST'])
# @app.route("/match")
def home():
	form = HomeForm()
	if form.validate_on_submit():
		if form.survey.data:
			print(form.username.data)
			session['username'] = form.username.data
			print("There is a session with username {}".format(session['username']))
			return redirect(url_for('survey'))
		elif form.match.data:
			print(form.username.data + 'found a match')
			return redirect(url_for('match'))
	return render_template('home.html', form=form)

@app.route("/survey")
def survey():
	# if form.validate_on_submit():
	# 	if form.survey.data:
	# 		return 'Survey has begun for user {}'.format(form.username.data);
	return render_template('test.html', username = session['username'] + ' is pretty cool I guess')

@app.route("/match")
def match():
	return render_template('test.html', username=session['username'] + ' is an awesome match')

# def match():
# 	return form.username.data + 'has matched'