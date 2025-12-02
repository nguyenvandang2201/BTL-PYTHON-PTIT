"""
Module OCR Hóa Đơn - Tự động đọc và trích xuất thông tin từ ảnh hóa đơn
Sử dụng Google Gemini Vision API
"""

import google.generativeai as genai
from config import GOOGLE_API_KEY_OCR
import json
from datetime import datetime
from PIL import Image


class ReceiptOCR:
    """Class xử lý OCR hóa đơn bằng Google Gemini Vision"""
    
    def __init__(self):
        """Khởi tạo Receipt OCR với Google Gemini Vision"""
        genai.configure(api_key=GOOGLE_API_KEY_OCR)
        
        # Sử dụng Gemini 2.5 Flash - multimodal model hỗ trợ ảnh
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_receipt_info(self, image_path):
        """
        Đọc hóa đơn từ ảnh và trích xuất thông tin
        
        Args:
            image_path: Đường dẫn đến file ảnh hóa đơn
            
        Returns:
            dict: Thông tin giao dịch đã trích xuất
        """
        try:
            # Đọc ảnh
            img = Image.open(image_path)
            
            # Tạo prompt cho AI
            prompt = """
Bạn là chuyên gia phân tích hóa đơn tiếng Việt. Hãy đọc hóa đơn trong ảnh và trích xuất thông tin.

QUAN TRỌNG: Trả về ĐÚNG định dạng JSON như sau:
{
    "amount": <số tiền (chỉ số, VD: 50000)>,
    "category": "<danh mục>",
    "description": "<mô tả chi tiết>",
    "date": "<ngày tháng định dạng YYYY-MM-DD>",
    "type": "expense",
    "merchant": "<tên cửa hàng/dịch vụ>"
}

DANH MỤC hợp lệ (chọn 1 trong các danh mục sau):
- Ăn uống: Cafe, nhà hàng, quán ăn, trà sữa, đồ ăn
- Đi lại: Xăng, Grab, taxi, xe bus, vé xe
- Mua sắm: Quần áo, giày dép, mỹ phẩm, đồ dùng
- Nhà cửa: Tiền nhà, điện, nước, internet, gas
- Giải trí: Phim, du lịch, game, vui chơi
- Y tế: Thuốc, khám bệnh, bệnh viện
- Học tập: Sách, khóa học, học phí
- Tiện ích: Điện thoại, internet, dịch vụ
- Khác: Các chi tiêu khác

Lưu ý:
- amount: CHỈ là số nguyên, KHÔNG có đơn vị, KHÔNG có dấu phẩy, KHÔNG có chữ (VD: 50000, không phải "50,000 VNĐ")
- category: Chọn CHÍNH XÁC 1 trong các danh mục trên
- description: Mô tả rõ ràng, ngắn gọn (VD: "Cafe đen đá", "Đổ xăng RON95")
- date: Định dạng YYYY-MM-DD. Nếu không rõ thì dùng ngày hôm nay (2025-11-08)
- type: Luôn là "expense" (chi tiêu)
- merchant: Tên cửa hàng/nhà hàng/dịch vụ (VD: "Highlands Coffee", "Petrolimex")

Ví dụ đầu ra hợp lệ:
{
    "amount": 45000,
    "category": "Ăn uống",
    "description": "Cafe đen đá",
    "date": "2025-11-08",
    "type": "expense",
    "merchant": "Highlands Coffee"
}

CHỈ TRẢ VỀ JSON, KHÔNG GIẢI THÍCH THÊM, KHÔNG THÊM MARKDOWN.
"""
            
            # Gửi ảnh và prompt cho AI
            response = self.model.generate_content([prompt, img])
            
            # Parse JSON từ response
            result_text = response.text.strip()
            
            # Loại bỏ markdown nếu có
            if result_text.startswith('```json'):
                result_text = result_text.replace('```json', '').replace('```', '').strip()
            elif result_text.startswith('```'):
                result_text = result_text.replace('```', '').strip()
            
            # Parse JSON
            receipt_data = json.loads(result_text)
            
            # Validate dữ liệu
            required_fields = ['amount', 'category', 'description', 'date', 'type']
            for field in required_fields:
                if field not in receipt_data:
                    raise ValueError(f"Thiếu trường bắt buộc: {field}")
            
            # Đảm bảo amount là số
            receipt_data['amount'] = float(receipt_data['amount'])
            
            # Validate date format
            try:
                datetime.strptime(receipt_data['date'], '%Y-%m-%d')
            except ValueError:
                receipt_data['date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Đảm bảo merchant tồn tại
            if 'merchant' not in receipt_data:
                receipt_data['merchant'] = 'N/A'
            
            return {
                'success': True,
                'data': receipt_data
            }
            
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Lỗi phân tích JSON: {str(e)}\nResponse: {result_text[:200]}'
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'Không tìm thấy file ảnh'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Lỗi: {str(e)}'
            }
    
    @staticmethod
    def is_available():
        """Kiểm tra xem tính năng OCR có khả dụng không"""
        try:
            import google.generativeai
            from config import GOOGLE_API_KEY_OCR
            return bool(GOOGLE_API_KEY_OCR and 
                       GOOGLE_API_KEY_OCR != "YOUR-GOOGLE-API-KEY-HERE")
        except ImportError:
            return False
        except:
            return False
