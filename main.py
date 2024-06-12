from flask import Flask, render_template, request
import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

# Debugging: Print the values to check if they are loaded correctly
print(f'Loaded email: {email}')
print(f'Loaded password: {password}')

# Check if email and password are loaded properly
if not email or not password:
    raise ValueError("EMAIL and PASSWORD must be set in the .env file")

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        sender_email = data["email"]
        mobile = data["phone"]
        msg = data["message"]
        message = f"Subject:Contact Form: \n\nname: {name}\nemail: {sender_email}\nmobile: {mobile}\nmessage: {msg}\n"

        try:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=email, password=password)
                connection.sendmail(from_addr=email, to_addrs="lokeshcoder123@gmail.com", msg=message)
                print(f'Email sent successfully to lokeshcoder123@gmail.com')
        except Exception as e:
            print(f'Failed to send email: {e}')

        print(name, sender_email, mobile, msg)
        return render_template("contact.html", msg=data)
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=False)
