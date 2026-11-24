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
6. [Cấu trúc dự án](#cấu-trúc-dự-án)
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




## Cách sử dụng

### Bước 1: Mở bảng Data3D

1. Mở Blender, đưa chuột vào **khung 3D**.

2. Nhấn phím **N** để mở thanh bên.

3. Bấm vào tab **Data3D**.

### Bước 2: Chọn dữ liệu

1. Ở mục **Dữ liệu**, bấm biểu tượng thư mục cạnh ô **File CSV**.

2. Chọn file dữ liệu của bạn, hoặc dùng file mẫu `sample_data/sample_chart.csv`.

3. Chọn **Loại** biểu đồ: **Cột** hoặc **Đường**.

### Bước 3: Tùy chỉnh (không bắt buộc)

| Mục | Tùy chọn | Tác dụng |
|---|---|---|
| **Kích thước** | Khoảng cách | Khoảng cách giữa các cột hoặc điểm |
| | Độ rộng | Độ rộng cột (hoặc kích thước điểm) |
| | Tỉ lệ chiều cao | Nhân chiều cao với một hệ số |
| **Nhãn** | Hiện nhãn | Bật/tắt tên và giá trị trên biểu đồ |
| | Font | Chọn file font để hiện đúng tiếng Việt hoặc emoji |
| **Hoạt họa** | Hoạt họa | Cột mọc lên lần lượt |
| | Số khung mỗi cột | Thời gian một cột mọc lên |
| | Trễ giữa các cột | Khoảng chờ giữa hai cột liên tiếp |

### Bước 4: Tạo biểu đồ

1. Bấm nút **Tạo biểu đồ**.

2. Biểu đồ xuất hiện trong khung 3D. Nếu chưa thấy rõ, đưa chuột vào khung 3D và nhấn phím **Home** để xem toàn cảnh.

3. Nếu cột vẫn màu xám, nhấn phím **Z** trong khung 3D rồi chọn **Material Preview**.

4. Muốn đổi dữ liệu hoặc cài đặt, chỉnh lại rồi bấm **Tạo biểu đồ** lần nữa. Biểu đồ cũ sẽ được thay thế.

### Bước 5: Xem hoạt họa (nếu đã bật)

1. Nhấn **Space** trong khung 3D để phát hoạt họa.

2. Nhấn **Space** lần nữa để dừng.

### Bước 6: Xuất ảnh

1. **Lưu file .blend trước** (**File > Save**), hoặc nhập đường dẫn đầy đủ vào ô **Ảnh xuất**, ví dụ `C:\Users\ten\Desktop\chart.png`.

2. Bấm nút **Xuất ảnh**.

3. Add-on tự đặt camera nhìn vào biểu đồ và lưu ảnh PNG.

> Nút **Xuất ảnh** sẽ di chuyển camera của cảnh. Nếu bạn đã đặt camera riêng, hãy lưu lại trước khi bấm.

### Xóa biểu đồ

Bấm **Xóa biểu đồ** để dọn sạch biểu đồ do Data3D tạo ra. Camera, đèn và các đối tượng khác không bị ảnh hưởng.

### Xử lý lỗi thường gặp

| Thông báo hoặc hiện tượng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Chưa chọn file CSV | Ô File CSV đang trống | Chọn file CSV |
| File CSV cần có cột `name` và `value` | Dòng tiêu đề sai | Sửa dòng đầu thành `name,value` |
| `'...'` không phải là số | Cột `value` có chữ | Chỉ để số, dùng dấu chấm cho số thập phân |
| File không phải UTF-8 | Lưu sai mã hóa | Lưu lại file CSV với mã hóa UTF-8 |
| Hiện chưa hỗ trợ giá trị âm | Có số âm trong dữ liệu | Bỏ hoặc đổi các giá trị âm |
| Hãy lưu file .blend trước | Xuất ảnh với đường dẫn `//` khi chưa lưu | Lưu file .blend hoặc nhập đường dẫn đầy đủ |
| Chữ hiện thành ô vuông | Font mặc định thiếu ký tự | Chọn font ở ô **Font** (ví dụ Noto Sans) |





## Định dạng file CSV

### Cấu trúc cơ bản

Dòng đầu tiên là **tiêu đề**, các dòng sau là dữ liệu. Mỗi dòng dữ liệu tương ứng với một cột (hoặc một điểm) trên biểu đồ.

```
name,value,emoji
Hà Nội,5,
TP.HCM,8,
Đà Nẵng,3,
Cần Thơ,4,
Huế,6,
```

### Các cột

| Cột | Bắt buộc | Ý nghĩa | Ví dụ |
|---|---|---|---|
| `name` | Có | Tên hiển thị của cột hoặc điểm | `Hà Nội` |
| `value` | Có | Giá trị số, quyết định chiều cao và màu | `5`, `3.5` |
| `emoji` | Không | Biểu tượng đi kèm giá trị | `🏙️` |

- Tên cột **không phân biệt chữ hoa, chữ thường** và được bỏ khoảng trắng thừa (`Name`, ` VALUE ` vẫn đọc được).
- Các cột khác ngoài ba cột trên sẽ bị bỏ qua.
- Thứ tự cột không quan trọng, miễn có `name` và `value`.

### Quy tắc dữ liệu

| Quy tắc | Chi tiết |
|---|---|
| Mã hóa | Lưu bằng **UTF-8** để tiếng Việt có dấu hiển thị đúng |
| Dấu phân cách | Dấu phẩy `,` hoặc dấu chấm phẩy `;` (tự nhận biết theo dòng tiêu đề) |
| Số thập phân | Nên dùng dấu chấm: `3.5`. Nếu file dùng `;` làm dấu phân cách thì có thể dùng dấu phẩy `3,5` |
| Giá trị âm | **Chưa hỗ trợ**, add-on sẽ báo lỗi |
| Dòng trống | Được bỏ qua |
| Thiếu tên | Add-on tự đặt tên theo số thứ tự (`Muc 1`, `Muc 2`...) |
| Số dòng | Nên dưới **50 dòng**, quá nhiều thì biểu đồ rất dài và add-on sẽ cảnh báo |

### Ví dụ đúng

Dùng dấu phẩy:

```
name,value
Hà Nội,5
TP.HCM,8.5
Đà Nẵng,3
```

Dùng dấu chấm phẩy (kiểu Excel tiếng Việt):

```
name;value
Hà Nội;5
TP.HCM;8,5
Đà Nẵng;3
```

### Ví dụ sai

| File | Lỗi | Kết quả |
|---|---|---|
| `ten,gia_tri` | Sai tên cột tiêu đề | Báo thiếu cột `name` và `value` |
| `Hà Nội,năm` | Giá trị là chữ | Báo dòng đó không phải số |
| `Hà Nội,-5` | Giá trị âm | Báo chưa hỗ trợ giá trị âm |
| File lưu mã hóa ANSI | Sai mã hóa | Báo file không phải UTF-8 |

### Cách lưu file CSV bằng UTF-8

**Notepad:**

1. Chọn **File > Save As**.

2. Ở ô **Encoding** phía dưới, chọn **UTF-8**.

3. Đặt tên có đuôi `.csv` và chọn **Save as type: All files**.

**Excel:**

1. Chọn **File > Save As**.

2. Ở ô loại file, chọn **CSV UTF-8 (Comma delimited)**.

### Về emoji và tiếng Việt

Font mặc định của Blender có thể không hiển thị emoji hoặc một số chữ có dấu. Khi gặp ô vuông, hãy chọn một font mã nguồn mở phù hợp (ví dụ Noto Sans, Noto Emoji) ở ô **Font** trong panel Data3D. Một ô Font chỉ nhận một font, nên nếu cần chữ Việt đúng thì ưu tiên Noto Sans và để trống cột `emoji`. Hãy kiểm tra giấy phép của font trước khi dùng.

### Nguồn dữ liệu mở

Bạn có thể lấy dữ liệu thật từ [World Bank Open Data](https://data.worldbank.org/) hoặc [Our World in Data](https://ourworldindata.org/), rút gọn còn vài chục dòng và đổi tên cột thành `name`, `value`. 




## Cấu trúc dự án


### Sơ đồ thư mục

```
Data3D-Blender/
├── .gitignore              # Danh sách file Git bỏ qua (*.blend1, *.blend2...)
├── LICENSE                 # Giấy phép GNU GPL v3.0
├── README.md               # Tài liệu giới thiệu và hướng dẫn
├── data3d_addon/           # Mã nguồn chính của add-on
│   ├── __init__.py         # Thông tin add-on, đăng ký / hủy đăng ký các module
│   ├── properties.py       # Các thuộc tính người dùng chỉnh
│   ├── operators.py        # Logic xử lý: đọc CSV, dựng biểu đồ, xuất ảnh
│   └── panels.py           # Giao diện bảng Data3D
├── sample_data/            # Dữ liệu mẫu để chạy thử
│   └── sample_chart.csv
└── docs/                   # Ảnh minh họa cho README (tạo khi cần)
```

### Vai trò từng file

| File | Vai trò | Nội dung chính |
|---|---|---|
| `__init__.py` | **Đăng ký** add-on với Blender | `bl_info` (tên, tác giả, phiên bản), hàm `register()` và `unregister()` |
| `properties.py` | **Lưu** lựa chọn của người dùng | Đường dẫn CSV, loại biểu đồ, kích thước, nhãn, font, hoạt họa, đường dẫn ảnh xuất |
| `operators.py` | **Xử lý** khi người dùng bấm nút | Đọc CSV, dựng biểu đồ, tạo màu, nhãn, hoạt họa, xuất ảnh |
| `panels.py` | **Hiển thị** giao diện | Bảng Data3D ở thanh bên (phím N) với các ô nhập và nút bấm |
| `sample_chart.csv` | Dữ liệu mẫu | 5 thành phố với giá trị minh họa |

### Các thành phần trong `operators.py`

| Nhóm | Tên | Chức năng |
|---|---|---|
| **Operator** (nút bấm) | `DATA3D_OT_create` | Đọc CSV và dựng biểu đồ |
| | `DATA3D_OT_clear` | Xóa biểu đồ cũ |
| | `DATA3D_OT_render` | Đặt camera và xuất ảnh PNG |
| **Đọc dữ liệu** | `read_csv` | Đọc và kiểm tra file CSV, trả về dữ liệu hoặc thông báo lỗi |
| **Dựng biểu đồ** | `build_bar_chart` | Dựng biểu đồ cột |
| | `build_line_chart` | Dựng biểu đồ đường |
| **Hình thức** | `gradient` | Đổi giá trị thành màu |
| | `make_material` | Tạo vật liệu có màu |
| | `add_label` | Tạo chữ 3D |
| | `load_font` | Nạp font người dùng chọn |
| **Hoạt họa** | `key_bar_grow`, `key_rise`, `key_pop` | Chèn keyframe cho cột, nhãn, điểm |
| **Quản lý cảnh** | `get_collection`, `clear_chart`, `move_to_col` | Quản lý Collection `Data3D` |
| | `frame_view` | Zoom khung 3D và bật chế độ xem màu |

### Mối quan hệ giữa các file

```
__init__.py ──đăng ký──> properties.py   (lưu lựa chọn)
            ──đăng ký──> operators.py    (xử lý khi bấm nút)
            ──đăng ký──> panels.py       (vẽ giao diện)

panels.py ──hiển thị ô nhập──> properties.py
          ──gắn nút bấm──────> operators.py
```

Cách tách file này theo hướng **tách giao diện, dữ liệu và xử lý** (gần với mô hình MVC) để mỗi file một nhiệm vụ, dễ đọc, dễ sửa và dễ mở rộng. Ví dụ thêm một loại biểu đồ mới chỉ cần thêm hàm dựng trong `operators.py`, một lựa chọn trong `properties.py` và không phải sửa gì ở phần còn lại của giao diện.




## Cách hoạt động

### Luồng xử lý tổng quát

```
Người dùng bấm "Tạo biểu đồ"
        │
        ▼
1. Kiểm tra đầu vào (đã chọn file chưa?)
        │
        ▼
2. Đọc và kiểm tra file CSV (read_csv)
        │
        ▼
3. Kiểm tra dữ liệu (giá trị âm, số dòng quá nhiều)
        │
        ▼
4. Chuẩn bị cảnh: xóa biểu đồ cũ, tạo Collection "Data3D", nạp font
        │
        ▼
5. Dựng biểu đồ theo loại đã chọn
   ├── Cột   -> build_bar_chart
   └── Đường -> build_line_chart
        │
        ▼
6. Thiết lập hoạt họa (nếu bật)
        │
        ▼
7. Zoom khung 3D và chuyển sang chế độ xem màu
```

### Bước 1: Đọc và kiểm tra CSV (`read_csv`)

| Việc làm | Chi tiết |
|---|---|
| Mở file | Đọc bằng mã hóa UTF-8, báo lỗi nếu không mở được hoặc sai mã hóa |
| Nhận dấu phân cách | Dòng tiêu đề có nhiều `;` hơn `,` thì dùng `;`, ngược lại dùng `,` |
| Chuẩn hóa tiêu đề | Bỏ khoảng trắng, viết thường, kiểm tra có đủ cột `name` và `value` |
| Đọc từng dòng | Bỏ dòng trống, đổi dấu phẩy thập phân thành dấu chấm, chuyển `value` thành số |
| Báo lỗi cụ thể | Chỉ rõ **dòng số mấy** có giá trị không phải số |

Kết quả trả về là danh sách các bộ `(tên, giá trị, emoji)` hoặc một thông báo lỗi.

### Bước 2: Chuẩn bị cảnh

- Chuyển Blender về **Object Mode** nếu đang ở chế độ khác.
- `clear_chart` xóa các đối tượng cũ **chỉ trong Collection `Data3D`**, đồng thời dọn mesh, curve và vật liệu `D3D_*` không còn dùng. Camera, đèn và đối tượng khác của người dùng **không bị ảnh hưởng**.
- `get_collection` tạo Collection `Data3D` nếu chưa có.

### Bước 3: Dựng biểu đồ cột (`build_bar_chart`)

Với mỗi dòng dữ liệu thứ `i` có giá trị `value`:

| Thành phần | Cách tính |
|---|---|
| Chiều cao | `h = value × tỉ lệ chiều cao` (tối thiểu 0.01 để cột không bị biến mất) |
| Vị trí ngang | `x = i × khoảng cách` |
| Khối cột | Khối lập phương cạnh 1 đặt tại `(x, 0, h/2)`, kéo giãn thành `(độ rộng, độ rộng, h)` để đáy cột nằm đúng mặt phẳng |
| Màu | Chuẩn hóa `t = (value − min) / (max − min)` rồi đổi qua `gradient(t)` |
| Nhãn tên | Chữ 3D dưới chân cột, tại `(x, −độ rộng, −0.8)` |
| Nhãn giá trị | Chữ 3D (kèm emoji) trên đỉnh cột, tại `(x, 0, h + 0.3)` |

### Bước 4: Dựng biểu đồ đường (`build_line_chart`)

| Thành phần | Cách làm |
|---|---|
| Điểm | Quả cầu nhỏ tại `(i × khoảng cách, 0, value × tỉ lệ)` |
| Đoạn nối | Khối trụ giữa hai điểm liền kề, quay theo hướng từ điểm này sang điểm kia |
| Màu | Điểm theo giá trị của nó, đoạn nối theo trung bình hai điểm đầu mút |
| Nhãn | Giống biểu đồ cột |

### Cách tô màu (`gradient`)

Giá trị `t` từ 0 đến 1 được đổi thành màu RGB:

| Khoảng `t` | Màu |
|---|---|
| 0 | Xanh dương |
| 0.5 | Xanh lá |
| 1 | Đỏ |

Giữa các mốc, màu được nội suy tuyến tính. Nếu mọi giá trị bằng nhau thì dùng `t = 0.5` (xanh lá) để tránh chia cho 0.

### Hoạt họa

Add-on dùng **keyframe** của Blender:

- Cột `i` bắt đầu ở khung `1 + i × độ trễ`, kết thúc sau `số khung mỗi cột`.
- **Cột:** chiều cao đi từ gần 0 đến giá trị thật. Vì tâm khối nằm ở giữa nên vị trí `z` cũng được chèn keyframe để cột mọc từ đáy lên.
- **Nhãn giá trị:** trượt từ dưới lên vị trí cuối.
- **Biểu đồ đường:** điểm, nhãn và đoạn nối phóng to dần từ gần 0.
- Khung cuối của cảnh được đặt bằng khung hoạt họa cuối cùng cộng thêm 15 khung.

### Xuất ảnh (`DATA3D_OT_render`)

1. Kiểm tra đã có biểu đồ và đường dẫn hợp lệ.
2. Nếu cảnh chưa có camera hoặc đèn thì tạo thêm (camera mới và đèn Sun).
3. Tính **khung bao** quanh toàn bộ đối tượng trong Collection `Data3D`.
4. Tính khoảng cách camera từ khung bao, góc nhìn của ống kính và tỉ lệ ảnh, nhân thêm hệ số 1.3 làm lề an toàn.
5. Đặt camera trước biểu đồ, nhìn thẳng vào.
6. Render và lưu ảnh PNG.

### Cách các file phối hợp

| Thời điểm | File | Việc xảy ra |
|---|---|---|
| Bật add-on | `__init__.py` | Gọi `register()` của `properties.py`, `operators.py`, `panels.py` theo thứ tự |
| Mở thanh bên | `panels.py` | Hàm `draw` vẽ các ô nhập và nút bấm |
| Chỉnh ô nhập | `properties.py` | Giá trị được lưu vào Scene (lưu cùng file `.blend`) |
| Bấm nút | `operators.py` | Hàm `execute` đọc các giá trị đã lưu và chạy luồng xử lý ở trên |
| Tắt add-on | `__init__.py` | Gọi `unregister()` theo thứ tự ngược lại |