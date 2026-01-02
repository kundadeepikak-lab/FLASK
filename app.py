from flask import Flask,render_template,request,redirect,url_for,flash,make_response,session
from werkzeug.utils import secure_filename
import os

#application setup
app=Flask(__name__)
app.secret_key="secret123"

#configure folder to store uploaded files
app.config["UPLOAD_FOLDER"]='uploads'

#create upload folder if doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    
#home page route
@app.route('/')
def home():
    return render_template('home.html')

#variables route
@app.route('/hello/<name>')
def hello(name):
    return f"Hello(name),welcome to flask!"

#login route
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        session['user']=username
        flash("Login successful")
        return redirect(url_for('dashboard'))
    return render_template('login.html')

#dashboard route
@app.route('/dashboard')
def dashboard():
    user=session.get('user')
    return render_template('dashboard.html',user=user)

#logout route
@app.route('/logout')
def logout():
    session.pop('user',None)
    flash('Logged out successfully')
    return redirect(url_for('home'))

#set cookie route
@app.route('/set-cookie')
def set_cookie():
    response=make_response("cookie has been set")
    response.set_cookie('course','Flask')
    return response

#get google route
@app.route('/get-cookie')
def get_cookie():
    course=request.cookies.get('course')
    return f"Cookie value is:{course}"

#file upload route
@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method=="POST":
        file=request.files.get("file")
        if not file or file.filename=="":
            flash("No file selected","error")
            return redirect(url_for('upload'))
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
        flash("File uploaded successfully!","success")
        return redirect(url_for("upload"))
    
    #render upload request page for get request
    return render_template("upload.html")

#error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

#run server
if __name__=="__main__":
    app.run(debug=True)