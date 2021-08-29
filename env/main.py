from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class DATA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow())

    def __repr__(self):
        return '<Employee %r>' % self.id

@app.route('/',methods=['POST','GET'])
def index():

    if  request.method == 'POST':
        employeeID=request.form['id']
        employeePassword=request.form['password']
        newEmployee = DATA(id=employeeID,password=employeePassword)

        try:
            db.session.add(newEmployee)
            db.session.commit()
            return redirect('/')

        except:
            return "There was an error"

    else:
        employees = DATA.query.order_by(DATA.date_created).all()
        return render_template('index.html',employees=employees)

@app.route('/delete/<int:id>')
def delete(id):
    employeeToDelete=DATA.query.get_or_404(id)

    try:
        db.session.delete(employeeToDelete)
        db.session.commit()
        return redirect('/')

    except:
        return "There was an error deleting that employee"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    employeeToUpdate = DATA.query.get_or_404(id)

    if request.method == 'POST':
        employeeToUpdate.id = request.form['id']
        employeeToUpdate.password = request.form['password']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return "There was an error updating"

    else:
        return render_template('update.html', employee=employeeToUpdate)

if __name__ == "__main__":
    app.run(debug=True)
