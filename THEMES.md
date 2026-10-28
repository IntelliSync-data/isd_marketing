# Làm website theme cho Odoo 18

Mẫu tham chiếu: [`theme_usa_program/`](theme_usa_program/). Làm theme mới thì copy nó, đổi tên, thay nội dung.

Trước khi push, luôn chạy:

```bash
python tools/theme_tool.py theme_ten_moi --homepage
```

`python` ở đây phải là python của venv Odoo vì cần `lxml` và `libsass` — trên máy dev là `PJ_Workplace/odoo18-venv/bin/python`. Ra `OK` mới push. Tool bắt đúng những lỗi đã từng làm hỏng theme ở đây; chạy nó trên bản gốc lỗi của `theme_usa_program` ra 20 lỗi.

---

## 1. Hai điều kiện bắt buộc

Thiếu một trong hai thì **không phải theme**, chỉ là module thường.

| | Vì sao |
|---|---|
| Tên module bắt đầu bằng **`theme_`** | `odoo/tools/convert.py` chỉ biến `<template>` thành `theme.ir.ui.view` (bản mẫu, chép vào website nào chọn theme) khi tên có tiền tố này. Không có thì template áp lên **mọi website** cùng lúc. |
| `category` là **`Theme`** hoặc **`Theme/...`** | `get_themes_domain()` lọc theo category. Không có thì theme không hiện trong trình chọn, không đổi được, và CSS/JS chạy trên **mọi website**. |

Tên `theme_` lệch quy ước `isd_` của công ty — chấp nhận, vì ở đây nó là điều kiện kỹ thuật chứ không phải cách đặt tên.

---

## 2. Cấu trúc

```text
theme_ten_moi/
├── __init__.py                       # để trống
├── __manifest__.py
├── static/
│   ├── description/icon.png
│   └── src/
│       ├── scss/
│       │   ├── css_variables.scss    # :root { --ten-mau: ... }
│       │   └── theme_ten_moi.scss
│       └── js/theme_ten_moi.js
└── views/
    ├── snippets/
    │   ├── s_ten_khoi_1.xml          # mỗi khối một file, tên bắt đầu s_
    │   ├── s_ten_khoi_2.xml
    │   └── snippets.xml              # đăng ký khối vào panel Builder
    └── pages/
        └── homepage.xml              # sinh bằng tool, không viết tay
```

---

## 3. `__manifest__.py`

```python
{
    'name': 'Tên Theme',
    'summary': '...',
    'category': 'Theme/Education',        # bắt buộc Theme/...
    'version': '18.0.1.0.0',
    'author': 'IntelliSyncData',
    'website': 'https://intellisyncdata.com',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': [
        # Thứ tự các s_*.xml ở đây = thứ tự khối trên trang chủ
        'views/snippets/s_ten_khoi_1.xml',
        'views/snippets/s_ten_khoi_2.xml',
        'views/snippets/snippets.xml',
        'views/pages/homepage.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_ten_moi/static/src/scss/css_variables.scss',
            'theme_ten_moi/static/src/scss/theme_ten_moi.scss',
            'theme_ten_moi/static/src/js/theme_ten_moi.js',
        ],
    },
    'images': ['static/description/icon.png'],   # chỉ liệt kê file có thật
    'installable': True,
    'application': False,
}
```

**Không** dùng `post_init_hook` để dựng trang. Hook chạy lúc cài, ghi vào mọi website — kể cả website không chọn theme.

---

## 4. Một khối (snippet)

```xml
<odoo>
    <template id="s_ten_khoi_1" name="Tên Khối">
        <section class="s_ten_khoi_1" data-snippet="s_ten_khoi_1" data-name="Tên Khối">
            ...
        </section>
    </template>
</odoo>
```

- Template chứa **đúng một** phần tử gốc (`<section>`).
- `data-snippet` = id template, `data-name` = tên hiện trong editor.
- **Không** thêm class `oe_snippet_body` — editor tự gắn khi đưa vào panel và tự gỡ khi thả.
- Đặt tiền tố riêng cho class, id và tên biến CSS của từng theme (`usa-`, `ielts-`...).

---

## 5. Đăng ký vào panel — `views/snippets/snippets.xml`

```xml
<odoo>
    <template id="snippets" inherit_id="website.snippets" priority="8">
        <xpath expr="//snippets[@id='snippet_structure']" position="inside">
            <t t-snippet="theme_ten_moi.s_ten_khoi_1" string="Tên Khối" group="intro"
               t-thumbnail="/theme_ten_moi/static/description/icon.png">
                <keywords>từ, khoá, để, tìm</keywords>
            </t>
        </xpath>
    </template>
</odoo>
```

Mỗi `t-snippet` **phải có** `string` và `group`. Thiếu `group` thì khối không có chỗ hiện.

| group | Dùng cho |
|---|---|
| `intro` | banner, hero đầu trang |
| `columns` | lưới, danh sách thẻ |
| `content` | khối nội dung chung |
| `text` | trích dẫn, đoạn chữ |
| `images` | gallery, ảnh |
| `people` | đội ngũ, đối tác |
| `contact_and_forms` | CTA, form liên hệ |
| `social` · `products` · `blogs` · `events` · `custom` | theo tên |

XPath kiểu cũ `//div[@id='snippet_structure']//div[hasclass('o_panel_body')]` là của Odoo 15/16 — **không khớp gì trong 18, cài là chết**.

---

## 6. Trang chủ

Không viết tay. Chạy tool:

```bash
python tools/theme_tool.py theme_ten_moi --homepage
```

Tool ghép nguyên markup các khối (theo thứ tự trong manifest) vào một template kế thừa `website.homepage`.

**Không** dùng `<t t-call="...">` cho trang chủ: trang hiện đúng nhưng Builder không sửa xuyên qua `t-call` được — bấm Edit không kéo thả gì được.

Sinh một lần lúc làm theme. Sau đó trang chủ và file snippet được phép khác nhau: snippet là cái *có thể thả vào*, trang chủ là cái *đã thả vào*.

---

## 7. CSS

- Màu thương hiệu viết dạng **CSS custom properties** (`:root { --x: ... }`) trong `css_variables.scss`, để ở `web.assets_frontend`.
- `web._assets_primary_variables` chỉ dành cho **biến SCSS `$...`** mà Bootstrap đọc lúc biên dịch. Để CSS custom properties vào đó là sai chỗ.
- **`min()` / `max()`**: Sass có sẵn hai hàm này và sẽ tự tính. Khác đơn vị (`px` với `%`) là gãy, và một file SCSS gãy thì **cả database mất CSS**. Viết:

```scss
width: #{"min(1180px, 92%)"};   /* đúng — để trình duyệt tự tính */
width: min(1180px, 92%);        /* SAI */
```

`clamp()` thì viết bình thường, Sass không có hàm tên đó.

---

## 8. JS

Mỗi website chỉ chạy một theme, nên hai theme khác nhau không bao giờ đụng nhau. Nhưng **không được** chạy theme cùng một module thường chứa cùng script trên một website: script gắn sự kiện thẳng lên `document` và tìm phần tử theo id, hai bản là mọi cú click xử lý hai lần.

Ví dụ: `isd_theme_usa_program` (bản module thường, vẫn để trong repo) phải được **gỡ** trước khi chọn `theme_usa_program`.

---

## 9. Deploy

Bloompod, vfo, kclickphoto rsync cả repo — theme mới tự lên.

**Ehub thì không**: `.github/workflows/ehub-demo.yml` liệt kê từng module bằng tay. Thêm tên theme vào cả hai chỗ:

```bash
for mod in isd_marketing isd_marketing_template ... theme_ten_moi; do
...
-u isd_marketing,isd_marketing_template,...,theme_ten_moi
```

Thêm vào danh sách `-u` khi theme chưa cài cũng không sao — Odoo chỉ ghi warning rồi bỏ qua.

Push `main` trước, rồi merge `main` vào nhánh khách hàng. Không commit trên nhánh khách hàng.

---

## 10. Cài và đổi theme

Odoo 18 **không có** mục Theme trong menu Configuration. Đường đúng:

1. Chọn website ở góc trên
2. **Edit** → tab **Theme** ở panel phải
3. Kéo xuống cuối, dòng **Theme** → **Switch Theme**
4. Chọn theme trong màn hình **Pick a Theme**

Không thấy theme trong danh sách thì: Apps → ⚙️ → **Update Apps List**.

Đổi sang theme khác cũng đúng chỗ đó — Odoo tự gỡ theme cũ khỏi website.

**Lưu ý khi đổi theme**: Odoo xoá bản trang chủ mà theme cũ đã tạo, nên những gì đã sửa trên trang chủ **mất theo**. Màu đã chỉnh trên site cũng bị reset.
