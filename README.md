 # Data3D – Add-on Blender vẽ biểu đồ 3D từ file CSV

Data3D là tiện ích mở rộng (add-on) cho phần mềm đồ họa 3D mã nguồn mở Blender, viết bằng Python. Chọn một file CSV, bấm một nút, add-on tự động dựng biểu đồ cột hoặc biểu đồ đường 3D ngay trong khung nhìn của Blender, không cần viết code.

* Dự án thuộc bài tập lớn môn Công nghệ mã nguồn mở. 
* Sinh viên: Trần Quỳnh Trang – MSSV 2551050225 – Lớp DH25IT03. 

## Mục lục

1. [Tính năng](#tính-năng)
2. [Yêu cầu](#yêu-cầu)
3. [Cài đặt](#cài-đặt)
4. [Cách sử dụng](#cách-sử-dụng)
5. [Định dạng file CSV](#định-dạng-file-csv)
6. [Cấu trúc mã nguồn](#cấu-trúc-mã-nguồn)
7. [Cách hoạt động](#cách-hoạt-động)
8. [Hạn chế đã biết](#hạn-chế-đã-biết)
9. [Hướng phát triển](#hướng-phát-triển)
10. [Đóng góp](#đóng-góp)
11. [Giấy phép](#giấy-phép)


## Tính năng

| Nhóm | Tính năng | Mô tả |
|---|---|---|
| **Dữ liệu** | Đọc file CSV | Hỗ trợ tiếng Việt có dấu (UTF-8) |
| | Tự nhận dấu phân cách | Dùng được cả `,` lẫn `;` (file xuất từ Excel tiếng Việt) |
| **Biểu đồ** | Biểu đồ cột 3D | Mỗi dòng dữ liệu là một cột, chiều cao theo giá trị |
| | Biểu đồ đường 3D | Mỗi dòng là một điểm, các điểm nối bằng đoạn thẳng |
| **Hiển thị** | Tô màu theo giá trị | Thấp xanh dương, trung bình xanh lá, cao đỏ |
| | Nhãn chữ 3D | Tên ở chân cột, giá trị (kèm emoji) ở đỉnh cột |
| | Tùy chỉnh kích thước | Khoảng cách, độ rộng, tỉ lệ chiều cao |
| | Chọn font | Hiện đúng tiếng Việt hoặc emoji |
| **Hoạt họa** | Cột mọc lên lần lượt | Chỉnh được thời lượng và độ trễ |
| **Xuất ảnh** | Render PNG | Camera tự căn theo biểu đồ |
| **Tiện ích** | Báo lỗi dễ hiểu | Sai file, thiếu cột, giá trị không phải số, giá trị âm |
| | Quản lý theo Collection | Tạo lại chỉ xóa biểu đồ cũ, không đụng camera và đèn |
| | Giao diện bằng chuột | Thanh bên Blender (phím N), không cần viết code |


## Yêu cầu 

* Blender (phát triển và thử trên bản 5.3.0). Khai báo tối thiểu trong bl_info là 4.2.
* Không cần cài thêm thư viện Python, add-on chỉ dùng bpy và thư viện chuẩn có sẵn trong Blender.


## Cài đặt

### Bước 1: Tải mã nguồn

Chọn một trong hai cách:

- **Tải file nén:** vào trang repo trên GitHub, bấm **Code > Download ZIP**, rồi giải nén.
- **Dùng Git:**

  ```
  git clone https://github.com/tranquynhtrang1502hk-cell/Data3D-Blender.git
  ```

### Bước 2: Nén add-on thành file zip

1. Mở thư mục repo vừa tải.

2. Chuột phải vào thư mục **`data3d_addon`**, chọn **Compress to ZIP file**.

3. Bạn được file `data3d_addon.zip`.

> Phải nén **cả thư mục `data3d_addon`**, không nén riêng các file bên trong, nếu không Blender sẽ không nhận.

### Bước 3: Cài vào Blender

1. Mở Blender, vào **Edit > Preferences > Add-ons**.

2. Chọn lệnh cài từ file (**Install from Disk**) rồi chọn `data3d_addon.zip`.

3. Tìm **Data3D** trong danh sách và tick bật.

4. Trong khung 3D nhấn phím **N**, tab **Data3D** sẽ hiện ở thanh bên.

> Giao diện cài add-on có thể khác nhau giữa các bản Blender. Nếu không thấy mục *Install from Disk*, xem hướng dẫn mới nhất tại [docs.blender.org](https://docs.blender.org/).

### Cách khác: Liên kết thư mục (dành cho người phát triển, Windows)

Cách này giúp Blender đọc thẳng code trong repo, sửa code xong chỉ cần khởi động lại Blender.

1. Mở **Command Prompt (cmd)**.

2. Chạy lệnh sau (sửa đường dẫn cuối cho đúng máy của bạn):

   ```
   mklink /J "%APPDATA%\Blender Foundation\Blender\5.3\scripts\addons\data3d_addon" "D:\duong\dan\toi\Data3D-Blender\data3d_addon"
   ```

3. Khởi động lại Blender, vào **Edit > Preferences > Add-ons** và bật **Data3D**.

### Gỡ cài đặt

Vào **Edit > Preferences > Add-ons**, tìm **Data3D** rồi tắt hoặc gỡ bỏ.