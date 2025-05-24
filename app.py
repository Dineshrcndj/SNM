from flask import Flask,render_template,redirect,url_for,request,flash
from otp import gen_otp
from cmail import send_mail
app=Flask(__name__)
app.secret_key='dineshkey'
# user_data={'dinesh':{'email':'dinesh.rcnd@gmail.com','password':'123'}}
user_data={}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=str(request.form['uname'])
        email=request.form['email']
        password=str(request.form['pwd'])
        user_data[username]={'email':email,'password':password}
        otp=gen_otp()
        print(user_data)
        subject=f'Verification mail for SNM project'
        body=f'OTP for SNM Register Verify {otp}'
        send_mail(to=email,subject=subject,body=body)
        flash(f'The OTP has been sent to given {email} email')
        print(otp)
        return redirect(url_for('otpverify',serverotp=otp))
        # if username not in user_data:
        #     user_data[username]={'email':email,'password':password}
        #     return redirect(url_for('login'))
        # else:
        #     return 'user already exists' and redirect(url_for('login'))
    return render_template('register.html')

@app.route('/otpverify/<serverotp>',methods=['GET','POST'])
def otpverify(serverotp):
    if request.method=='POST':
        userotp=request.form['userotp']
        #We need to check whether userotp is same as serverotp
        if userotp==serverotp:
            return redirect(url_for('login'))
        else:
            flash('INVALID OTP')

    return render_template('otpverify.html')

@app.route('/login',methods=['GET','POST'])
def login():
    print(user_data)
    if request.method=='POST':
        username=request.form['username']
        # email=request.form['email']
        password=request.form['password']
        if username in user_data:
            if password==user_data[username]['password']:
                return 'success'
            else:
                return 'wrong password'
        else:
            return 'user not found'
    return render_template('login.html')


app.run(use_reloader=True,debug=True)

