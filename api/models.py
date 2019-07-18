from . import db

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investors = db.relationship('Investor', backref='loan', lazy=True)
    

class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
