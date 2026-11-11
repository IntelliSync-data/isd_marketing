# Theme The IELTS Workshop (TIW) for Odoo 18 & 19

Module giao diện website hiện đại cho **Odoo 18.0 & 19.0 Community & Enterprise**, được chuyển thể 1:1 từ hệ thống website của The IELTS Workshop.

---

## 🌟 Tính Năng Nổi Bật

1. **Bộ Building Blocks (Snippets) kéo thả trực quan** trong Odoo Website Builder:
   - **TIW Hero Banner**: Banner trắc nghiệm & kiểm tra trình độ với nút Call-to-action.
   - **TIW Why Choose Us**: 4 giá trị cốt lõi, phương pháp L.I.M và ảnh Founder Đặng Trần Tùng.
   - **TIW Courses Roadmap**: Lộ trình 4 cấp độ từ Freshman (0-2.5) đến Master (7.5+).
   - **TIW Teachers 9.0**: Grid đội ngũ giáo viên 8.5 - 9.0 IELTS có chứng chỉ quốc tế CELTA.
   - **TIW Mini Test Widget**: Trắc nghiệm 4 kỹ năng tương tác trực tiếp với JavaScript chấm điểm và ước lượng band điểm tự động.
   - **TIW Lead Form**: Form đăng ký thông tin khách hàng, kết nối trực tiếp vào Odoo CRM (`crm.lead`).
2. **Bộ tiện ích nổi (Floating Widgets)**: Hotline 1900 0353, Test Free 4 kỹ năng & Scroll To Top tự động ẩn hiện.
3. **Menu & Trang tạo sẵn**:
   - Trang chủ (`/`)
   - Lịch khai giảng (`/schedule`)
   - Đội ngũ giảng viên (`/ielts-trainers`)
   - Liên hệ & 18 cơ sở (`/contact`)

---

## 🚀 Hướng Dẫn Cài Đặt Trên Odoo 18 & 19

### Bước 1: Sao chép thư mục module vào thư mục `addons` của Odoo
Copy thư mục `theme_theieltsworkshop` vào đường dẫn `addons` hoặc `custom_addons` của Odoo server.

Ví dụ:
```bash
cp -r theme_theieltsworkshop /path/to/odoo/custom_addons/
```

### Bước 2: Khởi động lại Odoo Server
```bash
# Nếu chạy bằng Systemd:
sudo systemctl restart odoo

# Nếu chạy bằng Docker Compose:
docker compose restart web
```

### Bước 3: Kích hoạt Developer Mode & Cập nhật danh sách ứng dụng
1. Đăng nhập vào Odoo bằng tài khoản **Admin**.
2. Vào **Settings (Cài đặt)** -> Kéo xuống cuối trang bấm **Activate the developer mode (Kích hoạt chế độ nhà phát triển)**.
3. Vào menu **Apps (Ứng dụng)** -> Bấm **Update Apps List (Cập nhật danh sách ứng dụng)** trên thanh công cụ.

### Bước 4: Cài đặt và Áp dụng Theme
1. Trong ô tìm kiếm của menu **Apps**, gõ: `Theme The IELTS Workshop`.
2. Bấm **Activate (Cài đặt)**.
3. Sau khi cài đặt hoàn tất, vào trang **Website** -> Bấm **Edit (Chỉnh sửa)** để bắt đầu tùy biến và kéo thả các snippet theo ý muốn!

