# -*- coding: utf-8 -*-
{
    'name': 'Theme The IELTS Workshop',
    'summary': 'Chất lượng vàng trong luyện thi IELTS - Giao diện chuyên nghiệp cho Odoo 18 & 19',
    'description': """
Theme The IELTS Workshop (TIW) for Odoo 18 & 19 Website Builder:
================================================================
- Thiết kế hiện đại chuẩn nhận diện thương hiệu TIW (Cam #F27439, Vàng #EEDD2F, Đen #262626)
- Bộ building blocks (Snippets) kéo thả trực quan cho Website Builder:
  * Hero Section Carousel & Call To Action
  * 4 Giá trị cốt lõi & Chân dung Founder Đặng Trần Tùng (9.0 IELTS)
  * Lộ trình các khóa học (Freshman, Sophomore, Junior, Senior & Master)
  * Đội ngũ giảng viên 8.5 - 9.0 IELTS có chứng chỉ quốc tế
  * Mini Test trắc nghiệm 4 kỹ năng tương tác trực tiếp
  * Bảng vàng học viên & Cảm nhận thực tế
  * Form đăng ký nhận lộ trình & tích hợp CRM Leads của Odoo
  * Bản đồ & Hệ thống 18 cơ sở tại Hà Nội & TP.HCM
  * Tin tức & Thư viện tự học
- Tích hợp Widget Hotline, Test Free & Nút cuộn trang mượt mà
- Tương thích 100% Bootstrap 5.3 và OWL 2 trên Odoo 18.0 & 19.0
    """,
    'category': 'Theme/Education',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'The IELTS Workshop',
    'website': 'https://theieltsworkshop.com',
    'depends': [
        'website',
        'website_crm',
    ],
    'data': [
        'data/menu.xml',
        'views/pages/header_footer.xml',
        'views/snippets/s_tiw_hero.xml',
        'views/snippets/s_tiw_why_us.xml',
        'views/snippets/s_tiw_courses.xml',
        'views/snippets/s_tiw_teachers.xml',
        'views/snippets/s_tiw_mini_test.xml',
        'views/snippets/s_tiw_registration.xml',
        'views/snippets/snippets.xml',
        'views/pages/homepage.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'theme_theieltsworkshop/static/src/scss/primary_variables.scss',
        ],
        'web.assets_frontend': [
            'theme_theieltsworkshop/static/src/scss/theme.scss',
            'theme_theieltsworkshop/static/src/js/mini_test.js',
            'theme_theieltsworkshop/static/src/js/floating_widgets.js',
            'theme_theieltsworkshop/static/src/js/registration.js',
        ],
    },
    'images': [
        'static/description/theme_screenshot.png',
    ],
    'application': False,
    'auto_install': False,
    'installable': True,
}

