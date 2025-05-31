from flask import Flask,render_template,redirect,url_for,request,flash,session
from flask_session import Session
from otp import gen_otp
from cmail import send_mail
from stoken import entoken,detoken
import mysql.connector 
app=Flask(__name__)
app.config['SESSION_TYPE']='filesystem'
app.secret_key='dineshkey'
Session(app)
# user_data={'dinesh':{'email':'dinesh.rcnd@gmail.com','password':'123'}}
userdata={}
mydb=mysql.connector.connect(user='root',host='localhost',password='admin',db='snmp') #Mysql connection

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=str(request.form['uname'])
        email=request.form['email']
        password=str(request.form['pwd'])
        cursor=mydb.cursor()
        cursor.execute('select count(email) from users where email=%s',[email])
        emailcount=cursor.fetchone() # returns single element in tuple form (1)
        if emailcount[0]==0:
            otp=gen_otp()
            userdata={'user_name':username,'user_email':email,'user_password':password,'otp':otp}
            print(userdata)
            subject=f'Verification mail for SNM project'
            body=f'OTP for SNM Register Verify {otp}'
            send_mail(to=email,subject=subject,body=body)
            flash(f'The OTP has been sent to given {email} email')
            print(otp)
            return redirect(url_for('otpverify',user_data=entoken(data=userdata))) #For encrypting otp we used entoken
        elif emailcount[0]==1:
            flash('Email already exists')
        else:
            return f'Something went wrong'
        # if username not in user_data:
        #     user_data[username]={'email':email,'password':password}
        #     return redirect(url_for('login'))
        # else:
        #     return 'user already exists' and redirect(url_for('login'))
    return render_template('register.html')

@app.route('/otpverify/<user_data>',methods=['GET','POST'])
def otpverify(user_data):
    if request.method=='POST':
        userotp=request.form['userotp']
        duser_data=detoken(data=user_data) #Decrypted user_data
        # userdata={'user_name':username,'user_email':email,'user_password':password,'otp':otp}
        #We need to check whether userotp is same as serverotp
        if userotp==duser_data['otp']:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into users(username,email,password) values(%s,%s,%s)',[duser_data['user_name'],duser_data['user_email'],duser_data['user_password']])
            mydb.commit()
            cursor.close()
            return redirect(url_for('login'))
        else:
            flash('INVALID OTP')

    return render_template('otpverify.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        useremail=request.form['email']
        userpassword=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(email) from users where email=%s',[useremail])
        count_email=cursor.fetchone()
        if count_email[0]==1:
            cursor.execute('select password from users where email=%s',[useremail])
            stored_password=cursor.fetchone()
            if userpassword==stored_password[0]:
                session['user']=useremail
                print(session)
                flash('Login Successful')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid Password')
        elif count_email[0]==0:
            flash('Invalid user. User not found in database')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/addnotes',methods=['GET','POST'])
def addnotes():
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(nid) from notes')
        nid_count=cursor.fetchone()
        if nid_count:
            nid=nid_count[0]+1
            cursor.execute('insert into notes(nid,title,description,added_by) values(%s,%s,%s,%s)',[nid,title,description,session.get('user')])
            mydb.commit()
            cursor.close()
            flash(f'notes {title} added successfully')
            return redirect(url_for('viewallnotes'))
        else:
            flash('nid not found')
            return redirect(url_for('dashboard'))
    return render_template('addnotes.html')

@app.route('/viewallnotes')
def viewallnotes():
    cursor=mydb.cursor()
    cursor.execute('select nid,title,created_at from notes where added_by=%s',[session.get('user')])
    allnotesdata=cursor.fetchall()
    cursor.close()
    return render_template('viewallnotes.html',allnotesdata=allnotesdata)

# For Single notes
@app.route('/viewnotes/<nid>')
def viewnotes(nid):
    cursor=mydb.cursor()
    cursor.execute('select * from notes where nid=%s and added_by=%s',[nid,session.get('user')])
    notesdata=cursor.fetchone()
    return render_template('viewnotes.html',notesdata=notesdata)


app.run(use_reloader=True,debug=True)

