import customtkinter as ctk
from engin.db import SessionLocal
from models.Plate import Plate
from models.Order import Order, OrderItems
from tkinter import messagebox
from PIL import Image
import os

class SellingPage(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        self.cart = {} # {plate_id: {"obj": plate_obj, "qty": int}}

        self.grid_columnconfigure(0, weight=3) # Product Grid
        self.grid_columnconfigure(1, weight=1) # Cart

        self.product_frame = ctk.CTkScrollableFrame(self, label_text="Menu")
        self.product_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.cart_frame = ctk.CTkFrame(self)
        self.cart_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.cart_title = ctk.CTkLabel(self.cart_frame, text="Current Order", font=("Roboto", 18, "bold"))
        self.cart_title.pack(pady=10)
        
        self.cart_list = ctk.CTkScrollableFrame(self.cart_frame)
        self.cart_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.total_label = ctk.CTkLabel(self.cart_frame, text="Total: $0.00", font=("Roboto", 16, "bold"))
        self.total_label.pack(pady=10)
        
        self.checkout_btn = ctk.CTkButton(self.cart_frame, text="Checkout", command=self.checkout, fg_color="green")
        self.checkout_btn.pack(pady=20, padx=20)

        self.load_products()

    def load_products(self):
        # Clear existing
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        db = SessionLocal()
        plates = db.query(Plate).all()
        db.close()

        row = 0
        col = 0
        for plate in plates:
            self.create_plate_card(plate, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def create_plate_card(self, plate, r, c):
        card = ctk.CTkFrame(self.product_frame)
        card.grid(row=r, column=c, padx=5, pady=5, sticky="ew")
        
        # Determine image path - simplified
        # Assuming images are stored in a folder named 'plate_images' with name as plate.picpathid + extension
        # For now, just a placeholder or text
        
        name = ctk.CTkLabel(card, text=plate.name, font=("Roboto", 14, "bold"))
        name.pack(pady=5)
        
        price = ctk.CTkLabel(card, text=f"${plate.price:.2f}")
        price.pack(pady=2)
        
        add_btn = ctk.CTkButton(card, text="Add", width=60, command=lambda p=plate: self.add_to_cart(p))
        add_btn.pack(pady=5)

    def add_to_cart(self, plate):
        if plate.id in self.cart:
            self.cart[plate.id]["qty"] += 1
        else:
            self.cart[plate.id] = {"obj": plate, "qty": 1}
        self.update_cart_display()

    def update_cart_display(self):
        for widget in self.cart_list.winfo_children():
            widget.destroy()
        
        total = 0.0
        for pid, item in self.cart.items():
            entry = ctk.CTkFrame(self.cart_list)
            entry.pack(fill="x", pady=2)
            
            p = item["obj"]
            qty = item["qty"]
            cost = p.price * qty
            total += cost
            
            # Layout: Name | Qty controls | Cost | Delete
            ctk.CTkLabel(entry, text=f"{p.name}").pack(side="left", padx=5)
            
            # Controls frame
            controls = ctk.CTkFrame(entry, fg_color="transparent")
            controls.pack(side="left", padx=5)
            
            ctk.CTkButton(controls, text="-", width=30, command=lambda x=pid: self.decrease_qty(x)).pack(side="left", padx=2)
            ctk.CTkLabel(controls, text=f"{qty}", width=30).pack(side="left", padx=2)
            ctk.CTkButton(controls, text="+", width=30, command=lambda x=pid: self.increase_qty(x)).pack(side="left", padx=2)
            
            ctk.CTkButton(entry, text="X", width=30, fg_color="red", command=lambda x=pid: self.remove_item(x)).pack(side="right", padx=5)
            ctk.CTkLabel(entry, text=f"${cost:.2f}").pack(side="right", padx=5)
            
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def increase_qty(self, pid):
        if pid in self.cart:
            self.cart[pid]["qty"] += 1
            self.update_cart_display()

    def decrease_qty(self, pid):
        if pid in self.cart:
            if self.cart[pid]["qty"] > 1:
                self.cart[pid]["qty"] -= 1
            else:
                del self.cart[pid]
            self.update_cart_display()

    def remove_item(self, pid):
        if pid in self.cart:
            del self.cart[pid]
            self.update_cart_display()

    def checkout(self):
        if not self.cart:
            return
            
        db = SessionLocal()
        try:
            new_order = Order(user_id=self.user.id, payment_status=True)
            db.add(new_order)
            db.flush() # get ID
            
            for pid, item in self.cart.items():
                order_item = OrderItems(
                    order_id=new_order.id,
                    plate_id=pid,
                    quantity=item["qty"]
                )
                db.add(order_item)
            
            db.commit()
            messagebox.showinfo("Success", "Order placed successfully!")
            self.cart = {}
            self.update_cart_display()
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"Failed to place order: {e}")
        finally:
            db.close()
