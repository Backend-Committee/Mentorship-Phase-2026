import customtkinter as ctk
from tkinter import messagebox, filedialog
from engin.db import SessionLocal
from models.Plate import Plate, Category
from models.User import user as User
import shutil
import os
import uuid
import bcrypt

class AdminPage(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_plates = self.tabview.add("Plates")
        self.tab_categories = self.tabview.add("Categories")
        
        self.tab_users = None
        if self.user.role == "super_admin":
            self.tab_users = self.tabview.add("Users")
            self.setup_users_tab()

        self.setup_plates_tab()
        self.setup_categories_tab()

    def setup_plates_tab(self):
        # Add Plate Form
        form_frame = ctk.CTkFrame(self.tab_plates)
        form_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Add New Plate").pack(pady=5)
        
        self.plate_name = ctk.CTkEntry(form_frame, placeholder_text="Details: Name")
        self.plate_name.pack(side="left", padx=5)
        
        self.plate_price = ctk.CTkEntry(form_frame, placeholder_text="Price")
        self.plate_price.pack(side="left", padx=5)

        self.plate_desc = ctk.CTkEntry(form_frame, placeholder_text="Description")
        self.plate_desc.pack(side="left", padx=5)

        # Category Dropdown
        self.category_var = ctk.StringVar(value="Select Category")
        self.category_menu = ctk.CTkOptionMenu(form_frame, variable=self.category_var)
        self.category_menu.pack(side="left", padx=5)
        self.refresh_categories_menu()

        self.image_path_var = ctk.StringVar(value="")
        btn_image = ctk.CTkButton(form_frame, text="Upload Image", command=self.select_image)
        btn_image.pack(side="left", padx=5)

        btn_add = ctk.CTkButton(form_frame, text="Add Plate", command=self.add_plate)
        btn_add.pack(side="left", padx=5)

        # List Plates
        self.plates_list_frame = ctk.CTkScrollableFrame(self.tab_plates, label_text="Existing Plates")
        self.plates_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_plates_list()

    def select_image(self):
        filename = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if filename:
            self.image_path_var.set(filename)
            messagebox.showinfo("Image Selected", f"Selected: {os.path.basename(filename)}")

    def add_plate(self):
        name = self.plate_name.get()
        price = self.plate_price.get()
        desc = self.plate_desc.get()
        cat_name = self.category_var.get()
        img_path = self.image_path_var.get()

        if not name or not price or cat_name == "Select Category":
            messagebox.showerror("Error", "Please fill required fields")
            return

        try:
            price_float = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
            return

        db = SessionLocal()
        category = db.query(Category).filter_by(name=cat_name).first()
        if not category:
            messagebox.showerror("Error", "Invalid Category")
            db.close()
            return

        new_plate = Plate(
            name=name,
            price=price_float,
            description=desc,
            category_id=category.id
        )
        
        # Handle Image
        if img_path:
            # unique id is already in new_plate.picpathid (default lambda)
            # But we need to instantiate it to access it? No, mapped default runs on insert.
            # We can set it explicitly or wait. 
            # Better to set it explicitly for file naming.
            uid = str(uuid.uuid4())
            new_plate.picpathid = uid
            ext = os.path.splitext(img_path)[1]
            dest = f"MetaData/images/{uid}{ext}"
            try:
                shutil.copy(img_path, dest)
            except Exception as e:
                 messagebox.showerror("Error", f"Image copy failed: {e}")
                 db.close()
                 return
        
        db.add(new_plate)
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Plate added")
        self.refresh_plates_list()

    def refresh_categories_menu(self):
        db = SessionLocal()
        cats = db.query(Category).all()
        names = [c.name for c in cats]
        if names:
            self.category_menu.configure(values=names)
            self.category_var.set(names[0])
        else:
            self.category_menu.configure(values=["No Categories"])
            self.category_var.set("No Categories")
        db.close()

    def refresh_plates_list(self):
        for w in self.plates_list_frame.winfo_children():
            w.destroy()
        
        db = SessionLocal()
        plates = db.query(Plate).all()
        for p in plates:
            row = ctk.CTkFrame(self.plates_list_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{p.name} (${p.price})").pack(side="left", padx=10)
            ctk.CTkButton(row, text="Delete", fg_color="red", width=60, command=lambda x=p: self.delete_plate(x.id)).pack(side="right", padx=10)
        db.close()

    def delete_plate(self, pid):
        if messagebox.askyesno("Confirm", "Delete this plate?"):
            db = SessionLocal()
            p = db.query(Plate).get(pid)
            if p:
                db.delete(p)
                db.commit()
            db.close()
            self.refresh_plates_list()

    def setup_categories_tab(self):
        form = ctk.CTkFrame(self.tab_categories)
        form.pack(fill="x", padx=10, pady=10)
        self.cat_name_entry = ctk.CTkEntry(form, placeholder_text="Category Name")
        self.cat_name_entry.pack(side="left", padx=5)
        ctk.CTkButton(form, text="Add Category", command=self.add_category).pack(side="left", padx=5)

        self.cats_list = ctk.CTkScrollableFrame(self.tab_categories)
        self.cats_list.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_categories_list()

    def add_category(self):
        name = self.cat_name_entry.get()
        if not name: return
        db = SessionLocal()
        if db.query(Category).filter_by(name=name).first():
            messagebox.showerror("Error", "Exists")
            db.close()
            return
        db.add(Category(name=name))
        db.commit()
        db.close()
        self.refresh_categories_list()
        self.refresh_categories_menu()

    def refresh_categories_list(self):
        for w in self.cats_list.winfo_children():
            w.destroy()
        db = SessionLocal()
        cats = db.query(Category).all()
        for c in cats:
            row = ctk.CTkFrame(self.cats_list)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=c.name).pack(side="left", padx=10)
            ctk.CTkButton(row, text="Delete", fg_color="red", width=60, command=lambda x=c: self.delete_category(x.id)).pack(side="right", padx=10)
        db.close()

    def delete_category(self, cid):
         db = SessionLocal()
         c = db.query(Category).get(cid)
         if c:
             db.delete(c)
             db.commit()
         db.close()
         self.refresh_categories_list()
         self.refresh_categories_menu()

    def setup_users_tab(self):
        form = ctk.CTkFrame(self.tab_users)
        form.pack(fill="x", padx=10, pady=10)
        
        self.u_name = ctk.CTkEntry(form, placeholder_text="Username")
        self.u_name.pack(side="left", padx=5)
        self.u_pass = ctk.CTkEntry(form, placeholder_text="Password", show="*")
        self.u_pass.pack(side="left", padx=5)
        
        self.u_role = ctk.CTkOptionMenu(form, values=["counter", "admin", "super_admin"])
        self.u_role.pack(side="left", padx=5)
        
        ctk.CTkButton(form, text="Add User", command=self.add_user).pack(side="left", padx=5)

    def add_user(self):
        uname = self.u_name.get()
        upass = self.u_pass.get()
        urole = self.u_role.get()
        
        if not uname or not upass: return
        
        db = SessionLocal()
        if db.query(User).filter_by(username=uname).first():
            messagebox.showerror("Error", "Username exists")
            db.close()
            return
            
        hashed = bcrypt.hashpw(upass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=uname, password=hashed, role=urole)
        db.add(new_user)
        db.commit()
        db.close()
        messagebox.showinfo("Success", "User created")
