from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime
import MySQLdb.cursors
from fpdf import FPDF
import numpy as np
from flask_mail import Mail, Message
# import io
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# import matplotlib.pyplot as plt 

# >cd flask_app

# C:\Users\Samrudhi\flask_app>env\scripts\activate

# (env) C:\Users\Samrudhi\flask_app>cd projects

# (env) C:\Users\Samrudhi\flask_app\projects>set FLASK_APP=project.py

# (env) C:\Users\Samrudhi\flask_app\projects>flask run

app=Flask(__name__)
app.secret_key='project key'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Aish147#'
app.config['MYSQL_DB']='project'

mysql =MySQL(app)

date=datetime.now()

l=datetime.today()
now=l.strftime('%Y-%m-%d')

# STATIC PAGES START
@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def services():
    return render_template('service.html')

@app.route('/team',methods=['POST','GET'])
def team():
    cursor=mysql.connection.cursor()
    cursor.execute("select * from project.builder")
    data=cursor.fetchall()
    return render_template('team.html',data=data)

@app.route('/project',methods=['POST','GET'])
def project():
    cursor=mysql.connection.cursor()
    # scheme_id= (session['scheme_id'])
    # print(scheme_id)
    # cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from project.scheme")
    # query="select project.scheme.scheme_name,project.scheme.scheme_address,scheme. aminities.aminities_name from project.scheme, project.aminities where project.scheme.scheme_id=%s and project.aminities.scheme_id=%s"
    # cursor.excute(query,(scheme_id,scheme_id,))
    data=cursor.fetchall()
    print(data)
    # session['scheme_id']=data[1]
    # print(data[1][0])
    return render_template('project.html',data=data)

@app.route('/contact',methods=['POST','GET'])
def contact():
    msg=""
    if request.method=='POST':
        fullname=request.form['fullname']
        email_id=request.form['email_id']
        phoneno=request.form['phoneno']
        message=request.form['message']
        cursor=mysql.connection.cursor()
        cursor.execute("insert into project.feedback (fullname,email_id,phoneno,message) values (%s,%s,%s,%s)",(fullname,email_id,phoneno,message))
        mysql.connection.commit()
        msg="Your feedback send successfully....."
    return render_template('contact.html',msg=msg)

@app.route('/inside',methods=['POST','GET'])
def inside():
    data1=''
    data=''
    if 'loggedin' in session:
        print("hii")
        cus_id=session['id']
        cursor=mysql.connection.cursor()
        if request.method=="POST" and 'scheme_id' in request.form:
            print("hiiiii")
            session['scheme_id']=request.form['scheme_id']
            scheme_id=(session['scheme_id'])
            print(scheme_id)
            print(type(scheme_id))
            # query="SELECT project.scheme.scheme_name,project.flat.image,project.flat.type_of_flat,project.flat.area_sqft,project.flat.price, project.scheme.builder_id, project.aminities.aminities_name  FROM project.scheme,project.flat,project.aminities WHERE project.flat.scheme_id=%s and project.scheme.scheme_id=%s and project.aminities.scheme_id=%s"
            query="SELECT project.scheme.scheme_name,project.flat.image,project.flat.type_of_flat,project.flat.area_sqft,project.flat.price, project.scheme.builder_id  FROM project.scheme,project.flat WHERE project.flat.scheme_id=%s and project.scheme.scheme_id=%s"
            cursor.execute(query,(scheme_id,scheme_id))
            data1=cursor.fetchall()
            print(data1)
            # print(data1[1])
            session['builder_id_msg']=data1[0][5]
            builder_id_msg=session['builder_id_msg']

        if request.method=="POST" and 'cus_id' in request.form:
            print('hii')
            session['cus_id_msg']=request.form['cus_id']
            # session['builder_id_msg']=request.form['builder_id']
            cus_id_msg=session['cus_id_msg']
            builder_id_msg=session.get('builder_id_msg')
            print(builder_id_msg)
            print(cus_id_msg)
            cursor=mysql.connection.cursor()
            # cursor.execute("select fullname,email_id,phone_no from project.customer where cus_id=%s",(session['cus_id_msg']))
            cursor.execute("select fullname,email_id,phone_no from project.customer where cus_id= %s ",(cus_id_msg, ))
            data=cursor.fetchall()
            print(data)
            msg='Your request has been send'
            cursor.execute("insert into project.inquiry(date,cus_id_msg,builder_id_msg,fullname,email_id,phone_no,msg)values (%s,%s,%s,%s,%s,%s,%s)",(now,cus_id_msg,builder_id_msg,data[0][0],data[0][1],data[0][2],msg))
            mysql.connection.commit()
            msg="Your request send successfully....."
            return redirect(url_for('customerdashboard'))
        return render_template('inside.html',data1=data1,cus_id=cus_id,data=data)
    else:
        return redirect(url_for('customersignin'))



@app.route('/try',methods=['POST','GET'])
def try1():
    if request.method=='POST':
        session['scheme_id']=request.form['scheme_id']
        cursor=mysql.connection.cursor()
        scheme_id=(session['scheme_id'])
        print(scheme_id)
        query="SELECT project.scheme.scheme_name,project.flat.image FROM project.scheme,project.flat WHERE project.scheme.scheme_id=project.flat.scheme_id=%s"
        cursor.execute(query,(scheme_id))
        data=cursor.fetchall()
    return render_template('try.html')

@app.route('/first1')
def first1():
    cursor=mysql.connection.cursor()
    # cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from project.scheme")
    data=cursor.fetchall()
    return render_template('first1.html',data=data)
# STATIC PAGES END

# ADMIN LOGIN START  
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select* from adminlogin where username=%s and password=%s",(username,password,))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['username']=account['username']
            return redirect(url_for('admindashboard'))
        else:
            msg="invaild username or password!"
    return render_template('adminlogin.html',msg=msg)

@app.route('/admindashboard')
def admindashboard():
    if 'loggedin' in session:
     return render_template('admindashboard.html')
    else:
        return redirect(url_for('adminlogin'))


# ADMIN LOGIN END

# CUSTOMER LOGIN/REGISTER START
@app.route('/customersignin',methods=['GET','POST'])
def customersignin():
    msg = ''
    if request.method =='POST' and 'email_id' in request.form and 'password' in request.form :
        email_id = request.form['email_id']
        password = request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select* from customer where email_id=%s and password=%s",(email_id,password,))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['id']=account['cus_id']
            session['email_id']=account['email_id']
            return redirect(url_for('customerdashboard'))
        else:
            msg='Incorrect emai_id / password !'
    return render_template('customersignin.html',msg=msg)

@app.route('/customersignup',methods=['GET','POST'])
def customersignup():
    msg = ''
    if request.method =='POST' and 'fullname' in request.form and 'phone_no' in request.form and 'email_id' in request.form and 'password' in request.form:
        fullname = request.form['fullname']
        phone_no = request.form['phone_no']
        email_id = request.form['email_id']
        password = request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select* from customer where email_id=%s",(email_id,))
        output =cursor.fetchone()
        if output:
            print('hi')
            msg='Account already exist !'
        elif not fullname or not phone_no or not email_id or not password:
            msg ='Please fill out the form !'
        elif not re.match (r'[^@]+@[^@]+\.[^@]+',email_id):
            msg='Invalid email address'
        
        # elif not re.match (r'[A-Za-z0-9]+',password):
        #     msg='Password must contain only characters and numbers'
        else:
            cursor.execute("insert into project.customer(fullname,phone_no,email_id,password) values (%s,%s,%s,%s)",(fullname,phone_no,email_id,password))
            mysql.connection.commit()
            msg='You have sccuesfully Registered !'
            return redirect(url_for('customersignin'))
    elif request.method == 'POST':
        msg='Please fill out the form'
    return render_template('customersignup.html',msg=msg)



# CUSTOMER LOGIN/REGISTERD END

# BUILDER LOGIN/REGISTERD START
@app.route('/buildersignin',methods=['GET','POST'])
def buildersignin():              
    msg = ''
    if request.method =='POST' and 'builder_emailid' in request.form and 'password' in request.form :
        session['builder_emailid']=request.form['builder_emailid']
        password = request.form['password']
        builder_emailid = session['builder_emailid']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from builder where builder_emailid=%s and password=%s",(builder_emailid,password,))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['builder_id']=account['builder_id']
            session['builder_emailid']=account['builder_emailid']
            
            return redirect(url_for('builderdashboard'))
        else:
            msg='Incorrect emai_id / password !'
    return render_template('buildersignin.html',msg=msg)


@app.route('/buildersignup',methods=['GET','POST'])
def buildersignup():
    msg = ''
    if request.method =='POST' and 'builder_name' in request.form and 'builder_emailid' in request.form and 'password' in request.form and 'logo' in request.form and 'builder_mobile' in request.form and 'builder_phone' in request.form and 'builder_office' in request.form and 'builder_city' in request.form and 'builder_state' in request.form and 'builder_country'in request.form:
        print('hi') 
        builder_name = request.form['builder_name']
        builder_emailid = request.form['builder_emailid']
        password = request.form['password']
        logo = request.form['logo']
        builder_mobile = request.form['builder_mobile']
        builder_phone = request.form['builder_phone']
        builder_office = request.form['builder_office']
        builder_city = request.form['builder_city']
        builder_state = request.form['builder_state']
        builder_country = request.form['builder_country']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from builder where builder_emailid=%s",(builder_emailid,))
        output =cursor.fetchone()
        
        if output:
            # print('hi') 
            msg='Account already exist !'
        elif not builder_name or not builder_emailid or not password or not builder_mobile or not builder_phone or not builder_office or not builder_city or not builder_state or not builder_country:
            msg ='Please fill out the form!'
        elif not re.match (r'[^@]+@[^@]+\.[^@]+',builder_emailid):
            msg='Invalid email address'
        else:
            cursor.execute("insert into project.builder (builder_name,builder_emailid,password,logo,builder_mobile,builder_phone,builder_office,builder_city,builder_state,builder_country) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(builder_name,builder_emailid,password,logo,builder_mobile,builder_phone,builder_office,builder_city,builder_state,builder_country)) 
            mysql.connection.commit()
            msg='You have sccuesfully Registered !'
            return redirect(url_for('buildersignin'))
    elif request.method == 'POST':
        msg='Please fill out the form'
    return render_template('buildersignup.html',msg=msg)



# BUILDER LOGIN/REGISTERD END

# FORGUT PASWORD FOR CUSTOMER START

@app.route('/forget',methods=['GET','POST'])
def forget():
    if request.method =='POST' and 'email_id' in request.form and 'password' in request.form:
        print('hi')
        email_id = request.form['email_id']
        password = request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from customer where email_id=%s",(email_id,))
        account=cursor.fetchone()
        print('hi')
        if account:
            cursor.execute("update project.customer set password=%s where email_id=%s" ,(password,email_id,))
            mysql.connection.commit()
            return redirect(url_for('customersignin'))
        else:
            msg='Incorrect emai_id / password !'
    return render_template('forget.html')

@app.route('/builderforget',methods=['GET','POST'])
def builderforget():
    if request.method =='POST' and 'builder_emailid' in request.form and 'password' in request.form:
        print('hii')
        builder_emailid = request.form['builder_emailid']
        password = request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from builder where builder_emailid=%s",(builder_emailid,))
        account=cursor.fetchone()
        print('hi')
        if account:
            cursor.execute("update project.builder set password=%s where builder_emailid=%s" ,(password,builder_emailid,))
            mysql.connection.commit()
            return redirect(url_for('buildersignin'))
        else:
            msg='Incorrect emai_id / password !'
    return render_template('builderforget.html')

@app.route('/adminforget',methods=['GET','POST'])
def adminforget():
    if request.method =='POST' and 'username' in request.form and 'password' in request.form:
        print('hi')
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from adminlogin where username=%s",(username,))
        account=cursor.fetchone()
        print('hi')
        if account:
            cursor.execute("update project.adminlogin set password=%s where username=%s" ,(password,username,))
            mysql.connection.commit()
            return redirect(url_for('adminlogin'))
        else:
            msg='Incorrect emai_id / password !'
    return render_template('adminforget.html')


# FORGOT PASSWORD FOR CUSTOMER END



# ADD SCHEME START

@app.route('/scheme',methods=['GET','POST'])
def scheme():
    msg = ''
  
    if request.method =='POST' and 'scheme_name' in request.form and 'scheme_address' in request.form and 'scheme_city' in request.form and 'scheme_state' in request.form and 'scheme_country'in request.form and 'total_no_of_flats'in request.form and 'aminities[]' in request.form:
        scheme_name = request.form['scheme_name']
        scheme_address = request.form['scheme_address']
        scheme_city = request.form['scheme_city']
        scheme_state = request.form['scheme_state']
        scheme_country = request.form['scheme_country']
        total_comercial_space = request.form['total_comercial_space']
        total_1bhk = request.form['total_1bhk']
        total_2bhk = request.form['total_2bhk']
        total_3bhk = request.form['total_3bhk']
        total_4bhk = request.form['total_4bhk']
        total_no_of_flats = request.form['total_no_of_flats']
        aminities_name = request.form.getlist('aminities[]')
        image = request.form['image']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from project.scheme where scheme_name=%s",(scheme_name,))
        output=cursor.fetchone()
        cursor.execute("select builder_id from project.builder where builder_emailid=%s",(session['builder_emailid'],))
        s=cursor.fetchone()
        print(s)
        a=''
        for values in s:
            a=s[values]
            print(a)
        # for i in aminities:
        #     print(i)

           
        if output:
            
            msg='Account already exist !'
        
        else:
           
            cursor.execute("insert into project.scheme(builder_id,scheme_name,scheme_address,scheme_city,scheme_state,scheme_country,total_comercial_space,total_1bhk,total_2bhk,total_3bhk,total_4bhk,total_no_flats,image) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(a,scheme_name,scheme_address,scheme_city,scheme_state,scheme_country,total_comercial_space,total_1bhk,total_2bhk,total_3bhk,total_4bhk,total_no_of_flats,image,))
            mysql.connection.commit()
            cursor.execute('select scheme_id from project.scheme where scheme_name=%s',(scheme_name,))
            data=cursor.fetchone()
            
            a1=''
            for values in data:
                a1=data[values]
                print(a1)
            for i in aminities_name:
                print(i)
                cursor.execute("insert into project.aminities(scheme_id,aminities_name) values(%s,%s)",(a1,i,))
                mysql.connection.commit()
            msg='You have sccuesfully Registered !'
            
            session['scheme_id']=a1
            
            return redirect(url_for('flat'))
            return redirect(url_for('flat'))
    elif request.method == 'POST':
        msg='Please fill out the form'
    return render_template('scheme.html',msg=msg)

# ADD SCHEME END

# ADD FLAT START

@app.route('/flat',methods=['GET','POST'])
def flat():
    msg = ''
    print('hii')
    account=''
    if request.method =='POST' and  'type_of_flat' in request.form and 'floor_no' in request.form and 'area_sqft' in request.form and 'price' in request.form and 'image' in request.form:
        type_of_flat =request.form['type_of_flat']
        floor_no =request.form['floor_no']
        area_sqft =request.form['area_sqft']
        price =request.form['price']
        image=request.form['image']
        
        # print('hii')
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from project.flat where image=%s",(image,))
        output=cursor.fetchone()
        
        if account:
            session['loggedin']=True
            session['flat_id']=account['flat_id']
            session['image']=account['image']
        #     return redirect(url_for(flat))
        # else:
        #     msg='hii'
        cursor.execute("select builder_id from project.builder where builder_emailid=%s",(session['builder_emailid'],))
        s=cursor.fetchone()
        print(s)
        cursor.execute("select scheme_id from project.scheme where scheme_id=%s",(session['scheme_id'],))
        s2=cursor.fetchone()
        print(s2)
        if output:
            print('hi')
            msg='Account already exist !'
        else:
            a=''
            for values in s:
                a=s[values]
                print(a)
            b=''
            for values in s2:
                b=s2[values]
                print(b)
            cursor.execute("insert into project.flat(builder_id,scheme_id,type_of_flat,floor_no,area_sqft,price,image) values (%s,%s,%s,%s,%s,%s,%s)", (a,b,type_of_flat,floor_no,area_sqft,price,image,))
            mysql.connection.commit()
            
            msg='You have sccuesfully Registered !'
            return redirect(url_for('builderdashboard'))
    elif request.method == 'POST':
        msg='Please fill out the form'
    return render_template('flat.html',msg=msg)

# ADD FLAT END 

# PROFILES  STARTS

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM builder WHERE builder_id = %s', (session['builder_id'],))
        data = cursor.fetchall()
        print(data)
    return render_template('profile.html',data=data)


@app.route('/customerprofile')
def customerprofile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM customer WHERE cus_id = %s', (session['id'],))
        data = cursor.fetchall()
        print(data)
    return render_template('customerprofile.html',data=data)


#PROFILES  END 

@app.route('/customerdashboard')
def customerdashboard():
    if 'loggedin' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT fullname FROM project.customer WHERE cus_id = %s', (session['id'],))
        data = cursor.fetchall()
        print(data)
        print(type(data))
    return render_template('customerdashboard.html',data=data)

@app.route('/builderdashboard')
def builderdashboard():
    if 'loggedin' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT builder_name FROM project.builder WHERE builder_id = %s', (session['builder_id'],))
        data = cursor.fetchall()
        print(data)
        print(type(data))
    return render_template('builderdashboard.html',data=data)



# DISPLAY REGISTERD DATA START
@app.route('/customerregistered',methods=['POST','GET'])
def cusdata():
    cursor=mysql.connection.cursor()
    cursor.execute('select * from project.customer')
    data=cursor.fetchall()
    cursor.close() 
    return render_template('customerregistered1.html',user=data)


# @app.route('/customerregistered1',methods=['POST','GET'])
# def cusdata1():
#     cursor=mysql.connection.cursor()
#     cursor.execute('select * from project.customer')
#     data=cursor.fetchall()
#     cursor.close() 
#     return render_template('customerregistered1.html',user=data)

@app.route('/messages',methods=['POST','GET'])
def totalinquiry():
    builder_id=session['builder_id']
    print(builder_id)
    print(type(builder_id))
    cursor=mysql.connection.cursor()
    cursor.execute('select * from project.inquiry where builder_id_msg=%s',(builder_id,))
    data=cursor.fetchall()
    print(data)
    # print(data[0][3])
    # print(data[0][1])
    # cus_id=data[0][1]
    # cus_id=session['id']
    # cursor.execute('select * from project.customer where cus_id=%s',(cus_id,))
    # data1=cursor.fetchall() 
    # print(data1)   
    cursor.close()
    return render_template('messages.html',user=data )

@app.route('/intrested',methods=['POST','GET'])
def intrested():
    cus_id=session['id']
    print(cus_id)
    cursor=mysql.connection.cursor()
    cursor.execute('select * from project.inquiry where cus_id_msg=%s',(cus_id,))
    data=cursor.fetchall()
    print(data)
    cursor.close()
    return render_template('intrested,html',user=data)

    
@app.route('/builderregistered',methods=['POST','GET'])
def buildata():
    cursor=mysql.connection.cursor()
    cursor.execute('select * from project.builder')
    data=cursor.fetchall()
    cursor.close() 
    return render_template('builderregistered1.html',user=data)

@app.route('/viewfeedback',methods=['POST','GET'])
def viewfeedback():
    cursor=mysql.connection.cursor()
    cursor.execute('select * from project.feedback')
    data=cursor.fetchall()
    cursor.close()
    return render_template('viewfeedback.html',data=data)

@app.route('/schemeregistered',methods=['POST','GET'])
def schemeregistered():
    builder_id=session['builder_id']
    print(builder_id)
    cursor=mysql.connection.cursor()
    query="SELECT project.scheme.scheme_name,project.scheme.total_no_flats,project.flat.price,project.flat.type_of_flat,project.scheme.builder_id from project.scheme,project.flat where project.scheme.builder_id=%s and project.flat.builder_id=%s"
    cursor.execute(query,(session['builder_id'],session['builder_id']))
    data=cursor.fetchall()
    print(data)
    cursor.close() 
    # cursor1=mysql.connection.cursor()
    # cursor1.execute("select * from project.flat")
    # data1=cursor1.fetchall()
    return render_template('schemeregistered1.html',data=data)

@app.route('/scheme_update/<flat_id>',methods=['POST','GET'])
def scheme_update(flat_id):
    msg = ''
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM flat WHERE type_of_flat = %s', (flat_id, ))
    data = cursor.fetchall()
    print(data)
    fl_id=data[0][0]
    session['fl_id']=fl_id
    fl_id=session['fl_id']
    # if request.method == 'POST':
    #     print("Hlo")
    #     price=request.form['price']
    #     cursor = mysql.connection.cursor()
    #     cursor.execute('SELECT * FROM scheme WHERE image = %s', (session['builder_id'], ))
    #     data = cursor.fetchall()
    #     print(data)
    return render_template('scheme_update.html',msg=msg,)

@app.route('/delete/<flat_id>',methods=['POST','GET'])
def delete(flat_id):
    cursor=mysql.connection.cursor()
    cursor.execute("delete from project.flat where flat_id=%s",(fl_id,))
    flash("Flat Deleted Sucessfully")
    return redirect(url_for('builderdashbord'))

@app.route('/scheme_update',methods=['POST','GET'])
def scheme_update1():
    fl_id=session['fl_id']
    if request.method == 'POST':
        price=request.form['price']
        print("hii")
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE project.flat SET price =%s WHERE flat_id =%s', (price,fl_id))
        mysql.connection.commit()
        msg = 'You have successfully updated !'
    return redirect(url_for('schemeregistered'))
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form !'
    
# @app.route('/schemeregistered',methods=['POST','GET'])
# def schemeregistered():
#     data=''
#     data1=''
#     data3=''
#     if 'loggedin' in session:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM builder WHERE builder_id = %s', (session['builder_id'],))
#         data3 = cursor.fetchone()
#         cursor=mysql.connection.cursor()
#         cursor.execute("select * from project.scheme")
#     # query="SELECT project.scheme.scheme_name,project.scheme.total_no_flats,project.flat.price,project.flat.type_of_flat from project.scheme,project.flat where project.scheme.builder_id=project.flat.builder_id"
#     # cursor.execute(query)
#         data=cursor.fetchall()
#         cursor.close() 
#         cursor=mysql.connection.cursor()
#         cursor.execute("select * from project.flat")
#         data1=cursor.fetchall()
#     return render_template('schemeregistered2.html',data=data,data1=data1,data3=data3)

# DISPLAY REGISTERD DATA END

# LOGOUT START
@app.route('/builderlogout')
def builderlogout():
    session.pop('loggedin',None)
    session.pop('builder_id',None)
    session.pop('builder_emailid',None)
    return redirect(url_for('index'))

@app.route('/adminlogout')
def adminlogout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/customerlogout')
def customerlogout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('email_id',None)
    return redirect(url_for('index'))
# LOGOUT END

# UPDATE START

@app.route('/edit', methods = ['GET','POST'])
def edit():
    if 'loggedin' in session:
        if request.method =='POST' and 'flat_id' in request.form and 'price' in request.form:
            print('hii')
            flat_id = request.form['flat_id']
            price = request.form['price']
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from flat where flat_id=%s",(session['id'],))
            account=cursor.fetchone()
            print('hii')
            if account:
                print(hii)
                cursor.excute("UPDATE project.flat SET price=%s WHERE flat_id=%s",(price,(session['flat_id'], ),))
                mysql.connection.commit()
                return redirect(url_for('schemeregistered'))
            else:
                msg='updated Information !'
        return render_template('edit.html')
    return redirect(url_for('schemeregistered'))
    

@app.route('/update',methods=['POST','GET'])
def update():
    msg = ''
    if request.method == 'POST':
        print("Hlo")
        builder_mobile = request.form['builder_mobile']
        builder_phone = request.form['builder_phone']
        builder_office = request.form['builder_office']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM builder WHERE builder_emailid = %s', (session['builder_emailid'], ))
        data = cursor.fetchone() 
        if request.method == 'POST':
            print("hii")
            cursor.execute('UPDATE project.builder SET builder_mobile =%s, builder_phone=%s, builder_office=%s  WHERE builder_emailid =%s', (builder_mobile,builder_phone, builder_office,(session['builder_emailid'], )))
            mysql.connection.commit()
            msg = 'You have successfully updated !'
            return redirect(url_for('builderdashboard'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('update.html',msg=msg,)


@app.route('/customerupdate',methods=['POST','GET'])
def customerupdate():
    msg = ''
    if request.method == 'POST':
        print("Hlo")
        fullname = request.form['fullname']
        phone_no = request.form['phone_no']
        # email_id = request.form['email_id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM customer WHERE email_id = %s',(session['email_id'], ))
        data = cursor.fetchall() 
        print(data)
        if request.method == 'POST':
            print("hii")
            cursor.execute('UPDATE project.customer SET  phone_no=%s, fullname=%s  WHERE email_id =%s', (phone_no,fullname,(session['email_id'], )))
            mysql.connection.commit()
            msg = 'You have successfully updated !'
            return redirect(url_for('customerdashboard'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('customerupdate.html',msg=msg,)
#UPDATE END

#FEEDBACK START

@app.route('/feedback',methods=['POST','GET'])
def feedback():
    msg=""
    if request.method=='POST':
        fullname=request.form['fullname']
        email_id=request.form['email_id']
        phoneno=request.form['phoneno']
        message=request.form['message']
        cursor=mysql.connection.cursor()
        cursor.execute("insert into feedback (fullname,email_id,phoneno,message) values (%s,%s,%s,%s)",(fullname,email_id,phoneno,message,))
        mysql.connection.commit()
        msg="Your feedback send successfully....."
    return render_template("contact.html",msg=msg)


#fEEDBACK END



@app.route('/form-basic')
def form_basic():
    return render_template('form-basic.html')

@app.route('/table-row-select')
def table_row_select():
    return render_template('table-row-select.html')

@app.route('/chart-flot')
def chart_flot():
    return render_template('chart-flot.html')

@app.route('/uc-rating-bar-rating')
def uc_rating_bar_rating():
    return render_template('uc-rating-bar-rating.html')

@app.route('/chart-sparkline')
def chart_sparkline():
    return render_template('chart-sparkline.html')

@app.route('/app-email')
def app_email():
    return render_template('app-email.html')

@app.route('/ui-panels')
def ui_panels():
    return render_template('ui-panels.html')

@app.route('/chartist')
def chartist():
    return render_template('chartist.html')

@app.route('/app-event-calender')
def app_event_calender():
    return render_template('app-event-calender.html')

#REPORTS STARTS

@app.route('/customerreport')
def customerreport():
    cursor=mysql.connection.cursor()
    cursor.execute('select fullname,phone_no,email_id from customer')
    data1=cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.ln(10)
    pdf.set_font('Times','B',30.0)
    pdf.cell(page_width,0.0,"Dream Home",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Address:"+""+"Rajarampuri,Kolhapur,416005",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Email:"+""+"dreamhome@gmail.com",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',20.0)
    
    pdf.cell(page_width,0.0,"Report of Total Registered Customer",align="C")
    
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(20,th,"Sno",border=1,align="C")
    pdf.cell(40,th,"Customer_Name",border=1,align="C")
    pdf.cell(35,th,"Phone Number",border=1,align="C")
    pdf.cell(55,th,"Email_id",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(20,th,str(i),border=1,align="C")
        pdf.cell(40,th,row[0],border=1,align="C")
        pdf.cell(35,th,str(row[1]),border=1,align="C")
        pdf.cell(55,th,str(row[2]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Total_Customer_Report.pdf'})

@app.route('/builderreport')
def builderreport():
    cursor=mysql.connection.cursor()
    cursor.execute('select builder_name,builder_emailid,builder_mobile,builder_phone,builder_office,builder_city, builder_state, builder_country from builder')
    data1=cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.ln(10)
    pdf.set_font('Times','B',30.0)
    pdf.cell(page_width,0.0,"Dream Home",align="C")
    pdf.ln(10)
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Address:"+""+"Rajarampuri,Kolhapur,416005",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Email:"+""+"dreamhome@gmail.com",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Report of Total Registered Builder",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(10,th,"Sno",border=1,align="C")
    pdf.cell(50,th,"Builder Name",border=1,align="C")
    pdf.cell(50,th,"Emailid",border=1,align="C")
    pdf.cell(25,th,"Mobileno",border=1,align="C")
    pdf.cell(20,th,"PhoneNo",border=1,align="C")
    pdf.cell(30,th,"Address",border=1,align="C")
    # pdf.cell(30,th,"builder_City",border=1,align="C")
    # pdf.cell(30,th,"builder_State",border=1,align="C")
    # pdf.cell(30,th,"builder_Country",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(10,th,str(i),border=1,align="C")
        pdf.cell(50,th,row[0],border=1,align="C")
        pdf.cell(50,th,str(row[1]),border=1,align="C")
        pdf.cell(25,th,str(row[2]),border=1,align="C")
        pdf.cell(20,th,str(row[3]),border=1,align="C")
        pdf.cell(30,th,str(row[4]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Total_Builder_Report.pdf'})


@app.route('/schemereport')
def schemereport():
    cursor=mysql.connection.cursor()
    cursor.execute('select scheme_name,scheme_address,scheme_city,scheme_state,scheme_country from scheme')
    data1=cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.ln(10)
    pdf.set_font('Times','B',30.0)
    pdf.cell(page_width,0.0,"Dream Home",align="C")
    pdf.ln(10)
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Address:"+""+"Rajarampuri,Kolhapur,416005",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Email:"+""+"dreamhome@gmail.com",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Report of Total Registered Projects",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(20,th,"Sno",border=1,align="C")
    pdf.cell(40,th,"Scheme Name",border=1,align="C")
    pdf.cell(35,th,"Scheme Address",border=1,align="C")
    pdf.cell(30,th,"City",border=1,align="C")
    pdf.cell(30,th,"State",border=1,align="C")
    pdf.cell(30,th,"Country",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(20,th,str(i),border=1,align="C")
        pdf.cell(40,th,row[0],border=1,align="C")
        pdf.cell(35,th,str(row[1]),border=1,align="C")
        pdf.cell(30,th,str(row[2]),border=1,align="C")
        pdf.cell(30,th,str(row[3]),border=1,align="C")
        pdf.cell(30,th,str(row[4]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Total_Scheme_Report.pdf'})


@app.route('/inquiryreport')
def inquiryreport():
    cursor=mysql.connection.cursor()
    cursor.execute('select date, fullname,phone_no,email_id from inquiry order by date')
    data1=cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.ln(10)
    pdf.set_font('Times','B',30.0)
    pdf.cell(page_width,0.0,"Dream Home",align="C")
    pdf.ln(10)
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Address:"+""+"Rajarampuri,Kolhapur,416005",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Email:"+""+"dreamhome@gmail.com",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Report of enquiry",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(15,th,"Sno",border=1,align="C")
    pdf.cell(35,th,"date",border=1,align="C")
    pdf.cell(50,th,"Customer Name",border=1,align="C")
    pdf.cell(40,th,"PhoneNo",border=1,align="C")
    pdf.cell(55,th,"Email",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(15,th,str(i),border=1,align="C")
        pdf.cell(35,th,str(row[0]),border=1,align="C")
        pdf.cell(50,th,str(row[1]),border=1,align="C")
        pdf.cell(40,th,str(row[2]),border=1,align="C")
        pdf.cell(55,th,str(row[3]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Inquiry_Report.pdf'})

@app.route('/feedbackreport')
def feedbackreport():
    cursor=mysql.connection.cursor()
    cursor.execute('select fullname,phoneno,email_id,message from feedback')
    data1=cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.ln(10)
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Dream Home",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report of Feedback",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(10,th,"Sno",border=1,align="C")
    pdf.cell(35,th,"Customer_Name",border=1,align="C")
    pdf.cell(30,th,"PhoneNumber",border=1,align="C")
    pdf.cell(45,th,"Emailid",border=1,align="C")
    pdf.cell(65,th,"Feedback",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(10,th,str(i),border=1,align="C")
        pdf.cell(35,th,row[0],border=1,align="C")
        pdf.cell(30,th,str(row[1]),border=1,align="C")
        pdf.cell(45,th,str(row[2]),border=1,align="C")
        pdf.cell(65,th,str(row[3]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Feedback_Report.pdf'})

@app.route('/builderscheme')
def builderscheme():
    cursor=mysql.connection.cursor()
    cursor.execute('select scheme_name,scheme_address,scheme_city,scheme_country from scheme where  builder_id=%s',(session['builder_id'],))
    data1=cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.ln(10)
    pdf.set_font('Times','B',30.0)
    pdf.cell(page_width,0.0,"Dream Home",align="C")
    pdf.ln(10)
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Address:"+""+"Rajarampuri,Kolhapur,416005",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Email:"+""+"dreamhome@gmail.com",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Report of Scheme",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Builder",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(15,th,"Sno",border=1,align="C")
    pdf.cell(50,th,"Scheme Name",border=1,align="C")
    pdf.cell(30,th,"Address",border=1,align="C")
    pdf.cell(30,th,"City",border=1,align="C")
    pdf.cell(30,th,"State",border=1,align="C")
    pdf.cell(30,th,"Country",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(15,th,str(i),border=1,align="C")
        pdf.cell(50,th,row[0],border=1,align="C")
        pdf.cell(30,th,str(row[1]),border=1,align="C")
        pdf.cell(30,th,str(row[2]),border=1,align="C")
        pdf.cell(30,th,str(row[3]),border=1,align="C")
        pdf.cell(30,th,str(row[3]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)

    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Scheme_Report_Dowloded_By_Builder.pdf'})

@app.route('/builderinquiery')
def builderinquiery():
    cursor=mysql.connection.cursor()
    cursor.execute('select fullname, email_id, phone_no from inquiry where  builder_id_msg=%s',(session['builder_id'],))
    data1=cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.ln(10)
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Dream Home",align="C")
    pdf.ln(10)
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Address:"+""+"Rajarampuri,Kolhapur,416005",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Email:"+""+"dreamhome@gmail.com",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report of Enquiry",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Builder",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(15,th,"Sno",border=1,align="C")
    pdf.cell(50,th,"Customer Name",border=1,align="C")
    pdf.cell(60,th,"email",border=1,align="C")
    pdf.cell(30,th,"Mobileno",border=1,align="C")
   
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(15,th,str(i),border=1,align="C")
        pdf.cell(50,th,row[0],border=1,align="C")
        pdf.cell(60,th,str(row[1]),border=1,align="C")
        pdf.cell(30,th,str(row[2]),border=1,align="C")
        
        i=i+1
        pdf.ln(th)
    pdf.ln(10)

    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Enquiry_Report_Dowloded_By_Builder.pdf'})

@app.route('/inquierydate',methods=['POST','GET'])
def inquierydate():
    cursor=mysql.connection.cursor()
    if request.method=="POST":
        fdate=request.form['fdate']
        tdate=request.form['tdate']
        cursor.execute('select fullname, email_id, phone_no from inquiry where  builder_id_msg=%s and date>=%s and date<=%s',(session['builder_id'],str(fdate),str(tdate),))
        data1=cursor.fetchall()
        pdf = FPDF()
        pdf.add_page()
        page_width=pdf.w-3*pdf.l_margin
        pdf.ln(10)
        pdf.set_font('Times','B',30.0)
        pdf.cell(page_width,0.0,"Dream Home",align="C")
        pdf.ln(10)
        pdf.ln(10)
        pdf.set_font('Times','I',14.0)
        pdf.cell(page_width,0.0,"Address:"+""+"Rajarampuri,Kolhapur,416005",align="C")
        pdf.ln(10)
        pdf.set_font('Times','I',14.0)
        pdf.cell(page_width,0.0,"Email:"+""+"dreamhome@gmail.com",align="C")
        pdf.ln(10)
        pdf.set_font('Times','B',20.0)
        pdf.cell(page_width,0.0,"Report of Enquiry",align="C")
        pdf.ln(10)
        pdf.set_font('Times','B',12.0)
        pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Builder",align="L")
        pdf.ln(10)
        pdf.set_font('Times','B',12.0)
        pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
        pdf.ln(10)
        pdf.set_font('Times','B',12.0)
        pdf.cell(page_width,0.0," From Date:"+""+str(fdate),align="C")
        pdf.ln(10)
        pdf.cell(page_width,0.0,"TO Date:"+""+str(tdate),align="C")
        pdf.ln(10)
        pdf.set_font('Courier','',12)
        col_width=page_width/4
        pdf.ln(1)
        th=pdf.font_size
        i=1
        pdf.set_font('Times','B',12.0)
        pdf.cell(15,th,"Sno",border=1,align="C")
        pdf.cell(50,th,"Customer Name",border=1,align="C")
        pdf.cell(60,th,"email",border=1,align="C")
        pdf.cell(30,th,"Mobileno",border=1,align="C")
    
        pdf.ln(th)
        th=pdf.font_size 
        pdf.set_font('Times','I',10.0)        
        for row in data1:
            pdf.cell(15,th,str(i),border=1,align="C")
            pdf.cell(50,th,row[0],border=1,align="C")
            pdf.cell(60,th,str(row[1]),border=1,align="C")
            pdf.cell(30,th,str(row[2]),border=1,align="C")
            
            i=i+1
            pdf.ln(th)
        pdf.ln(10)

        pdf.set_font('Times','',10.0)
        pdf.cell(page_width,0.0, '-----End of report-----',align='C')
        return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Monthwise_Enquiry_Report_Dowloded_By_Builder.pdf'})

@app.route('/inquierydate1')
def inquierydate1():
    return render_template('Monthwise.html')

@app.route('/inquierydate2',methods=['POST','GET'])
def inquierydate2():
    cursor=mysql.connection.cursor()
    if request.method=="POST":
        fdate=request.form['fdate']
        tdate=request.form['tdate']
        cursor.execute('select date,fullname,phone_no,email_id from inquiry where date>=%s and date<=%s order by date',(str(fdate),str(tdate),))
        data1=cursor.fetchall()
        pdf = FPDF()
        pdf.add_page()
        page_width=pdf.w-3*pdf.l_margin
        pdf.ln(10)
        pdf.set_font('Times','B',30.0)
        pdf.cell(page_width,0.0,"Dream Home",align="C")
        pdf.ln(10)
        pdf.ln(10)
        pdf.set_font('Times','I',14.0)
        pdf.cell(page_width,0.0,"Address:"+""+"Rajarampuri,Kolhapur,416005",align="C")
        pdf.ln(10)
        pdf.set_font('Times','I',14.0)
        pdf.cell(page_width,0.0,"Email:"+""+"dreamhome@gmail.com",align="C")
        pdf.ln(10)
        pdf.set_font('Times','B',20.0)
        pdf.cell(page_width,0.0,"Report of Enquiry",align="C")
        pdf.ln(10)
        pdf.set_font('Times','B',12.0)
        pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
        pdf.ln(10)
        pdf.set_font('Times','B',12.0)
        pdf.cell(page_width,0.0," From Date:"+""+str(fdate),align="C")
        pdf.ln(10)
        pdf.cell(page_width,0.0,"TO Date:"+""+str(tdate),align="C")
        pdf.ln(10)
        pdf.set_font('Courier','',12)
        col_width=page_width/4
        pdf.ln(1)
        th=pdf.font_size
        i=1
        pdf.set_font('Times','B',12.0)
        pdf.cell(15,th,"Sno",border=1,align="C")
        pdf.cell(50,th,"Customer Name",border=1,align="C")
        pdf.cell(60,th,"email",border=1,align="C")
        pdf.cell(30,th,"Mobileno",border=1,align="C")
    
        pdf.ln(th)
        th=pdf.font_size 
        pdf.set_font('Times','I',10.0)        
        for row in data1:
            pdf.cell(15,th,str(i),border=1,align="C")
            pdf.cell(50,th,str(row[0]),border=1,align="C")
            pdf.cell(60,th,str(row[1]),border=1,align="C")
            pdf.cell(30,th,str(row[2]),border=1,align="C")
            
            i=i+1
            pdf.ln(th)
        pdf.ln(10)

        pdf.set_font('Times','',10.0)
        pdf.cell(page_width,0.0, '-----End of report-----',align='C')
        return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Monthwise_Enquiry_Report_Dowloded_By_Admin.pdf'})

@app.route('/inquierydate3')
def inquierydate3():
    return render_template('Monthwise1.html')

# @app.route('/graph')
# def graph():
#     from PIL import Image
#     cursor=mysql.connection.cursor()
#     cursor.execute("select service_type,count(*) from adminserviceform where month(r_date)=month(current_date()) group by service_type")
#     data5=cursor.fetchall()
#     print(data5)
#     cursor.execute("select servicename from service")
#     data6=cursor.fetchall()
#     x = [] 
#     y = []
#     label="Highest service of current month"
#     explode = (0.1, 0, 0) 
#     for value in data5:         
#         x.append(value[0])  #x column contain data(1,2,3,4,5) 
#         y.append(value[1]) 
#     fig1=plt.figure(figsize =(10, 7)) 
#     # plt.pie(labels=x,values=y,0.3,colors="orange",autopct='%1.1f%%', shadow=True, startangle=140)
#     colors = ['lightgray', 'darkorange', 'gray']
#     plt.pie(y, explode=explode, labels=x, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
#     plt.title("Highest service of current month")
#     # plt.xlabel("servicetype")
#     # plt.ylabel("Value")
#     plt.legend()
#     plt.axis('equal')
#     img=fig1.savefig('static/images/highest.jpg')
#     canvas=FigureCanvas(fig1)
#     img=io.BytesIO()
#     fig1.savefig(img)
#     img.seek(0)
#     return send_file(img,mimetype='img/jpg')
#REPORTS END    

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
# app.config['MAIL_PASSWORD'] = '*****'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

# @app.route("/mail")
# def index():
#    msg = Message('Hello', sender = 'yourId@gmail.com', recipients = ['someone1@gmail.com'])
#    msg.body = "Hello Flask message sent from Flask-Mail"
#    mail.send(msg)
#    return "Sent"