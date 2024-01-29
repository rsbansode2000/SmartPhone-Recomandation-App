from flask import Flask, render_template, request
import mysql.connector


app = Flask(__name__)


#create DB connection
mydb = mysql.connector.connect(
    host="mydb.cjzqczmkydzs.us-east-1.rds.amazonaws.com",
    user="admin",
    passwd="proj123456",
    database="mydb",
    port = '3306'
)

#create cursor using DB connection
mycursor = mydb.cursor()

# This is Name of Our Site
site_name = 'Global MP 360'

@app.route('/')   #This is index
def index():
    mycursor.execute('select brand,ram, price, release_date, url, camera, rating from phone, image_url where phone.id = image_url.id')
    data = mycursor.fetchall()

    return render_template('index.html',data=data, site_name = site_name)

@app.route('/result',methods=['POST','GET'])
def result():
    output = request.form.to_dict()
    brand = output['brand']
    ram = output['ram']
    price = output['price']
    camera = output['camera']

    mycursor.execute("insert into result (brand,price, ram, camera)values (%s,%s,%s,%s)",(brand,price,ram,camera))
    mydb.commit()

    mycursor.execute(f"select brand,price,ram,release_date, url, camera, rating from phone, image_url where phone.id = image_url.id and brand like '{brand}%' and price >= {price} and price < {int(price)+5000} and ram like '{ram}' and camera = '{camera}' order by rating desc " )
    data = mycursor.fetchall()

    return render_template("show.html",site_name = site_name,brand=brand,ram=ram, camera=camera, price=price, data=data)

@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template('about_us.html', site_name = site_name)


@app.route('/latest', methods = ['GET'])
def latest():
    mycursor.execute('select brand,ram, price, release_date, url, camera, rating from phone, image_url where phone.id = image_url.id order by release_date desc')
    data = mycursor.fetchall()

    return render_template('latest.html', site_name = site_name, data = data)



if __name__ == '__main__':
    app.run(debug=True)