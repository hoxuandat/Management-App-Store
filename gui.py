import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter
import bcrypt
import sqlalchemy as sa
from database import get_session, Product, Customer, Order, OrderItem, Staff 
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
import threading
import numpy as np
from collections import Counter
import time
import random
import copy
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression

### Tao doi tuong engine ket noi voi database SQLite supermarket.db####
engine = sa.create_engine('sqlite:///supermarket.db')


### Tao base class cho cac model####
Base = declarative_base()

# Khóa đồng bộ
order_lock = threading.Lock()

# Giỏ hàng (List)
cart = {
    'products': [],
    'customer': None,
    'order': None
}
new_order = True


# Font settings
FONT1 = ('Helvetica', 25, 'bold')
FONT2 = ('Arial', 17, 'bold')
FONT3 = ('Arial', 13, 'bold')
FONT4 = ('Arial', 13, 'bold', 'underline')

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('App Store Management')
        self.geometry('700x500')
        self.config(bg='#001220')


        # Login window
        self.login_window()

    # login and signup windows 
    def login_window(self):
        self.login_frame = customtkinter.CTkFrame(
            self, bg_color='#001220', fg_color='#001220', width=470, height=360)
        self.login_frame.place(x=0, y=0)

        login_label2 = customtkinter.CTkLabel(
            self.login_frame, font=FONT1, text='Đăng nhập', text_color='#fff', bg_color='#001220')
        login_label2.place(x=280, y=20)

        self.username_entry = customtkinter.CTkEntry(
            self.login_frame, font=FONT2, text_color='#fff', fg_color='#001a2e', bg_color='#121111',
            border_color='#004780', border_width=3, placeholder_text='Username', placeholder_text_color='#a3a3a3',
            width=200, height=50)
        self.username_entry.place(x=230, y=80)

        self.password_entry = customtkinter.CTkEntry(
            self.login_frame, font=FONT2, show='*', text_color='#fff', fg_color='#001a2e', bg_color='#121111',
            border_color='#004780', border_width=3, placeholder_text='Password', placeholder_text_color='#a3a3a3',
            width=200, height=50)
        self.password_entry.place(x=230, y=150)

        login_button = customtkinter.CTkButton(
            self.login_frame, command=self.handle_login, font=FONT2, text_color='#fff', text='Đăng nhập',
            fg_color='#00965d', hover_color='#006e44', bg_color='#121111', cursor='hand2', corner_radius=5, width=140)
        login_button.place(x=230, y=220)

        # Signup button
        signup_label = customtkinter.CTkLabel(
            self.login_frame, font=FONT3, text='Chưa có tài khoản?', text_color='#fff', bg_color='#001220')
        signup_label.place(x=230, y=250)

        signup_button = customtkinter.CTkButton(
            self.login_frame, command=self.switch_to_signup, font=FONT4, text_color='#00bf77', text='Đăng ký',
            fg_color='#001220', hover_color='#001220', cursor='hand2', width=40)
        signup_button.place(x=395, y=250)

    def signup_window(self):
        self.signup_frame = customtkinter.CTkFrame(
            self, bg_color='#001220', fg_color='#001220', width=470, height=360)
        self.signup_frame.place(x=0, y=0)

        signup_label = customtkinter.CTkLabel(
            self.signup_frame, font=FONT1, text='Đăng ký', text_color='#fff', bg_color='#001220')
        signup_label.place(x=280, y=20)

        self.username_entry = customtkinter.CTkEntry(
            self.signup_frame, font=FONT2, text_color='#fff', fg_color='#001a2e', bg_color='#121111',
            border_width=3, placeholder_text='Username', placeholder_text_color='#a3a3a3', width=200, height=50)
        self.username_entry.place(x=230, y=80)

        self.password_entry = customtkinter.CTkEntry(
            self.signup_frame, font=FONT2, show='*', text_color='#fff', fg_color='#001a2e', bg_color='#121111',
            border_width=3, placeholder_text='Password', placeholder_text_color='#a3a3a3', width=200, height=50)
        self.password_entry.place(x=230, y=150)

        signup_button = customtkinter.CTkButton(
            self.signup_frame, command=self.handle_signup, font=FONT2, text_color='#fff', text='Đăng ký',
            fg_color='#00965d', hover_color='#006e44', bg_color='#121111', cursor='hand2', corner_radius=5, width=120)
        signup_button.place(x=230, y=220)

        # Login button
        login_label = customtkinter.CTkLabel(
            self.signup_frame, font=FONT3, text='Đã có tài khoản rồi?', text_color='#fff', bg_color='#001220')
        login_label.place(x=230, y=250)

        login_button = customtkinter.CTkButton(
            self.signup_frame, command=self.switch_to_login, font=FONT4, text_color='#00bf77', text='Đăng nhập',
            fg_color='#001220', hover_color='#001220', cursor='hand2', width=40)
        login_button.place(x=395, y=250)

    def switch_to_signup(self):
        self.login_frame.destroy()
        self.signup_window()

    def switch_to_login(self):
        self.signup_frame.destroy()
        self.login_window()

    def handle_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username != '' and password != '':
            try:
                session = get_session()
                existing_user = session.query(Staff).filter_by(name=username).first()

                if existing_user:
                    messagebox.showerror('THÔNG BÁO', 'Tên người dùng đã tồn tại.')
                    return

                encoded_password = password.encode('utf-8')
                hashed_password = bcrypt.hashpw(
                    encoded_password, bcrypt.gensalt()).decode('utf-8')

                new_staff = Staff(name=username, password=hashed_password)
                session.add(new_staff)
                session.commit()
                session.close()

                messagebox.showinfo('THÔNG BÁO', 'Tài khoản đã được tạo')

                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)

            except Exception as e:
                messagebox.showinfo('THÔNG BÁO', str(e))
        else:
            messagebox.showinfo('THÔNG BÁO', 'Nhập lại dữ liệu')

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username != '' and password != '':
            try:
                session = get_session()
                user = session.query(Staff).filter_by(name=username).first()
                session.close()

                if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    messagebox.showinfo('THÔNG BÁO', 'Đăng nhập thành công!')
                    self.login_frame.destroy()
                    self.create_store_interface()  # Gọi hàm để tạo giao diện cửa hàng
                   
                else:
                    messagebox.showerror('THÔNG BÁO', 'Password hoặc Username không hợp lệ!')
            except Exception as e:
                messagebox.showerror('THÔNG BÁO', str(e))
        else:
            messagebox.showerror('THÔNG BÁO', 'Nhập lại dữ liệu.')

    def create_store_interface(self):
        # Create Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs and frames
        self.tabs = ['Sản phẩm', 'Khách hàng', 'Đơn hàng', 'Phân tích', 'Lịch sử đơn hàng']
        self.frames = [tk.Frame(self.notebook, bg='#001220') for _ in range(len(self.tabs))]
        for i, tab in enumerate(self.tabs):
            self.notebook.add(self.frames[i], text=tab)

        # truy cập frames bằng index
        self.init_product_tab(self.frames[0])  
        self.init_customer_tab(self.frames[1])
        self.init_order_tab(self.frames[2]) 
        self.init_order_history_tab(self.frames[3])  
        self.init_analysis_tab(self.frames[4])  
        

        self.notebook.pack() # Hiển thị Notebook chứa các tab

    def init_product_tab(self, frame):
        frame = self.frames[0]
        self.product_treeview = ttk.Treeview(frame, columns=('ID', 'Tên', 'Giá', 'Số lượng'), show='headings')
        for col in ('ID', 'Tên', 'Giá', 'Số lượng'):
            self.product_treeview.heading(col, text=col)
            self.product_treeview.column(col, width=100, minwidth=50)
        self.product_treeview.pack(side='left', fill='both', expand=True)
        self.refresh_product_treeview()

        # Right frame
        right_frame = tk.Frame(frame, bg='#001220')
        right_frame.pack(side='right', fill='y')

        # Trường NHập vào

        self.product_name_label = tk.Label(right_frame, text='Tên sản phẩm:', font=FONT3, bg='#001220', fg='white')
        self.product_name_label.pack(fill='x')
        self.product_name_entry = tk.Entry(right_frame, font=FONT3, bg='#001220', fg='white')
        self.product_name_entry.pack(fill='x', padx=10, pady=5)

        self.product_price_label = tk.Label(right_frame, text='Giá:', font=FONT3, bg='#001220', fg='white')
        self.product_price_label.pack(fill='x')
        self.product_price_entry = tk.Entry(right_frame, font=FONT3, bg='#001220', fg='white')
        self.product_price_entry.pack(fill='x', padx=10, pady=5)

        self.product_quantity_label = tk.Label(right_frame, text='Số lượng:', font=FONT3, bg='#001220', fg='white')
        self.product_quantity_label.pack(fill='x')
        self.product_quantity_entry = tk.Entry(right_frame, font=FONT3, bg='#001220', fg='white')
        self.product_quantity_entry.pack(fill='x', padx=10, pady=5)

        # Buttons
        self.add_product_button = tk.Button(right_frame, text='Thêm', font=FONT3, command=self.handle_add_product)
        self.add_product_button.pack(fill='x', padx=10, pady=5)
        self.edit_product_button = tk.Button(right_frame, text='Sửa', font=FONT3, command=self.open_edit_product_window)
        self.edit_product_button.pack(fill='x', padx=10, pady=5)
        self.delete_product_button = tk.Button(right_frame, text='Xoá', font=FONT3, command=self.handle_delete_product)
        self.delete_product_button.pack(fill='x', padx=10, pady=5)
        self.add_to_cart_product_button = tk.Button(right_frame, text='Thêm vào giỏ', font=FONT3, command=self.handle_add_to_cart_product)
        self.add_to_cart_product_button.pack(fill='x', padx=10, pady=5)

         # Thêm dữ liệu mẫu vào treeview (không lưu vào database)
        sample_data = [
            (1, "Bánh mỳ", 10000, 10),
            (2, "Thịt gà", 70000, 5),
            
        ]
        for data in sample_data:
            self.product_treeview.insert('', tk.END, values=data)
    def init_customer_tab(self, frame):
        frame = self.frames[1]
        self.customer_treeview = ttk.Treeview(frame, columns=('ID', 'Tên', 'Số điện thoại', 'Địa chỉ'), show='headings')
        for col in ('ID', 'Tên', 'Số điện thoại', 'Địa chỉ'):
            self.customer_treeview.heading(col, text=col)
            self.customer_treeview.column(col, width=100, minwidth=50)
        self.customer_treeview.pack(side='left', fill='both', expand=True)
        self.refresh_customer_treeview()

        # Right frame
        right_frame = tk.Frame(frame, bg='#001220')
        right_frame.pack(side='right', fill='y')

        # Trường nhập vào
        self.customer_name_entry = tk.Entry(right_frame, font=FONT3, bg='#001220', fg='white')
        self.customer_phone_entry = tk.Entry(right_frame, font=FONT3, bg='#001220', fg='white')
        self.customer_address_entry = tk.Entry(right_frame, font=FONT3, bg='#001220', fg='white')

        for i, label_text in enumerate(('Tên khách hàng:', 'Số điện thoại:', 'Địa chỉ:')):
            label = tk.Label(right_frame, text=label_text, font=FONT3, bg='#001220', fg='white')
            label.pack(fill='x')
            # Sử dụng self.entry để thiết lập thuộc tính
            if i == 0:
                self.customer_name_entry.pack(fill='x', padx=10, pady=5)
            elif i == 1:
                self.customer_phone_entry.pack(fill='x', padx=10, pady=5)
            elif i == 2:
                self.customer_address_entry.pack(fill='x', padx=10, pady=5)

        # Buttons
        self.add_customer_button = tk.Button(right_frame, text='Thêm', font=FONT3, command=self.handle_add_customer)
        self.add_customer_button.pack(fill='x', padx=10, pady=5)
        self.edit_customer_button = tk.Button(right_frame, text='Sửa', font=FONT3, command=self.open_edit_customer_window)
        self.edit_customer_button.pack(fill='x', padx=10, pady=5)
        self.delete_customer_button = tk.Button(right_frame, text='Xoá', font=FONT3, command=self.handle_delete_customer)
        self.delete_customer_button.pack(fill='x', padx=10, pady=5)
        self.add_to_cart_customer_button = tk.Button(right_frame, text='Thêm vào giỏ', font=FONT3, command=self.handle_add_to_cart_customer)
        self.add_to_cart_customer_button.pack(fill='x', padx=10, pady=5)
                 # Thêm dữ liệu mẫu vào treeview (không lưu vào database)
        sample_data = [
            (1, "Hồ Xuân Đạt", "21020728", "Hà Đông"),
            (2, "Nguyễn Mạnh Cường", "21021516", "Cầu Giấy"),
            (3, "Vũ Phương Nhi", "21021536", "Đống Đa")
            
        ]
        for data in sample_data:
            self.customer_treeview.insert('', tk.END, values=data)

    def init_order_tab(self, frame):
        frame = self.frames[2]
        #khung chứa thông tin đơn hàng
        order_info_frame = tk.Frame(frame, bg='#001220')
        order_info_frame.pack(side='top', fill='x')


        # Label hiển thị tên khách hàng và số lượng sản phẩm đã chọn
        self.order_summary_label = tk.Label(frame, text="", font=FONT3, bg='#001220', fg='white')
        self.order_summary_label.pack(side='top', fill='x')

        # Treeview hiển thị chi tiết đơn hàng
        self.order_treeview = ttk.Treeview(frame, columns=('ID', 'Khách hàng', 'Sản phẩm', 'Tổng giá trị'), show='headings')
        for col in ('ID', 'Khách hàng','Sản phẩm', 'Tổng giá trị'):
            self.order_treeview.heading(col, text=col)
            self.order_treeview.column(col, width=120, minwidth=50)
        self.order_treeview.pack(side='left', fill='both', expand=True)
        self.refresh_order_treeview()

        # Right frame
        right_frame = tk.Frame(frame, bg='#001220')
        right_frame.pack(side='right', fill='y')

        
        # Khung chứa bill khách hàng
        bill_frame = tk.Frame(right_frame, bg='#001220')
        bill_frame.pack(fill='both', expand=True, padx=10, pady=5)

                
        # Label hiển thị bill
        self.bill_label = tk.Label(bill_frame, text="Hóa đơn", font=FONT3, bg='#001220', fg='white')
        self.bill_label.pack()

                
        # Textbox hiển thị nội dung bill
        self.bill_textbox = tk.Text(bill_frame, font=FONT3, bg='#001220', fg='white', state='disabled')
        self.bill_textbox.pack(fill='both', expand=True)


        # Buttons
        # Nút "Tạo đơn hàng"

        self.create_order_button = tk.Button(right_frame, text='Tạo đơn hàng', font=FONT3, command=self.handle_create_order)
        self.create_order_button.pack(fill='x', padx=10, pady=5)

        # Nút "Xem đơn hàng"
        self.view_order_button = tk.Button(right_frame, text='Xem đơn hàng', font=FONT3, command=self.handle_view_order)
        self.view_order_button.pack(fill='x', padx=10, pady=5)
 


    def init_order_history_tab(self, frame):
        frame = self.frames[4]
        self.order_history_treeview = ttk.Treeview(frame, columns=('ID', 'Khách hàng', 'Sản phẩm', 'Tổng giá trị', 'Ngày tạo'), show='headings')
        for col in ('ID', 'Khách hàng', 'Sản phẩm', 'Tổng giá trị', 'Ngày tạo'):
            self.order_history_treeview.heading(col, text=col)
            self.order_history_treeview.column(col, width=100, minwidth=50)
        self.order_history_treeview.pack(side='left', fill='both', expand=True)

        self.refresh_order_history_treeview()

    def init_analysis_tab(self, frame):
        frame = self.frames[3]

        # Label
        analysis_label = tk.Label(frame, text="Phân tích dữ liệu", font=FONT1, bg='#001220', fg='white')
        analysis_label.pack(pady=10)

        # Nút "Phân tích dữ liệu"
        analyze_button = tk.Button(frame, text='Phân tích', font=FONT3, command=self.perform_data_analysis)
        analyze_button.pack(fill='x', padx=10, pady=5)

        # Textbox hiển thị kết quả phân tích
        self.analysis_results_textbox = tk.Text(frame, font=FONT3, bg='#001220', fg='white', state='disabled')
        self.analysis_results_textbox.pack(fill='both', expand=True, padx=10, pady=5)


    def handle_add_product(self):
        name = self.product_name_entry.get()
        price = self.product_price_entry.get()
        quantity = self.product_quantity_entry.get()
        try:
            price = float(price)
            quantity = int(quantity)
            session = get_session()
            product = Product(name=name, price=price, quantity=quantity)
            session.add(product)
            session.commit()
            session.close()
            self.refresh_product_treeview()
            messagebox.showinfo("THÔNG BÁO", "Thêm sản phẩm thành công")
        except ValueError as e:
            messagebox.showwarning("THÔNG BÁO", f"Lỗi: {str(e)}")

    def open_edit_product_window(self):
        selected_item = self.product_treeview.selection()
        if selected_item:
            item_data = self.product_treeview.item(selected_item)
            product_id = item_data['values'][0]
            name = item_data['values'][1]
            price = item_data['values'][2]
            quantity = item_data['values'][3]

            edit_window = tk.Toplevel(self)
            edit_window.title("Sửa sản phẩm")
            edit_window.geometry("500x170")

            # Dùng grid cho toàn bộ window
            edit_window.grid_rowconfigure(0, weight=1)
            edit_window.grid_columnconfigure(0, weight=1)

            # Tạo Frame trung gian
            main_frame = tk.Frame(edit_window)
            main_frame.grid(row=0, column=0, sticky="nsew")

            # cấu hình grid weights cho cột
            main_frame.grid_columnconfigure(0, weight=1) 
            main_frame.grid_columnconfigure(1, weight=3) 

            # Dùng grid layout và sticky cho frame trung gian
            name_label = tk.Label(main_frame, text="Tên sản phẩm:")
            name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            name_entry = tk.Entry(main_frame)
            name_entry.insert(0, name)
            name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

            price_label = tk.Label(main_frame, text="Giá:")
            price_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            price_entry = tk.Entry(main_frame)
            price_entry.insert(0, price)
            price_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

            quantity_label = tk.Label(main_frame, text="Số lượng:")
            quantity_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            quantity_entry = tk.Entry(main_frame)
            quantity_entry.insert(0, quantity)
            quantity_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

            save_button = tk.Button(main_frame, text="Lưu", command=lambda: self.handle_save_product(
                edit_window, product_id, name_entry, price_entry, quantity_entry))
            save_button.grid(row=3, columnspan=2, pady=10)

        else:
            messagebox.showinfo("THÔNG BÁO", "Vui lòng chọn sản phẩm cần sửa.")

    def handle_save_product(self, edit_window, product_id, name_entry, price_entry, quantity_entry):
        name = name_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()

        try:
            price = float(price)
            quantity = int(quantity)
            session = get_session()
            product = session.query(Product).filter_by(id=product_id).first()
            if product:
                product.name = name
                product.price = price
                product.quantity = quantity
                session.commit()
                edit_window.destroy()
                self.refresh_product_treeview()
               
                messagebox.showinfo("THÔNG BÁO", "Sửa sản phẩm thành công")
            session.close()
        except ValueError as e:
            messagebox.showwarning("THÔNG BÁO", f"Lỗi: {str(e)}")

    def handle_delete_product(self):
        selected_item = self.product_treeview.selection()
        if selected_item:
            product_id = self.product_treeview.item(selected_item, 'values')[0]
            try:
                session = get_session()
                product = session.query(Product).filter_by(id=product_id).first()
                if product:
                    # Kiểm tra xem sản phẩm có đang được sử dụng trong đơn hàng nào không
                    order_items = session.query(OrderItem).filter_by(product_id=product_id).all()
                    if order_items:
                        messagebox.showwarning("THÔNG BÁO", "Không thể xóa sản phẩm này vì nó đang được sử dụng trong đơn hàng.")
                    else:
                        session.delete(product)
                        session.commit()
                        self.refresh_product_treeview()
                        messagebox.showinfo("THÔNG BÁO", "Xóa sản phẩm thành công")
                session.close()
            except ValueError as e:
                messagebox.showwarning("THÔNG BÁO", f"Lỗi: {str(e)}")
        else:
            messagebox.showinfo("THÔNG BÁO", "Vui lòng chọn sản phẩm cần xóa")

    def handle_add_customer(self):
        name = self.customer_name_entry.get()
        phone = self.customer_phone_entry.get()
        address = self.customer_address_entry.get()
        try:
            session = get_session()
            customer = Customer(name=name, phone=phone, address=address)
            session.add(customer)
            session.commit()
            session.close()
            self.refresh_customer_treeview()
            messagebox.showinfo("THÔNG BÁO", "Thêm khách hàng thành công")
        except ValueError as e:
            messagebox.showwarning("THÔNG BÁO", f"Lỗi: {str(e)}")

    def open_edit_customer_window(self):
        selected_item = self.customer_treeview.selection()
        if selected_item:
            item_data = self.customer_treeview.item(selected_item)
            customer_id = item_data['values'][0]
            name = item_data['values'][1]
            phone = item_data['values'][2]
            address = item_data['values'][3]

            edit_window = tk.Toplevel(self)
            edit_window.title("Sửa khách hàng")
            edit_window.geometry("500x170")

            # Dùng grid cho toàn bộ window
            edit_window.grid_rowconfigure(0, weight=1)
            edit_window.grid_columnconfigure(0, weight=1)

            # Tạo Frame trung gian
            main_frame = tk.Frame(edit_window)
            main_frame.grid(row=0, column=0, sticky="nsew")

            # Cấu hình grid weights cho cột
            main_frame.grid_columnconfigure(0, weight=1)  
            main_frame.grid_columnconfigure(1, weight=3)  

            # Dùng grid layout và sticky cho frame trung gian
            name_label = tk.Label(main_frame, text="Tên khách hàng:")
            name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            name_entry = tk.Entry(main_frame)
            name_entry.insert(0, name)
            name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

            phone_label = tk.Label(main_frame, text="Số điện thoại:")
            phone_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            phone_entry = tk.Entry(main_frame)
            phone_entry.insert(0, phone)
            phone_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

            address_label = tk.Label(main_frame, text="Địa chỉ:")
            address_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            address_entry = tk.Entry(main_frame)
            address_entry.insert(0, address)
            address_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

            save_button = tk.Button(main_frame, text="Lưu", command=lambda: self.handle_save_customer(
                edit_window, customer_id, name_entry, phone_entry, address_entry))
            save_button.grid(row=3, columnspan=2, pady=10)

        else:
            messagebox.showinfo("THÔNG BÁO", "Vui lòng chọn khách hàng cần sửa.")


    def handle_save_customer(self, edit_window, customer_id, name_entry, phone_entry, address_entry):
        name = name_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()

        try:
            session = get_session()
            customer = session.query(Customer).filter_by(id=customer_id).first()
            if customer:
                customer.name = name
                customer.phone = phone
                customer.address = address
                session.commit()
                edit_window.destroy()
                self.refresh_customer_treeview()
                messagebox.showinfo("THÔNG BÁO", "Sửa khách hàng thành công")
            session.close()
        except ValueError as e:
            messagebox.showwarning("THÔNG BÁO", f"Lỗi: {str(e)}")

    def handle_delete_customer(self):
        selected_item = self.customer_treeview.selection()
        if selected_item:
            customer_id = self.customer_treeview.item(selected_item, 'values')[0]
            try:
                session = get_session()
                customer = session.query(Customer).filter_by(id=customer_id).first()
                if customer:
                    session.delete(customer)
                    session.commit()
                    self.refresh_customer_treeview()
                    messagebox.showinfo("THÔNG BÁO", "Xóa khách hàng thành công")
                session.close()
            except ValueError as e:
                messagebox.showwarning("THÔNG BÁO", f"Lỗi: {str(e)}")
        else:
            messagebox.showinfo("THÔNG BÁO", "Vui lòng chọn khách hàng cần xóa")

    def handle_add_to_cart_product(self):
        global cart
        selected_item = self.product_treeview.selection()
        if selected_item:
            product_id, _, _, quantity = self.product_treeview.item(selected_item)['values']
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError("Số lượng phải lớn hơn 0.")
            except ValueError as e:
                messagebox.showwarning("THÔNG BÁO", f"Lỗi: {str(e)}")
                return

            
            session = get_session()
            product = session.query(Product).filter_by(id=int(product_id)).first()
            session.close()

            if product:
                if product.quantity >= quantity:
                    cart['products'].append({'product': product, 'quantity': quantity})
                    messagebox.showinfo("THÔNG BÁO", f"Đã thêm {quantity} {product.name} vào giỏ hàng.")

                    # Cập nhật order_summary_label
                    self.update_order_summary()

                    # Cập nhật treeview với giỏ hàng
                    self.refresh_order_treeview()
            else:
                messagebox.showwarning("THÔNG BÁO", "Lỗi: Sản phẩm không tồn tại.")
        else:
            messagebox.showinfo("THÔNG BÁO", "Vui lòng chọn sản phẩm cần thêm vào giỏ hàng.")
   


    def handle_add_to_cart_customer(self):
        global cart
        selected_item = self.customer_treeview.selection()
        if selected_item:
            customer_id = self.customer_treeview.item(selected_item, 'values')[0]
            session = get_session()
            customer = session.query(Customer).filter_by(id=int(customer_id)).first()
            session.close()
            if customer:
                cart['customer'] = customer
                messagebox.showinfo("THÔNG BÁO", f"Đã chọn khách hàng {customer.name}.")

                # Cập nhật order_summary_label
                self.update_order_summary()

                # Cập nhật treeview với giỏ hàng
                self.refresh_order_treeview()

            else:
                messagebox.showwarning("THÔNG BÁO", "Lỗi: Khách hàng không tồn tại.")
        else:
            messagebox.showinfo("THÔNG BÁO", "Vui lòng chọn khách hàng.")


    def handle_create_order(self):
        global cart, new_order
        if cart['products'] and cart['customer']:
            try:
                session = get_session()

                # Tạo đơn hàng mới
                if new_order:
                    order = Order(customer_id=cart['customer'].id, total=0)
                    session.add(order)
                    cart['order'] = order
                    new_order = False
                else:
                    order = cart['order']

                for item in cart['products']:
                    product = item['product']
                    quantity = item['quantity']

                    # Kiểm tra xem sản phẩm đã có trong đơn hàng chưa
                    existing_item = session.query(OrderItem).filter_by(order=order, product=product).first()
                    if existing_item:
                        existing_item.quantity += quantity
                    else:
                        order_item = OrderItem(order=order, product=product, quantity=quantity)
                        session.add(order_item)

                # Cập nhật số lượng sản phẩm sau khi tạo đơn thành công
                for item in cart['products']:
                    product = item['product']
                    quantity = item['quantity']
                    product.quantity -= quantity

                order.total = self.calculate_total_value()
                session.commit()


                order.total = self.calculate_total_value()
                session.commit()

                # Hiển thị hóa đơn
                self.display_bill(order)
                session.close()

                # Reset danh sách sản phẩm trong giỏ, giữ lại khách hàng và order
                cart['products'] = []  
                new_order = True

                self.refresh_product_treeview()  # Cập nhật product_treeview
                self.refresh_order_treeview() # Cập nhật order_treeview
                self.update_order_summary()  # Cập nhật order_summary_label
                                
                # Cập nhật lịch sử đơn hàng
                self.refresh_order_history_treeview()
                messagebox.showinfo("THÔNG BÁO", "Tạo đơn hàng thành công")

            except ValueError as e:
                messagebox.showwarning("THÔNG BÁO", f"Lỗi: {str(e)}")
        else:
            messagebox.showinfo("THÔNG BÁO", "Vui lòng chọn sản phẩm và khách hàng.")


    def handle_view_order(self):
        selected_item = self.order_treeview.selection()
        if selected_item:
            order_id = self.order_treeview.item(selected_item)['values'][0]
            session = get_session()
            order = session.query(Order).filter_by(id=order_id).first()
            session.close()
            if order:
                self.display_bill(order)
            else:
                messagebox.showwarning("THÔNG BÁO", "Lỗi: Đơn hàng không tồn tại.")
        else:
            messagebox.showinfo("THÔNG BÁO", "Vui lòng chọn đơn hàng cần xem.")


    def refresh_product_treeview(self):
        self.product_treeview.delete(*self.product_treeview.get_children())
        session = get_session()
        products = session.query(Product).all()
        for product in products:
            self.product_treeview.insert('', tk.END, values=(product.id, product.name, product.price, product.quantity))
        session.close()

    def open_edit_order_window(self):
        global cart
        if cart['products'] and cart['customer']:
            edit_window = tk.Toplevel(self)
            edit_window.title("Chỉnh sửa đơn hàng")
            edit_window.geometry("500x300")

            # Tạo Treeview để hiển thị giỏ hàng
            cart_treeview = ttk.Treeview(edit_window, columns=('ID', 'Sản phẩm', 'Số lượng', 'Giá'), show='headings')
            for col in ('ID', 'Sản phẩm', 'Số lượng', 'Giá'):
                cart_treeview.heading(col, text=col)
                cart_treeview.column(col, width=80, minwidth=50)
            cart_treeview.pack(side='top', fill='both', expand=True)

            for i, item in enumerate(cart['products']):
                product = item['product']
                quantity = item['quantity']
                cart_treeview.insert('', tk.END, values=(i+1, product.name, quantity, product.price * quantity))

            # Hàm chỉnh sửa số lượng sản phẩm trong giỏ hàng
            def handle_edit_cart_item():
                global cart
                selected_item = cart_treeview.selection()
                if selected_item:
                    item_id = int(cart_treeview.item(selected_item)['values'][0]) - 1  # Lấy id của item
                    product = cart['products'][item_id]['product']

                    # Tạo cửa sổ để nhập số lượng mới
                    new_quantity_window = tk.Toplevel(edit_window)
                    new_quantity_window.title("Nhập số lượng mới")

                    new_quantity_label = tk.Label(new_quantity_window, text="Số lượng:")
                    new_quantity_label.pack()
                    new_quantity_entry = tk.Entry(new_quantity_window)
                    new_quantity_entry.pack()

                    def save_new_quantity():
                        global cart
                        try:
                            new_quantity = int(new_quantity_entry.get())
                            if new_quantity > 0:
                                cart['products'][item_id]['quantity'] = new_quantity
                                self.refresh_order_treeview()
                                new_quantity_window.destroy()
                            else:
                                messagebox.showwarning("THÔNG BÁO", "Số lượng phải lớn hơn 0.")
                        except ValueError:
                            messagebox.showwarning("THÔNG BÁO", "Vui lòng nhập số nguyên.")

                    save_button = tk.Button(new_quantity_window, text="Lưu", command=save_new_quantity)
                    save_button.pack()

            # Hàm xóa sản phẩm khỏi giỏ hàng
            def handle_delete_cart_item():
                global cart
                selected_item = cart_treeview.selection()
                if selected_item:
                    item_id = int(cart_treeview.item(selected_item)['values'][0]) - 1
                    del cart['products'][item_id]
                    self.refresh_order_treeview()
                    messagebox.showinfo("THÔNG BÁO", "Đã xóa sản phẩm khỏi giỏ hàng.")

            # Buttons
            edit_button = tk.Button(edit_window, text='Chỉnh sửa', font=FONT3, command=handle_edit_cart_item)
            edit_button.pack(fill='x', padx=10, pady=5)
            delete_button = tk.Button(edit_window, text='Xóa', font=FONT3, command=handle_delete_cart_item)
            delete_button.pack(fill='x', padx=10, pady=5)

        else:
            messagebox.showinfo("THÔNG BÁO", "Giỏ hàng trống.")
    def refresh_customer_treeview(self):
        self.customer_treeview.delete(*self.customer_treeview.get_children())
        session = get_session()
        customers = session.query(Customer).all()
        for customer in customers:
            self.customer_treeview.insert('', tk.END, values=(customer.id, customer.name, customer.phone, customer.address))
        session.close()

    def refresh_order_treeview(self):
        self.order_treeview.delete(*self.order_treeview.get_children())
        global cart, new_order
        if cart['customer'] and not new_order:  # Hiển thị giỏ hàng nếu đang tạo đơn hàng mới
            for i, item in enumerate(cart['products']):
                product = item['product']  # Lấy product từ dictionary
                quantity = item['quantity']
                self.order_treeview.insert('', tk.END, values=(
                    i+1, # Hiển thị số thứ tự
                    cart['customer'].name,
                    f"{product.name} x {quantity}", # Hiển thị số lượng chính xác
                    product.price * quantity
                ))
        else: # Hiển thị danh sách đơn hàng từ database
            session = get_session()
            orders = session.query(Order).all()
            for order in orders:
                customer = session.query(Customer).filter_by(id=order.customer_id).first()
                # Lấy danh sách OrderItem liên quan đến order
                order_items = session.query(OrderItem).filter_by(order_id=order.id).all()
                product_names = [f"{item.product.name} x {item.quantity}" for item in order_items]
                self.order_treeview.insert('', tk.END, values=(
                    order.id,
                    customer.name if customer else 'N/A',
                    ', '.join(product_names),
                    order.total
                ))
            session.close()

            
    def refresh_order_history_treeview(self):
        self.order_history_treeview.delete(*self.order_history_treeview.get_children())
        session = get_session()
        orders = session.query(Order).all()
        for order in orders:
            customer = session.query(Customer).filter_by(id=order.customer_id).first()
            order_items = session.query(OrderItem).filter_by(order_id=order.id).all()
            product_names = [f"{item.product.name} x {item.quantity}" for item in order_items]
            self.order_history_treeview.insert('', tk.END, values=(
                order.id,
                customer.name if customer else 'N/A',
                ', '.join(product_names),
                order.total,
                order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ))
        session.close()

    def perform_data_analysis(self):
        session = get_session()
        orders = session.query(Order).all()
        order_items = session.query(OrderItem).all()

        # Lấy dữ liệu sản phẩm và khách hàng từ database
        products = session.query(Product).all()
        customers = session.query(Customer).all()
        session.close()


        #Tạo DataFrame từ df_customers
        df_customers = pd.DataFrame([(customer.id, customer.address) for customer in customers],
                                columns=['customer_id', 'address'])

                
       # Refresh dữ liệu lịch sử đơn hàng
        self.refresh_order_history_treeview()

        session = get_session()
        orders = session.query(Order).all()
        order_items = session.query(OrderItem).all()  # Lấy lại dữ liệu OrderItem sau khi refresh

        #Tạo DataFrame df_orders, df_order_items, df_products
        df_orders = pd.DataFrame([(order.id, order.customer_id, order.total, order.created_at) for order in orders],
                                columns=['order_id', 'customer_id', 'total', 'created_at'])

        df_order_items = pd.DataFrame([(item.id, item.order_id, item.product_id, item.quantity) for item in order_items],
            columns=['order_item_id', 'order_id', 'product_id', 'quantity'])

        df_products = pd.DataFrame([(product.id, product.name, product.price) for product in products], 
                                columns=['product_id', 'product_name', 'price'])


 
         # Tính toán daily_revenue và average_daily_order_value
        df_orders['created_at'] = pd.to_datetime(df_orders['created_at'])
        daily_revenue = df_orders.groupby(df_orders['created_at'].dt.date)['total'].sum()
        average_daily_order_value = df_orders.groupby(df_orders['created_at'].dt.date)['total'].mean()
        
        # Sản phẩm bán chạy nhất (theo số lượng bán)
        # Nối DataFrame df_order_items và df_products
        df_order_items = df_order_items.merge(df_products, on='product_id', how='left')

        # Tính toán sản phẩm bán chạy nhất dựa trên số lượng bán từ df_order_items
        product_sales = df_order_items.groupby('product_name')['quantity'].sum()
        best_selling_product_name = product_sales.idxmax()
        best_selling_product_id = df_products[df_products['product_name'] == best_selling_product_name]['product_id'].iloc[0]

  
        # Nối DataFrame df_orders và df_customers để lấy address
        df_orders = df_orders.merge(df_customers, on='customer_id', how='left')
               
        # Chuẩn bị dữ liệu cho biểu đồ tròn doanh thu theo address
        address_revenue = df_orders.groupby('address')['total'].sum()


        # Bố trí giao diện 3 cột
        self.analysis_results_textbox.config(state='normal')
        self.analysis_results_textbox.delete('1.0', tk.END)
        self.analysis_results_textbox.pack_forget()

                
        # Tạo frame chính, chia thành 3 cột bằng grid
        main_frame = tk.Frame(self.frames[3], bg='#001220')
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)


        # Phần 1: Bảng Doanh thu theo ngày
        revenue_frame = tk.LabelFrame(main_frame, text="Doanh thu theo ngày", font=FONT3, bg='#001220', fg='white')
        revenue_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        revenue_tree = ttk.Treeview(revenue_frame, columns=('Ngày', 'Doanh thu'), show='headings')
        revenue_tree.heading('Ngày', text='Ngày')
        revenue_tree.heading('Doanh thu', text='Doanh thu')
        for day, revenue in daily_revenue.items():
            revenue_tree.insert('', tk.END, values=(day, f"{revenue:.2f}"))
        revenue_tree.pack(fill=tk.BOTH, expand=True)

        # Phần 2: Thông tin khác
        info_frame = tk.LabelFrame(main_frame, text="Thông tin khác", font=FONT3, bg='#001220', fg='white')
        info_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        best_selling_label = tk.Label(info_frame, text=f"Sản phẩm bán chạy nhất: {best_selling_product_name} (ID: {best_selling_product_id})", 
                                     font=FONT3, bg='#001220', fg='white')
        best_selling_label.pack()

        avg_order_label = tk.Label(info_frame, text="Giá trị đơn hàng trung bình theo ngày:", font=FONT3, bg='#001220', fg='white')
        avg_order_label.pack()

        for day, avg_value in average_daily_order_value.items():
            avg_order_label.config(text=avg_order_label.cget("text") + f"\n{day}: {avg_value:.2f}")


        # Phần 3: Biểu đồ 
        chart_frame = tk.LabelFrame(main_frame, text="Biểu đồ", font=FONT3, bg='#001220', fg='white')
        chart_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)

        # Biểu đồ Top 5 sản phẩm bán chạy nhất (bar chart)
        top_5_products = df_order_items.groupby('product_name')['quantity'].sum().nlargest(5)
        top_5_product_names = top_5_products.index  # Lấy tên sản phẩm từ index

        if top_5_product_names.shape[0] == 0:
            print("Không có sản phẩm nào để hiển thị trên biểu đồ.")
        else:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(top_5_product_names, top_5_products)
            ax.set_title('Top 5 sản phẩm bán chạy nhất')
            ax.set_ylabel('Số lượng bán')

            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Biểu đồ tròn doanh thu theo address
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.pie(address_revenue.values, labels=address_revenue.index, autopct='%1.1f%%')
        ax2.set_title('Doanh thu theo địa điểm')

        canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)



    def display_bill(self, order):
        self.bill_textbox.config(state='normal')
        self.bill_textbox.delete('1.0', tk.END)

        if order:  # Hiển thị bill cho đơn hàng đã tạo
            session = get_session()
            customer = session.query(Customer).filter_by(id=order.customer_id).first()
            if customer:
                self.bill_textbox.insert(tk.END, f"Tên khách hàng: {customer.name}\n")
            else:
                self.bill_textbox.insert(tk.END, "Không có thông tin khách hàng\n")
            total = 0

            # Lấy danh sách OrderItem liên quan đến order
            order_items = session.query(OrderItem).filter_by(order_id=order.id).all()
            for item in order_items:
                product_total = item.quantity * item.product.price
                self.bill_textbox.insert(tk.END, f"{item.product.name} x {item.quantity} = {product_total}\n")
                total += product_total
            self.bill_textbox.insert(tk.END, f"Tổng giá trị đơn hàng: {total}")
            session.close()

        self.bill_textbox.config(state='disabled')

    def calculate_total_value(self):
        global cart
        return sum([item['product'].price * item['quantity'] for item in cart['products']])

    def update_order_summary(self):
        global cart
        if cart['customer']:
            self.order_summary_label.config(text=f"Khách hàng: {cart['customer'].name} - Số lượng sản phẩm: {len(cart['products'])}")
        else:
            self.order_summary_label.config(text="")

if __name__ == '__main__':
    app = App()
    app.mainloop()