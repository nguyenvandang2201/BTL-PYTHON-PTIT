"""
Module AI Auto Input - Nhập liệu tự động bằng AI
Người dùng chat văn bản, AI phân tích và tạo giao dịch
"""

import google.generativeai as genai
from config import GOOGLE_API_KEY_AUTO_INPUT
from datetime import datetime
import json
import re

class AIAutoInput:
    def __init__(self):
        """Khởi tạo AI Auto Input"""
        self.api_key = GOOGLE_API_KEY_AUTO_INPUT
        
        if not self.api_key or self.api_key.strip() == "":
            self.model = None
            return
        
        try:
            # Cấu hình Google Gemini
            genai.configure(api_key=self.api_key)
            
            # Khởi tạo model
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            
        except Exception as e:
            print(f"Lỗi khởi tạo AI Auto Input: {e}")
            self.model = None
    
    def is_available(self):
        """Kiểm tra AI có sẵn sàng không"""
        return self.model is not None
    
    def parse_transaction(self, user_message, available_categories):
        """
        Phân tích tin nhắn người dùng và trích xuất thông tin giao dịch
        
        Args:
            user_message: Tin nhắn từ người dùng
            available_categories: Dict danh mục có sẵn {'income': [...], 'expense': [...]}
        
        Returns:
            dict: Thông tin giao dịch hoặc None nếu không phải giao dịch
        """
        if not self.is_available():
            return None
        
        # Tạo danh sách danh mục
        income_cats = ", ".join(available_categories.get('income', []))
        expense_cats = ", ".join(available_categories.get('expense', []))
        
        prompt = f"""
Bạn là trợ lý AI chuyên phân tích giao dịch tài chính từ văn bản tiếng Việt.

NHIỆM VỤ:
Phân tích câu nói của người dùng và trích xuất thông tin giao dịch (nếu có).

DANH MỤC CÓ SẴN:
- Thu nhập: {income_cats}
- Chi tiêu: {expense_cats}

QUY TẮC:
1. Xác định đây có phải là giao dịch tài chính không
2. Nếu KHÔNG phải giao dịch → Trả về: {{"is_transaction": false}}
3. Nếu LÀ giao dịch → Trích xuất thông tin:
   - type: "income" hoặc "expense"
   - category: Chọn từ danh sách trên (phù hợp nhất)
   - amount: Số tiền (chỉ số, không có đơn vị)
   - description: Mô tả ngắn gọn
   - date: Ngày (format YYYY-MM-DD, mặc định hôm nay: {datetime.now().strftime('%Y-%m-%d')})

VÍ DỤ:

Input: "Vừa mua cà phê 50k"
Output: {{"is_transaction": true, "type": "expense", "category": "Ăn uống", "amount": 50000, "description": "Mua cà phê", "date": "{datetime.now().strftime('%Y-%m-%d')}"}}

Input: "Nhận lương 15 triệu"
Output: {{"is_transaction": true, "type": "income", "category": "Lương", "amount": 15000000, "description": "Nhận lương tháng", "date": "{datetime.now().strftime('%Y-%m-%d')}"}}

Input: "Hôm qua ăn phở 50 nghìn"
Output: {{"is_transaction": true, "type": "expense", "category": "Ăn uống", "amount": 50000, "description": "Ăn phở", "date": "{(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')}"}}

Input: "Thời tiết hôm nay thế nào?"
Output: {{"is_transaction": false}}

Input: "Cho tôi lời khuyên tài chính"
Output: {{"is_transaction": false}}

CHÚ Ý:
- k = nghìn = 1,000
- triệu = 1,000,000
- Nếu không có danh mục phù hợp → chọn "Khác"
- Ngày: hôm nay, hôm qua, hôm kia, ngày cụ thể...
- Chỉ trả về JSON, KHÔNG giải thích thêm

TIN NHẮN NGƯỜI DÙNG:
"{user_message}"

CHỈ TRẢ VỀ JSON:
"""
        
        try:
            # Gọi AI
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Loại bỏ markdown code block nếu có
            result_text = result_text.replace('```json', '').replace('```', '').strip()
            
            # Parse JSON
            result = json.loads(result_text)
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"Lỗi parse JSON: {e}")
            print(f"Response: {result_text}")
            return None
        except Exception as e:
            print(f"Lỗi khi phân tích: {e}")
            return None
    
    def extract_multiple_transactions(self, user_message, available_categories):
        """
        Trích xuất nhiều giao dịch từ một tin nhắn
        
        VD: "Hôm nay ăn sáng 30k, trưa 50k, tối 60k"
        """
        if not self.is_available():
            return []
        
        income_cats = ", ".join(available_categories.get('income', []))
        expense_cats = ", ".join(available_categories.get('expense', []))
        
        prompt = f"""
Phân tích câu nói và trích xuất TẤT CẢ các giao dịch (nếu có).

DANH MỤC:
- Thu nhập: {income_cats}
- Chi tiêu: {expense_cats}

TIN NHẮN: "{user_message}"

Trả về JSON array các giao dịch, mỗi giao dịch có:
- type, category, amount, description, date

VÍ DỤ:
Input: "Hôm nay ăn sáng 30k, trưa 50k, tối 60k"
Output: [
  {{"type": "expense", "category": "Ăn uống", "amount": 30000, "description": "Ăn sáng", "date": "{datetime.now().strftime('%Y-%m-%d')}"}},
  {{"type": "expense", "category": "Ăn uống", "amount": 50000, "description": "Ăn trưa", "date": "{datetime.now().strftime('%Y-%m-%d')}"}},
  {{"type": "expense", "category": "Ăn uống", "amount": 60000, "description": "Ăn tối", "date": "{datetime.now().strftime('%Y-%m-%d')}"}}
]

Nếu không có giao dịch → []

CHỈ TRẢ VỀ JSON ARRAY:
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            result_text = result_text.replace('```json', '').replace('```', '').strip()
            
            transactions = json.loads(result_text)
            
            return transactions if isinstance(transactions, list) else []
            
        except Exception as e:
            print(f"Lỗi: {e}")
            return []
    
    def confirm_transaction(self, transaction_info):
        """
        Tạo thông báo xác nhận giao dịch
        """
        type_text = "Thu nhập" if transaction_info['type'] == 'income' else "Chi tiêu"
        amount_text = f"{transaction_info['amount']:,.0f}"
        
        message = f"""
✅ Đã phát hiện giao dịch:

📌 Loại: {type_text}
📂 Danh mục: {transaction_info['category']}
💰 Số tiền: {amount_text} VNĐ
📝 Mô tả: {transaction_info['description']}
📅 Ngày: {transaction_info['date']}

Bạn có muốn thêm giao dịch này không?
"""
        return message.strip()

from datetime import timedelta
