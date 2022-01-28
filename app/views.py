import os

from app import app
from app import camera_views
from flask import render_template
from flask import request, redirect
from flask import jsonify, make_response, Response

from werkzeug.utils import secure_filename
from flask import send_file, send_from_directory, safe_join, abort
from flask import flash



from datetime import datetime

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


users = {
        "mitsuhiko": {
            "name": "Armin Ronacher",
            "bio": "Creatof of the Flask framework",
            "twitter_handle": "@mitsuhiko"
            },
        "gvanrossum": {
            "name": "Guido Van Rossum",
            "bio": "Creator of the Python programming language",
            "twitter_handle": "@gvanrossum"
            },
        "elonmusk": {
            "name": "Elon Musk",
            "bio": "technology entrepreneur, investor, and engineer",
            "twitter_handle": "@elonmusk"
            }
        }
@app.route("/test-page")
def test_page():
    return render_template("public/test_page.html")

@app.route("/")
def index():
    return render_template("public/index.html")



@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/jinja")
def jinja():
    my_name = "Till"
    my_age: int = 30
    
    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C"]
    
    # Dictonaries
    friends = {
        "Tony": 43,
        "Cody": 28,
        "Amy": 26,
        "Clarissa": 23,
        "Wendell": 39
    }
    
    # Tuples
    colors = ("Red", "Blue")
    
    # Booleans
    cool = True
    
    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description 
            self.domain = domain
            
        def pull(self):
            return f"Pulling repo '{self.name}'"
        
        def clone(self, repo):
            return f"Cloning into {repo}"
        
    my_remote = GitRemote(
    name="Learning Flask",
    description="Learn the Flask web framework for Python",
    domain="https://github.com/Julian-Nash/learning-flask.git"
    )
    
    # Functions
    def repeat(x, qty=1):
        return x * qty
    
    date = datetime.utcnow()
    
    my_html = "<h1>This is some HTML</h1>"
    
    suspicious = "<script>alert('NEVER TRUST USER INPUT!')</script>"
    
    return render_template(
    "public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
    friends=friends, colors=colors, cool=cool, GitRemote=GitRemote, 
    my_remote=my_remote, repeat=repeat, date=date, my_html=my_html, 
    suspicious=suspicious
    )
    
    @app.template_filter("clean_date")
    def clean_date(dt):
        return dt.strftime("%d %b %Y")
    
@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        
        req = request.form
        
        username = req.get("username")
        email = req.get("email")
        password = req.get("password")
        
        if not len(password) >= 10:
            flash("Password length must be at least 10 characters", "warning")
            return redirect(request.url)
        
        flash("Account created", "success")
        return redirect(request.url)
        
    return render_template("public/sign_up.html")

@app.route("/profile/<username>")
def profile(username):
    
    user = None
    
    if username in users:
        user = users[username]
    
    return render_template("public/profile.html", username=username, user=user)


@app.route("/json", methods=["POST"])
def json_example():
    
    if request.is_json:
        req = request.get_json()
        response_body = {
        "message": "JSON received!",
        "sender": req.get("name")
        }
        res = make_response(jsonify(response_body), 200)
        
        return res
    
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}),
        400)
        
@app.route("/guestbook")
def guestbook():
    
    print(app.config["SECRET_KEY"])
    return render_template("public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():
    
    req = request.get_json()
    
    print(req)
    
    res = make_response(jsonify(req), 200)
    return res


@app.route("/query")
def query():
    args = request.args
    
    for k, v in args.items():
        print(f"{k}: {v}")
    
    
    return "no query string recieved", 200



def allowed_image(filename):
    # We only want files with a . in the filename
    if not "." in filename:
        return False
    
    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]
    
    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/upload-image", methods=["GET","POST"])
def upload_img():
    
    if request.method == "POST":
        if request.files:
            
            image = request.files["image"]
            
            if image.filename == "":
                print("No filename")
                return redirect(request.url)
            
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("image saved")
            else:
                print(f"File extention was not allowed. Allowed extentions: {app.config['ALLOWED_IMAGE_EXTENTIONS']}")
            return redirect(request.url)
    
    return render_template("public/upload_image.html")


@app.route("/get-image/<image_name>")
def get_image(image_name):    
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], path=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)
        
@app.route("/get-csv/<csv_id>")
def get_csv(csv_id):
    
    path = f"{csv_id}.csv"
    
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], path=path, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get-pdf/<pdf_id>")
def get_pdf(pdf_id):
    
    path = f"{pdf_id}.csv"
    
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], path=path, as_attachment=True)
    except FileNotFoundError:
        abort(404)
        
@app.route("/cookies")
def cookies():
    
    resp = make_response("Cookies")
    resp.set_cookie(
        "flavor",
        value="chocolate chip",
        max_age=10,
        path=request.path
        )
    
    resp.set_cookie("chocolate type", "dark")
    resp.set_cookie("chewy", "yes")
    
    print(request.cookies)
    
    return resp