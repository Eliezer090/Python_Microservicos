from dataclasses import dataclass
import requests
from flask import Flask,jsonify,abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate
from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)
#migrate = Migrate(app, db)

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(100))
    image = db.Column(db.String(100))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    #Esta URL é la do django, esta request vai cair no views.UserAPIView
    req = requests.get('http://167.172.159.3:8000/api/user')
    json = req.json()

    try:
        productUser = ProductUser(user_id=json['id'],product_id=id)
        db.session.add(productUser)
        db.session.commit()
        publish('product_liked',id)
    except:
        abort(400,'You aready liked this product')

    return jsonify({
        'message':'sucess'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
