from engin.db import init_db, SessionLocal
from models.User import user
from models.Plate import Plate
from models.Order import Order
import bcrypt

def create_super_admin():
    db = SessionLocal()
    # Check if super admin exists
    admin = db.query(user).filter_by(role="super_admin").first()
    if not admin:
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        new_admin = user(
            username="admin", 
            password=hashed_password.decode('utf-8'), 
            role="super_admin"
        )
        db.add(new_admin)
        db.commit()
        print("Super Admin created: admin / admin123")
    else:
        print("Super Admin already exists.")
    db.close()

if __name__ == "__main__":
    init_db()
    create_super_admin()
