# AI-POWERED FINANCE ASSISTANT

## Trợ Lý Tài Chính Thông Minh Được Hỗ Trợ Bởi AI

Ứng dụng quản lý chi tiêu cá nhân hiện đại với **3 tính năng AI đột phá** được tích hợp bởi **Google Gemini 2.5 Flash**, giúp việc quản lý tài chính trở nên dễ dàng và thông minh hơn bao giờ hết.

<div align="center">
  <img src="Screenshot 2025-12-02 235437.png" alt="Dashboard Chính - Giao Diện Quản Lý Chi Tiêu" width="750"/>
  <p><i>📊 Giao diện dashboard chính với biểu đồ trực quan và quản lý giao dịch</i></p>
</div>

---

## 3 TÍNH NĂNG AI THÔNG MINH

### 1. AI ChatBot Tư Vấn Tài Chính
**Module:** `chatbot.py`

Trợ lý AI thông minh hiểu ngữ cảnh, phân tích dữ liệu chi tiêu của bạn và đưa ra lời khuyên tài chính cá nhân hóa.

**Khả năng:**
- Trò chuyện tự nhiên bằng tiếng Việt
- Phân tích chi tiêu theo thời gian thực
- Đưa ra lời khuyên tiết kiệm thông minh
- Giải thích xu hướng chi tiêu
- Tối ưu hóa ngân sách cá nhân
- Cảnh báo chi tiêu vượt hạn mức

**Ví dụ sử dụng:**
```
 Bạn: "Tôi chi tiêu tháng này thế nào?"
 AI: "Tháng này bạn đã chi 12 triệu, trong đó 'Ăn uống' chiếm 
       40% (4.8 triệu). Gợi ý: Hãy cân nhắc nấu ăn tại nhà để 
       tiết kiệm 30-40% chi phí này nhé! "

 Bạn: "Làm sao để tiết kiệm hơn?"
 AI: "Dựa trên dữ liệu của bạn, 3 cách tiết kiệm hiệu quả:
       1. Giảm chi phí cafe (hiện tại 500k/tháng) 
       2. Sử dụng xe bus thay vì Grab (tiết kiệm 1 triệu/tháng) 
       3. Đặt hạn mức 3 triệu cho 'Mua sắm' "
```

<div align="center">
  <img src="Screenshot 2025-12-02 235645.png" alt="AI ChatBot Tư Vấn Tài Chính" width="700"/>
  <p><i>🤖 AI ChatBot phân tích chi tiêu và đưa ra lời khuyên thông minh</i></p>
</div>

---

### 2. AI Auto Input - Nhập Liệu Bằng Chat
**Module:** `ai_auto_input.py`

**Đột phá:** Không cần điền form! Chỉ cần chat tự nhiên, AI tự động hiểu và tạo giao dịch.

**Công nghệ:**
- Natural Language Processing (NLP)
- Tự động phân loại giao dịch
- Nhận diện thời gian (hôm nay, hôm qua, tuần trước...)
- Chuyển đổi số tiền thông minh (k, triệu, tỷ)
- Gán danh mục tự động

**Ví dụ thực tế:**
```
 Bạn: "Vừa mua cafe 50k"
 AI: ✅ Đã tạo giao dịch:
       - Chi tiêu: 50,000 VNĐ
       - Danh mục: Ăn uống 
       - Mô tả: Mua cafe
       - Ngày: 02/12/2025

 Bạn: "Hôm qua ăn phở 45 nghìn"
 AI: ✅ Đã tạo giao dịch:
       - Chi tiêu: 45,000 VNĐ
       - Danh mục: Ăn uống 
       - Mô tả: Ăn phở
       - Ngày: 01/12/2025

 Bạn: "Nhận lương 15 triệu"
 AI: ✅ Đã tạo giao dịch:
       - Thu nhập: 15,000,000 VNĐ
       - Danh mục: Lương 
       - Mô tả: Nhận lương tháng
       - Ngày: 02/12/2025
```

<div align="center">
  <img src="Screenshot 2025-12-02 235608.png" alt="AI Auto Input - Nhập Liệu Bằng Chat" width="700"/>
  <p><i>💬 Nhập giao dịch chỉ bằng cách chat tự nhiên - AI tự động hiểu và xử lý</i></p>
</div>

### 📸 3. AI Receipt OCR - Quét Hóa Đơn Tự Động
**Module:** `receipt_ocr.py`

**Ma thuật:** Chụp ảnh hóa đơn → AI đọc và tạo giao dịch tự động!

**Công nghệ AI Vision:**
- Google Gemini Vision 2.5 Flash
- OCR (Optical Character Recognition)
- Hỗ trợ hóa đơn tiếng Việt
- Trích xuất thông tin thông minh
- Nhận diện tên cửa hàng

**Quy trình:**
```
 Chụp ảnh hóa đơn
    ↓
 AI phân tích ảnh
    ↓
 Trích xuất thông tin:
    • Số tiền
    • Cửa hàng
    • Ngày giờ
    • Loại hàng hóa/dịch vụ
    ↓
 Tạo giao dịch tự động
```

<div align="center">
  <img src="Screenshot 2025-12-02 235846.png" alt="AI Receipt OCR - Quét Hóa Đơn Tự Động" width="700"/>
  <p><i>📸 AI Vision đọc và trích xuất thông tin từ hóa đơn tự động với độ chính xác cao</i></p>
</div>

**Hỗ trợ các loại hóa đơn:**
- Cafe (Highlands, Starbucks, The Coffee House...)
- Nhà hàng
- Cửa hàng xăng dầu
- Siêu thị (CoopMart, Vinmart...)
- Mua sắm (Shopee, Lazada...)
- Grab, GoViet
- Y tế, thuốc
- Hóa đơn điện, nước

**Ưu điểm:**
- Nhanh: 3-5 giây
- Chính xác: 95%+
- Tự động 100%
- Chỉ cần chụp ảnh

---

## TÍNH NĂNG KHÁC

### Quản Lý Chi Tiêu Thông Minh
- Thêm/Sửa/Xóa giao dịch
- Biểu đồ trực quan (tròn, cột, đường)
- Lọc theo ngày/tháng/năm
- Tính tổng thu/chi tự động
- Tìm kiếm nâng cao

### Theo Dõi Giá Vàng Thời Gian Thực
**Module:** `gold_price.py`
- Giá vàng thế giới (USD/ounce)
- Giá vàng Việt Nam (VNĐ/chỉ)
- Biểu đồ biến động
- Cập nhật realtime

### Xuất Báo Cáo PDF
- Báo cáo chi tiết theo tháng/năm
- Biểu đồ phân tích
- In hoặc chia sẻ

### Đa Người Dùng
- Đăng ký/Đăng nhập
- Mã hóa mật khẩu (SHA-256)
- Dữ liệu riêng tư cho mỗi user

---

## CÀI ĐẶT

### 1. Yêu Cầu Hệ Thống
- Python 3.8+
- Kết nối Internet (cho AI features)

### 2. Cài Đặt Thư Viện
```bash
pip install -r requirements.txt
```

**Thư viện chính:**
```
google-generativeai>=0.3.0  # Google Gemini AI
pillow>=10.0.0              # Xử lý ảnh (OCR)
matplotlib==3.7.1           # Biểu đồ
reportlab==4.0.7            # Export PDF
requests>=2.31.0            # API calls
```

#### Cấu hình `config.py`:
```python
# Tư vấn tài chính
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# Nhập liệu tự động
GOOGLE_API_KEY_AUTO_INPUT = "YOUR_API_KEY_HERE"

# OCR hóa đơn
GOOGLE_API_KEY_OCR = "YOUR_API_KEY_HERE"
```

### 4. Chạy Ứng Dụng
```bash
python finance_manager.py
```

---


## CÔNG NGHỆ AI SỬ DỤNG

### Google Gemini 2.5 Flash
- **Model:** `gemini-2.5-flash`
- **Loại:** Multimodal AI (Text + Vision)
- **Đặc điểm:**
  - Nhanh nhất trong dòng Gemini
  - Độ chính xác cao
  - Miễn phí (có giới hạn quota)
  - Hỗ trợ tiếng Việt tốt
  - Nhận diện ảnh (Vision)

### AI Capabilities
- **NLP (Natural Language Processing):** Hiểu ngôn ngữ tự nhiên
- **Named Entity Recognition:** Trích xuất số tiền, ngày tháng
- **Classification:** Phân loại danh mục tự động
- **OCR (Optical Character Recognition):** Đọc văn bản từ ảnh
- **Context Understanding:** Hiểu ngữ cảnh hội thoại
- **Financial Analysis:** Phân tích dữ liệu tài chính

---

## KIẾN TRÚC HỆ THỐNG

```
┌─────────────────────────────────────────────────────┐
│          FINANCE MANAGER (Main App)                 │
│              finance_manager.py                      │
└─────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  ChatBot AI  │  │ AI Auto Input│  │ Receipt OCR  │
│ chatbot.py   │  │ai_auto_input │  │receipt_ocr.py│
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   Google Gemini API   │
              │   gemini-2.5-flash    │
              └───────────────────────┘
```

---

## CẤU TRÚC DỰ ÁN

```
AI-POWERED-FINANCE-ASSISTANT/
│
├── finance_manager.py      # Ứng dụng chính
├── chatbot.py             # AI ChatBot tư vấn
├── ai_auto_input.py       # AI nhập liệu tự động
├── receipt_ocr.py         # AI đọc hóa đơn
├── gold_price.py          # API giá vàng
├── config.py              # Cấu hình API keys
├── requirements.txt       # Thư viện
├── finance.db            # Database SQLite
└── README.md             # Tài liệu này
```

---

## GIAO DIỆN

### Dashboard Chính
- Tổng quan thu/chi
- Biểu đồ trực quan
- Danh sách giao dịch
- Tìm kiếm & Lọc

### Tab AI Features
- **ChatBot:** Chat với AI tư vấn viên
- **Nhập Nhanh:** Chat để thêm giao dịch
- **Quét Hóa Đơn:** Upload ảnh để tạo giao dịch

### Tab Thống Kê
- Biểu đồ tròn (theo danh mục)
- Biểu đồ cột (theo tháng)
- Biểu đồ đường (xu hướng)
- Giá vàng realtime

---

## BẢO MẬT

- Mã hóa mật khẩu (SHA-256)
- API keys được lưu local (không chia sẻ)
- Dữ liệu lưu trên máy cá nhân
- Mỗi user có dữ liệu riêng biệt

**⚠️ LƯU Ý QUAN TRỌNG:**
- Không commit `config.py` có API keys lên Git
- Không chia sẻ API keys với người khác
- Backup file `finance.db` thường xuyên

---

##  XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi: "API Key không hợp lệ"
**Giải pháp:**
1. Kiểm tra API key trong `config.py`
2. Đảm bảo không có khoảng trắng thừa
3. Tạo API key mới 

### Lỗi: "Module không tìm thấy"
**Giải pháp:**
```bash
pip install -r requirements.txt --upgrade
```

### Lỗi: OCR không đọc được hóa đơn
**Giải pháp:**
1. Chụp ảnh rõ nét hơn
2. Đảm bảo ánh sáng đủ
3. Thử với ảnh hóa đơn khác

### AI trả lời bằng tiếng Anh
**Giải pháp:**
- Đã được cấu hình trả lời tiếng Việt
- Nếu vẫn lỗi, thử tạo lại API key

---

## LIÊN HỆ & HỖ TRỢ

- Email: nguyenvandang22012k5@gmail.com
- GitHub: https://github.com/nguyenvandang2201

---