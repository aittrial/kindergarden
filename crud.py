from sqlalchemy.orm import Session
from models import Expense  # Убедитесь, что название модели совпадает с вашим
from database import SessionLocal

def add_expense(amount, description, date):
    db = SessionLocal()
    try:
        new_expense = Expense(amount=amount, description=description, date=date)
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
        return new_expense
    finally:
        db.close()

def get_all_expenses():
    db = SessionLocal()
    try:
        return db.query(Expense).all()
    finally:
        db.close()

def delete_expense(expense_id):
    db = SessionLocal()
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if expense:
            db.delete(expense)
            db.commit()
        return True
    finally:
        db.close()
