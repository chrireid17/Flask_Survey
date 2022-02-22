from this import s
from flask import Flask, request, render_template, redirect, flash
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home_page():
    """Show the survey with survey instructions"""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('home.html', title=title, instructions=instructions)


@app.route('/questions/<int:question_id>')
def show_question(question_id):
    """Show the question with given integer id"""

    if len(responses) == len(satisfaction_survey.questions):
        flash('Invalid Question, Cannot Access')
        return redirect('/thanks')

    if question_id != len(responses):
        flash('Invalid Question, Cannot Access')
        return redirect(f'/questions/{len(responses)}')

    question = satisfaction_survey.questions[question_id].question
    answers = satisfaction_survey.questions[question_id].choices

    return render_template('question.html', question=question, answers=answers)


@app.route('/answers', methods=['POST'])
def handle_answer():
    """Save answer to response list and redirect to next question"""

    responses.append(request.form['answer'])
    next_question = len(responses)

    if next_question == len(satisfaction_survey.questions):
        return redirect('/thanks')

    return redirect(f'/questions/{next_question}')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')
