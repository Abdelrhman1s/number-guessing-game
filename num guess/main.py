from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        diff = request.form.get("difficulty")
        if diff == "easy":
            guesses = 10
        elif diff == "medium":
            guesses = 7
        elif diff == "hard":
            guesses = 5
        else:
            return "Invalid difficulty"

        session['num'] = random.randint(1, 100)
        session['guesses'] = guesses
        session['difficulty'] = diff
        session['message'] = ""
        return redirect(url_for('game'))

    return render_template("index.html")


@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'num' not in session:
        return redirect(url_for('index'))

    message = session.get('message', '')
    guesses = session['guesses']
    win = False
    lose = False

    if request.method == 'POST':
        try:
            guess = int(request.form.get('guess'))
        except:
            session['message'] = "Invalid input! Please enter a number."
            return redirect(url_for('game'))

        if guess < 1 or guess > 100:
            session['message'] = "Invalid input! Guess between 1 and 100."
        elif guess == session['num']:
            session['message'] = "Correct 🎉"
            win = True
        else:
            session['guesses'] -= 1
            if session['guesses'] == 0:
                lose = True
                session['message'] = f"You lose, the number was {session['num']}."
            elif guess < session['num']:
                session['message'] = "Too low"
            else:
                session['message'] = "Too high"

        return redirect(url_for('game'))

    return render_template("game.html", 
                           message=session['message'],
                           guesses=session['guesses'],
                           win=(session['message'] == "Correct 🎉"),
                           lose=("lose" in session['message']))


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
