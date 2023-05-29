from flask import render_template, session, redirect, url_for, Blueprint
from models.model_home import  Userdata, Userlogin,  Adminlogin
from dotenv import  load_dotenv
import os
import logging

home_ctrl = Blueprint("home", __name__, static_folder='static', template_folder='templates')
load_dotenv()

@home_ctrl.route('/',methods=["POST", "GET"])
def index():

    user_session = session.get('name')
    user_session_otp = session.get('otp_valid')
    if not user_session or not user_session_otp:
        return render_template('index.html')
    else:
        return redirect(url_for('home.home'))


@home_ctrl.route("/home",methods=["POST", "GET"])
def home():
    user_session = session.get('name')
    user_session_otp = session.get('otp_valid')
    if not user_session or not user_session_otp:
        logging.info(f"{user_session_otp} In First IF with no data")
        return render_template('index.html')
    else:
        user_session = session.get('name')
        input_userdata = {'userid': user_session}
        userdata_found = Userdata.get_data(input_userdata)
        userlogin_found = Userlogin.get_data(input_userdata)
        #print("userdata found: ", userdata_found)
        name = userdata_found["Name"]
        Acc_no = userdata_found["Accno"]
        Acc_bal = userdata_found["Accbal"]
        email_id = userlogin_found["email"]
        act_page = 'home'
        #print("NAme is: ", name)
        return render_template('home.html', active_page = act_page, username_session = user_session, username = name, emailid = email_id, Accnumber = Acc_no, Accbalance = Acc_bal, logedin_user = user_session)

@home_ctrl.route('/admin',methods=["POST", "GET"])
def admin():
    
    if session.get('username') is not None:
        #print("session name is true: ", session.get('username'))
        return redirect(url_for('home.admin_home'))
    else:
        #print("In Main Route session name is false: ", session.get('username'))
        return render_template('admin-index.html')
    

@home_ctrl.route("/admin-home",methods=["POST", "GET"])
def admin_home():
    user_session = session.get('username')
    if not user_session:
        #print("In Home functuon username is: ", user_found)
        return render_template('admin-index.html')
    else:
        user_session = session.get('username')
        #print("Session in home new is: ", user_session)
        input_userdata = {'userid': user_session}
        userdata_found = Adminlogin.find_data(input_userdata)
        if not userdata_found:
             return render_template('admin-index.html')
        else:
            users_count = Userdata.find_user_count()
            pending_status = 'Pending'
            suspended_status = 'Suspended'
            pending_users_count = Userdata.find_user_status(pending_status)
            suspended_users_count = Userdata.find_user_status(suspended_status)
            act_page ='adminhome'
            return render_template('admin-home.html', active_page = act_page, username_session = user_session, totalusers = users_count, username = user_session, pendingusers = pending_users_count, suspendedusers = suspended_users_count , logedin_user = user_session)