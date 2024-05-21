# Manager-Strore-Order
# Giao diện dùng Tkinter
Các kiến thức cần lưu ý:
1. Thư viện custom tkinter/tkinter
   Thư viện dùng các hàm như CTkEntry, CTkLabel... thay vì Entry, Label,... như tkinter
   hàm place thay cho pack: Đặt vị trí cho ô mình thiết lập
3. Các tham số thiết lập
   font: font chữ
   bg_color(customtkinter, tkinter dùng bg): màu nền
   fg_color(tương tự như trên): màu chữ
   màu hexa: '#nnnnnn' (n là số hexa): mỗi mã sẽ tương ứng với dải màu khác nhau, có thể tra trên https://www.color-hex.com/
   border_color: màu viền, border_width: độ rộng viền
   placeholder_text: văn bản, placeholder_text_color: màu văn bản
   corner_radius: bán kính góc
   width: độ rộng, height: độ cao
   cursor='hand2':thiết lập con trỏ tại ô khi nhấp vào sẽ chuyển thành hình bàn tay
   command=hàm gọi: lệnh để thực hiện hàm đích(có thể là CTkButton như trong code)
   padx: khoảng cách giữa hộp này với hộp khác bên cạnh nó, pady: tương tự nhưng là trên/dưới
   fill=X: hộp mở rộng theo hướng ngang (Y: hướng dọc)
4. Thư viện csdl sqlite3
   Các câu lệnh:
   conn = sqlite3.connect('data.db'):Kết nối đến csdl tên 'data.db'
   # Tổ hợp 2 lệnh dưới là tạo 1 bảng có tên 'users' nếu nó chưa tồn tại, với 2 cột là 'username' và 'password'
cursor = conn.cursor() 
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL,password TEXT NOT NULL)''')
# Thao tác với csdl: chọn 1 username từ cột username
 cursor.execute('SELECT username FROM users WHERE username=?',[username])
 cursor.fetchone(): trả về 1 nếu có username, 0 khi không có
 # Lưu mật khẩu và tài khoản mới vào csdl
 cursor.execute('INSERT INTO users VALUES (?, ?)',[username,hashed_password])
 conn.commit(): Lưu các thay đổi vào csdl
 4. Thư viện messagebox
 Các hàm showinfo: Hiện thông báo, showerror: Hiện thông báo lỗi
 5. Thư viện mã hóa mật khẩu bcrypt
 Các hàm:
   password.encode('utf-8'): Định dạng biến đó là utf8
    # bcrypt.gensalt() Tạo là salt - là chuỗi giả ngẫu nhiên được thêm vào password
 # bcrypt.hashpw() Dùng để tạo hàm băm cuối cùng được lưu trữ trong csdl
 hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
 6. Thư viện matplotlib: Vẽ biểu đồ 2D, 3D
 7. FigureCanvasTkAgg: CHuyển biểu đồ thành đối tượng có thể hiển thị trong giao diện tkinter
 ######
 Cần cài thêm các thư viện customtkinter, sqlite3, bcrypt, matplotlib để chạy được code giao diện
 Sử dụng lệnh py -3 -m pip install <tên gói thư viện> trong cửa sổ cmd
 Điều kiện: Cài python idle mới có được trình compile của python
