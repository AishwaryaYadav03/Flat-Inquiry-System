from flask import *
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Sam@1912'
app.config['MYSQL_DB']='project'

mysql=MySQL(app)

# query='CREATE TABLE project.register(name VARCHAR(20),address VARCHAR(30),pincode INT (6),phone_no INT(10),milk_type VARCHAR(20),cust_type VARCHAR(20),password VARCHAR(10),cpassword VARCHAR(10))'
query='CREATE TABLE project.feedback( fullname VARCHAR(30) NOT NULL ,email_id VARCHAR(30) NOT NULL,phoneno BIGINT NOT NULL,message VARCHAR(150) NOT NULL )'
# query='CREATE TABLE project.collection(day DATE NOT NULL,cust_id INT(10) PRIMARY KEY,cust_name VARCHAR(30) NOT NULL,daytime VARCHAR(20) NOT NULL,milk_type VARCHAR(20) NOT NULL,amount FLOAT(20) NOT NULL,fat FLOAT(10) NOT NULL,SNF FLOAT(10) NOT NULL,degree FLOAT(10) NOT NULL)'
# query='CREATE TABLE project.selling(date DATE NOT NULL,cust_id INT(10) PRIMARY KEY,time VARCHAR(10) NOT NULL, milk_type VARCHAR(10),amount FLOAT(20))'
# query='CREATE TABLE project.sanghrate(fat FLOAT(10) NOT NULL,SNF FLOAT(10) NOT NULL, cow_Rate FLOAT(30),buffalo_Rate FLOAT(30))'
#query='CREATE TABLE project.SNFpurchase(fat FLOAT(10) NOT NULL,SNF FLOAT(10) NOT NULL, cow_Rate FLOAT(30),buffalo_Rate FLOAT(30))'

@app.route('/')
def create_table():
	cursor=mysql.connection.cursor()
	cursor.execute(query)
	return "Table is created"