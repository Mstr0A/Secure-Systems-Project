import bcrypt
from dotenv import load_dotenv
from flask_session import Session
from db.connection import get_db_connection
from flask import Flask, request, session, render_template, redirect

load_dotenv()


app = Flask(__name__)

# Session setup
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if session.get("username"):
            # Fetch the data needed if a session exists, otherwise continue with a normal login

            return render_template("logged.html", username=session.get("username"))

        try:
            form_username = request.form["username"]
            form_password = request.form["password"]

            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            query = "SELECT `password_hash` FROM `users` WHERE `username` = %s"
            values = (form_username,)

            cursor.execute(query, values)
            result = cursor.fetchone()

            if not result:
                return render_template(
                    "error.html", error="Username or password incorrect"
                )

            match = bcrypt.checkpw(
                form_password.encode(), result["password_hash"].encode()
            )

            # If the passwords dont match
            if not match:
                return render_template(
                    "error.html", error="Username or password incorrect"
                )

            # Set the session if a match
            session["username"] = form_username

            # If they match we do another query to fetch the stuff we need but here we dont need much

            return render_template("logged.html", username=form_username)

        except Exception as e:
            cursor.close()
            connection.close()
            return f"<h1>ERROR</h1><pre>{str(e)}</pre>", 500

        finally:  # Close everything in the end
            try:
                cursor.close()
                connection.close()
            except Exception:
                pass

    else:  # GET request
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Get the form info
        form_username = request.form["username"]
        form_password = request.form["password"]

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            query = "SELECT `password_hash` FROM `users` WHERE `username` = %s"
            values = (form_username,)

            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                return render_template(
                    "error.html", error="A user with that name already exists"
                )

            # Generate the passowrd hash to be stored
            form_password_hash = bcrypt.hashpw(form_password.encode(), bcrypt.gensalt())

            query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
            values = (form_username, form_password_hash)
            cursor.execute(query, values)
            connection.commit()

            return render_template("signed.html")
        except Exception as e:
            cursor.close()
            connection.close()
            return f"<h1>ERROR</h1><pre>{str(e)}</pre>", 500

        finally:  # Close everything in the end
            try:
                cursor.close()
                connection.close()
            except Exception:
                pass
    else:  # GET request
        return render_template("signup.html")


@app.route("/logout", methods=["GET"])
def logout():
    # Check if a session exists, if so, clear it
    if session.get("username"):
        session["username"] = None

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
