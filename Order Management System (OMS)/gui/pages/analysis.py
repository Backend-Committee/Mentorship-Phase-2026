import customtkinter as ctk
from engin.db import SessionLocal
from models.Order import Order
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class AnalysisPage(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.plot_ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        button_refresh = ctk.CTkButton(self, text="Refresh Data", command=self.load_data)
        button_refresh.grid(row=1, column=0, pady=10)

        self.load_data()

    def load_data(self):
        db = SessionLocal()
        
        # Determine time range
        now = datetime.datetime.utcnow()
        if self.user.role == "super_admin":
            start_date = datetime.datetime.min
        else:
            start_date = now - datetime.timedelta(days=7)
            
        orders = db.query(Order).filter(Order.created_at >= start_date).all()
        
        # Aggregate sales by date
        sales_data = {} # Date string -> total amount
        
        for order in orders:
            order_total = 0
            for item in order.items:
                if item.plate:
                    order_total += item.quantity * item.plate.price
            
            date_str = order.created_at.strftime("%Y-%m-%d")
            sales_data[date_str] = sales_data.get(date_str, 0) + order_total
            
        db.close()
        
        # Sorting
        sorted_dates = sorted(sales_data.keys())
        amounts = [sales_data[d] for d in sorted_dates]

        # Plotting
        self.plot_ax.clear()
        self.plot_ax.bar(sorted_dates, amounts)
        self.plot_ax.set_title("Sales Overview")
        self.plot_ax.set_ylabel("Revenue ($)")
        self.plot_ax.set_xlabel("Date")
        self.plot_ax.tick_params(axis='x', rotation=45)
        
        self.fig.tight_layout()
        self.canvas.draw()
