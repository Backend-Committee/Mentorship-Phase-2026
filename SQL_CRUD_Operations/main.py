import re
from db import engine, SessionLocal
from models import Base, Plan, Member

def init_db():
    Base.metadata.create_all(bind=engine)

def seed_plans():
    session = SessionLocal()
    try:
        if session.query(Plan).count() == 0:
            session.add_all([
                Plan(plan_name="Monthly", price=300.0),
                Plan(plan_name="Quarterly", price=800.0),
                Plan(plan_name="Yearly", price=2500.0),
            ])
            session.commit()
    finally:
        session.close()


def create_member(session, first_name, last_name, email, phone, plan_id):
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        print(" Error: Invalid email format.")
        return
    
    plan = session.query(Plan).filter(Plan.plan_id == plan_id).first()
    if not plan:
        print("❌ Error: Plan ID not found.")
        return

    new_member = Member(first_name=first_name, last_name=last_name, email=email, phone=phone, plan_id=plan_id)
    session.add(new_member)
    session.commit()
    print(f"Member {first_name} created!")

def get_member_by_id(session, m_id):
    return session.query(Member).filter(Member.member_id == m_id, Member.is_deleted == False).first()

def update_member_info(session, m_id):
    member = get_member_by_id(session, m_id)
    if not member:
        print("Member not found!")
        return

    print(f"Updating Member: {member.first_name}")
    print("Leave blank to keep current value.")
    
    new_email = input(f"New Email [{member.email}]: ")
    new_phone = input(f"New Phone [{member.phone}]: ")
    new_plan = input(f"New Plan ID [{member.plan_id}]: ")

    if new_email and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', new_email):
        member.email = new_email
    if new_phone and new_phone.isdigit():
        member.phone = new_phone
    if new_plan:
        member.plan_id = int(new_plan)

    session.commit()
    session.refresh(member)
    print("Member info updated successfully!")

def soft_delete_member(session, m_id):
    member = get_member_by_id(session, m_id)
    if member:
        member.is_deleted = True
        session.commit()
        print(f"Member {m_id} soft-deleted.")
    else:
        print("Member not found.")


def main_menu():
    init_db()
    seed_plans()
    session = SessionLocal()
    
    while True:
        print("\n--- Gym Manager CRUD ---")
        print("1. Create Member")
        print("2. List All Members")
        print("3. Update Member Info")
        print("4. Delete Member (Soft)")
        print("5. Exit")
        choice = input("Choice: ")

        if choice == '1':
            create_member(session, input("First: "), input("Last: "), input("Email: "), input("Phone: "), int(input("Plan ID: ")))
        
        elif choice == '2':
            session.expire_all() 
            members = session.query(Member).filter(Member.is_deleted == False).all()
            print("\n--- Active Members List ---")
            for m in members:
                print(f"ID: {m.member_id} | Name: {m.first_name} | Email: {m.email} | Plan: {m.plan.plan_name}")
        
        elif choice == '3':
            try:
                m_id = int(input("Enter Member ID to update: "))
                update_member_info(session, m_id)
            except ValueError:
                print("Invalid ID format.")
                
        elif choice == '4':
            try:
                m_id = int(input("Enter Member ID to delete: "))
                soft_delete_member(session, m_id)
            except ValueError:
                print("Invalid ID format.")
                
        elif choice == '5':
            break
    
    session.close()

if __name__ == "__main__":
    main_menu()