from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Config
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Models
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investor_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    loan = db.relationship('Loan', backref='purchases')


# Schemas
class LoanSchema(ma.ModelSchema):
    class Meta:
        model = Loan


loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)


class PurchaseSchema(ma.ModelSchema):
    class Meta:
        model = Purchase


purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)


# Endpoints
# Loan
@app.route("/loan", methods=["POST"])
def add_loan():
    total = request.json['total']
    new_loan = Loan(total=total)
    db.session.add(new_loan)
    db.session.commit()
    result = loan_schema.dump(new_loan).data
    return jsonify({'loan': result})


@app.route("/loan", methods=["GET"])
def get_loan():
    loans = Loan.query.all()
    result = loans_schema.dump(loans).data
    return jsonify({'loans': result})


@app.route("/loan/<id>", methods=["GET"])
def detail_loan(id):
    loan = Loan.query.get(id)
    result = loan_schema.dump(loan).data
    return jsonify({'loan': result})


@app.route("/loan/<id>", methods=["PUT"])
def update_loan(id):
    loan = Loan.query.get(id)
    req_json = request.get_json()
    for k, v in req_json.items():
        setattr(loan, k, v)
    db.session.commit()
    result = loan_schema.dump(loan).data
    return jsonify({"loan": result})


@app.route("/loan/<id>", methods=['DELETE'])
def delete_loan(id):
    loan = Loan.query.get(id)
    db.session.delete(loan)
    db.session.commit()
    result = loan_schema.dump(loan).data
    return jsonify({"loan": result})


# Purchase
@app.route("/purchase", methods=["POST"])
def add_purchase():
    investor_name = request.json['investor_name']
    amount = request.json['amount']
    loan_id = request.json['loan_id']
    loan = Loan.query.get(loan_id)
    new_purchase = Purchase(investor_name=investor_name, amount=amount, loan=loan)
    db.session.add(new_purchase)
    db.session.commit()
    result = purchase_schema.dump(new_purchase).data
    return jsonify({"purchase": result})


@app.route("/purchase", methods=["GET"])
def get_purchase():
    loan_id = request.json['loan_id']
    purchases = Purchase.query.filter(Purchase.loan_id == loan_id)
    result = purchases_schema.dump(purchases).data
    return jsonify({"purchases": result})


@app.route("/purchase/<id>", methods=["GET"])
def detail_purchase(id):
    purchase = Purchase.query.get(id)
    result = purchase_schema.dump(purchase).data
    return jsonify({"purchase": result})


@app.route("/purchase/<id>", methods=["PUT"])
def update_purchase(id):
    purchase = Purchase.query.get(id)
    req_json = request.get_json()
    for k, v in req_json.items():
        setattr(purchase, k, v)
    db.session.commit()
    result = purchase_schema.dump(purchase).data
    return jsonify({"purchase": result})


@app.route("/purchase/<loan_id>", methods=['DELETE'])
def delete_purchase(loan_id):
    purchase = Purchase.query.get(loan_id)
    result = purchase_schema.dump(purchase).data
    db.session.delete(purchase)
    db.session.commit()
    return jsonify({"purchase": result})


if __name__ == '__main__':
    app.run(debug=True)
