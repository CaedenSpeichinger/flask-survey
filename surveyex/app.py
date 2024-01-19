from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/')
def show_survey_start():
    """show survey and allow the user to select it """

    return render_template("start.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    """starts the survey and sets it empty to reset it"""
    
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/questions/<int:que>")
def show_question(que):
    """displays question"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # if the responce is none then they are redirected to the home page
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # when they finish all the quests then send them to the thankyou page
        return redirect("/thankyou")

    if (len(responses) != que):
        # when they answer the wrong questions and try to jump around
        flash(f"Invalid question id: {que}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[que]
    return render_template(
        "question.html", question_num=que, question=question)
    
@app.route("/answer", methods=["POST"])
def handle_question():
    
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/thankyou")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/thankyou")
def complete():
    """creates a new page to thank them for the survey"""

    return render_template("thankyou.html")

if __name__ == '__main__':
    app.run()
    
