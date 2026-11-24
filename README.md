 # Data3D – Add-on Blender vẽ biểu đồ 3D từ file CSV

Data3D là tiện ích mở rộng (add-on) cho phần mềm đồ họa 3D mã nguồn mở Blender, viết bằng Python. Chọn một file CSV, bấm một nút, add-on tự động dựng biểu đồ cột hoặc biểu đồ đường 3D ngay trong khung nhìn của Blender, không cần viết code.

* Dự án thuộc bài tập lớn môn Công nghệ mã nguồn mở. 
* Sinh viên: Trần Quỳnh Trang – MSSV 2551050225 – Lớp DH25IT03. 

## Mục lục 
1 Tính năng
2 Yêu cầu
3 Cài đặt
4 Cách sử dụng
5 Định dạng file CSV
6 Cấu trúc mã nguồn
7 Cách hoạt động
8 Hạn chế đã biết
9 Hướng phát triển
10 Đóng góp
11 Giấy phép


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