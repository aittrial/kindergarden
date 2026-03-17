from sqlalchemy.orm import Session
from models import Expense
from database import SessionLocal

def get_all_expenses():
    db = SessionLocal()
    try:
        return db.query(Expense).all()
    finally:
        db.close()

def add_expense(date, category, amount, description, comment):
    db = SessionLocal()
    try:
        new_expense = Expense(
            date=date,
            category=category,
            amount=amount,
            description=description,
            comment=comment
        )
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
        return new_expense
    finally:
        db.close()

def delete_expense(expense_id):
    db = SessionLocal()
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if expense:
            db.delete(expense)
            db.commit()
    finally:
        db.close()
