#Ứng Dụng Quản Lý Cửa Hàng

## Giới thiệu
Đây là tài liệu hướng dẫn và mô tả về "Ứng Dụng Quản Lý Cửa Hàng". Ứng dụng này được xây dựng bằng Python và Tkinter và được phát triển nhằm mục đích quản lý sản phẩm, khách hàng và đơn hàng trong một cửa hàng. Dưới đây là các phần cụ thể về chức năng, cài đặt và hướng dẫn sử dụng.

## Chức năng
Ứng dụng này cung cấp các chức năng quản lý cơ bản như sau:
- Quản lý tài khoản nhân viên với tính năng đăng nhập và đăng ký an toàn.
- Quản lý sản phẩm: Thêm, sửa, xóa sản phẩm trong database, thêm sản phẩm vào giỏ hàng.
- Quản lý khách hàng: Thêm, sửa, xóa khách hàng trong database, chọn khách hàng cho đơn hàng hiện tại
- Quản lý đơn hàng: Tạo đơn hàng mới, xem đơn hàng hiện có, lịch sử đơn hàng.
- Phân tích dữ liệu: Phân tích doanh thu hàng ngày, sản phẩm bán chạy nhất, hiển thị dữ liệu trực quan bằng biểu đồ.

## Cài đặt
1. Đảm bảo đã cài đặt Python 3.x và thư viện SQLite3  trên máy tính.
2. Cài đặt các thư viện cần thiết bằng lệnh sau:
    ```
    pip install customtkinter tkinter ttk pandas matplotlib bcrypt sqlalchemy
    ```
3. Tạo một tệp cơ sở dữ liệu SQLite có tên `supermarket.db` trong cùng thư mục với các tệp Python.
4. Chạy tệp `main.py` để khởi động ứng dụng.

##Cấu trúc thư mục
Management-App-Store/
--- main.py             # File chính của ứng dụng
--- database.py         # Kết nối cơ sở dữ liệu và định nghĩa các model
--- README.md           # Hướng dẫn sử dụng và mô tả dự án

## Sử dụng
1. Đăng nhập hoặc đăng ký tài khoản mới.
2. Sử dụng các tab để quản lý sản phẩm, khách hàng và đơn hàng.

## Ghi chú
- Hãy chắc chắn rằng các thư viện được cài đặt đúng cách và cơ sở dữ liệu được tạo trước khi chạy ứng dụng.
- Để xem mã nguồn và chi tiết triển khai, vui lòng tham khảo các tệp Python trong ứng dụng.
- Ứng dụng này được phát triển với mục đích học tập và thử nghiệm, còn nhiều chức năng và hoạt động chưa được hoàn chỉnh và đầy đủ. Nếu muốn sử dụng trong môi trường thực tế thì cần cải tiến, sửa đổi và kiểm tra kỹ lưỡng hơn.

