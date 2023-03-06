from flask import Flask,render_template,request,url_for
import sqlite3,datetime

app = Flask(__name__)


import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

con = sqlite3.connect("database.db", check_same_thread=False)
cur = con.cursor()
app.route('/')
def page():
    return redirect(url_for('/auth/v1.0'))

@app.route('/auth/v1.0',methods=['GET','POST'])
def auth():
    global con,cur
    print(cur.execute("""SELECT * FROM users""").fetchall())
    if request.method == 'POST':
        phone = request.form.get('phone',None)
        pasw = request.form.get('password',None)
        print(phone,pasw)
        if phone=='' or pasw=='':
            return render_template('auth.html',response = "Вы что-то не ввели")
        user=cur.execute(f"""SELECT * FROM users WHERE phone='{phone}'""").fetchall()
        if len(user)>0:
            if user[0][4]!=str(hash(pasw)):
                return render_template('auth.html',response = "Неверный ПАРОЛЬ!!!")
            else:
                today=datetime.date.today().strftime("%m/%d/%Y")
                print("updating...")
                cur.execute(f"""UPDATE users SET date_update = {today} where phone = {phone}""")
                return  "UPDATED, "+str(cur.execute('SELECT * FROM users').fetchall())
        elif len(user)==0:
            try:
                if carrier._is_mobile(number_type(phonenumbers.parse(phone))):
                    pass
                else:
                    return render_template('auth.html',response = "Неверный номер телефона")
            except:
                return render_template('auth.html',response = "Неверный номер телефона")
            if len(pasw)>=8 and len([i for i in pasw if i in list('1234567890')])>0 and len([i for i in pasw if i in list('qwertyuiopasdfghjklzxcvbnm')])>0 and len([i for i in pasw if i in list('qwertyuiopasdfghjklzxcvbnm'.upper())])>0 and len([i for i in pasw if i in list('!@#$%^&*()_+-=/.,[]{}')])>0:
                pass
            else:
                return render_template('auth.html',response = "Слишком простой пароль!")
            last_id=len(cur.execute("""SELECT * FROM users""").fetchall())
            today=datetime.date.today().strftime("%m/%d/%Y")
            cur.execute(f"""INSERT INTO users VALUES({last_id+1},'{today}','{today}','{phone}','{hash(pasw)}')""")
            con.commit()
            return "CREATED, "+str(cur.execute('SELECT * FROM users').fetchall())
    
            
                
            
    else:
        return render_template('auth.html')
        
app.run()
