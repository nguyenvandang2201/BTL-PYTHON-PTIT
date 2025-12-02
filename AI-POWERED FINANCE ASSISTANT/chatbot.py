"""
Module ChatBot AI sử dụng Google Gemini
Hỗ trợ phân tích và tư vấn tài chính cá nhân
"""

import google.generativeai as genai
from config import GOOGLE_API_KEY
import sqlite3
from datetime import datetime

class FinanceChatBot:
    def __init__(self, user_id, db_connection):
        """Khởi tạo ChatBot với Google Gemini API"""
        self.user_id = user_id
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        
        # Kiểm tra API Key
        if not GOOGLE_API_KEY or GOOGLE_API_KEY.strip() == "":
            self.model = None
            self.chat = None
            return
        
        try:
            # Cấu hình Google Gemini
            genai.configure(api_key=GOOGLE_API_KEY)
            
            # Khởi tạo model (sử dụng gemini-2.5-flash - stable và miễn phí)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Khởi tạo chat session
            self.chat = self.model.start_chat(history=[])
            
            # System prompt
            system_prompt = """Bạn là trợ lý tài chính thông minh giúp người dùng quản lý chi tiêu cá nhân.
            
Nhiệm vụ của bạn:
- Phân tích dữ liệu chi tiêu và đưa ra lời khuyên cụ thể
- Trả lời câu hỏi về tài chính cá nhân
- Đề xuất cách tiết kiệm và quản lý ngân sách hiệu quả
- Giải thích các xu hướng chi tiêu
- Gợi ý tối ưu hóa chi phí

Luôn trả lời bằng tiếng Việt, ngắn gọn, dễ hiểu và hữu ích.
Sử dụng emoji phù hợp để làm câu trả lời sinh động hơn."""
            
            # Gửi system prompt
            self.chat.send_message(system_prompt)
        except Exception as e:
            print(f"Lỗi khởi tạo ChatBot: {e}")
            self.model = None
            self.chat = None
    
    def is_available(self):
        """Kiểm tra ChatBot có sẵn sàng không"""
        return self.model is not None and self.chat is not None
    
    def _check_user_id_column(self):
        """Kiểm tra xem bảng transactions có cột user_id không"""
        try:
            self.cursor.execute("PRAGMA table_info(transactions)")
            columns = [column[1] for column in self.cursor.fetchall()]
            return 'user_id' in columns
        except:
            return False
    
    def get_user_financial_summary(self):
        """Lấy tổng quan tài chính của user"""
        current_month = datetime.now().strftime('%Y-%m')
        
        has_user_id = self._check_user_id_column()
        
        if has_user_id:
            self.cursor.execute('''
                SELECT 
                    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
                FROM transactions 
                WHERE user_id = ? AND strftime('%Y-%m', date) = ?
            ''', (self.user_id, current_month))
        else:
            # Không có user_id, lấy tất cả dữ liệu
            self.cursor.execute('''
                SELECT 
                    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
                FROM transactions 
                WHERE strftime('%Y-%m', date) = ?
            ''', (current_month,))
        
        result = self.cursor.fetchone()
        income = result[0] if result[0] else 0
        expense = result[1] if result[1] else 0
        
        # Chi tiêu theo danh mục
        if has_user_id:
            self.cursor.execute('''
                SELECT category, SUM(amount) as total
                FROM transactions
                WHERE user_id = ? AND type = 'expense' AND strftime('%Y-%m', date) = ?
                GROUP BY category
                ORDER BY total DESC
                LIMIT 5
            ''', (self.user_id, current_month))
        else:
            self.cursor.execute('''
                SELECT category, SUM(amount) as total
                FROM transactions
                WHERE type = 'expense' AND strftime('%Y-%m', date) = ?
                GROUP BY category
                ORDER BY total DESC
                LIMIT 5
            ''', (current_month,))
        
        top_categories = self.cursor.fetchall()
        
        summary = f"""
📊 Tổng quan tài chính tháng {datetime.now().strftime('%m/%Y')}:
💰 Thu nhập: {income:,.0f} VNĐ
💸 Chi tiêu: {expense:,.0f} VNĐ
🏦 Số dư: {income - expense:,.0f} VNĐ

📈 Top danh mục chi tiêu:
"""
        
        if top_categories:
            for idx, (category, amount) in enumerate(top_categories, 1):
                percentage = (amount / expense * 100) if expense > 0 else 0
                summary += f"{idx}. {category}: {amount:,.0f} VNĐ ({percentage:.1f}%)\n"
        else:
            summary += "(Chưa có dữ liệu)\n"
        # Lấy hạn mức chi tiêu (nếu có) từ bảng budget_limits cho tháng hiện tại
        try:
            month_int = int(datetime.now().strftime('%m'))
            year_int = int(datetime.now().strftime('%Y'))
            self.cursor.execute('''
                SELECT limit_amount FROM budget_limits
                WHERE user_id = ? AND month = ? AND year = ?
            ''', (self.user_id, month_int, year_int))
            row = self.cursor.fetchone()
            if row and row[0]:
                limit_amount = row[0]
                used_pct = (expense / limit_amount * 100) if limit_amount > 0 else 0
                summary += f"\n💡 Hạn mức chi tiêu tháng: {limit_amount:,.0f} VNĐ\n"
                summary += f"   • Đã tiêu: {expense:,.0f} VNĐ ({used_pct:.1f}%)\n"
                if expense >= limit_amount:
                    summary += "   ⚠️ Bạn đã vượt (hoặc đạt) hạn mức chi tiêu tháng này. Cần cân nhắc giảm chi tiêu.\n"
                elif used_pct >= 80:
                    summary += "   ⚠️ Bạn đã sử dụng >=80% hạn mức. Hãy lưu ý các chi tiêu không cần thiết.\n"
        except Exception:
            # Nếu bảng/khóa không tồn tại hoặc lỗi, bỏ qua im lặng
            pass

        return summary

    def get_budget_limit(self):
        """Trả về hạn mức chi tiêu của user cho tháng hiện tại (nếu có)

        Returns:
            limit_amount (float) hoặc None
        """
        try:
            month_int = int(datetime.now().strftime('%m'))
            year_int = int(datetime.now().strftime('%Y'))
            self.cursor.execute('''
                SELECT limit_amount FROM budget_limits
                WHERE user_id = ? AND month = ? AND year = ?
            ''', (self.user_id, month_int, year_int))
            row = self.cursor.fetchone()
            return row[0] if row and row[0] else None
        except Exception:
            return None
    
    def get_spending_trend(self, months=3):
        """Phân tích xu hướng chi tiêu"""
        has_user_id = self._check_user_id_column()
        
        if has_user_id:
            self.cursor.execute('''
                SELECT strftime('%Y-%m', date) as month,
                       SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                       SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense
                FROM transactions
                WHERE user_id = ?
                GROUP BY month
                ORDER BY month DESC
                LIMIT ?
            ''', (self.user_id, months))
        else:
            self.cursor.execute('''
                SELECT strftime('%Y-%m', date) as month,
                       SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                       SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense
                FROM transactions
                GROUP BY month
                ORDER BY month DESC
                LIMIT ?
            ''', (months,))
        
        trends = self.cursor.fetchall()
        
        if not trends:
            return "📉 Chưa có dữ liệu để phân tích xu hướng."
        
        trend_text = f"📊 Xu hướng {months} tháng gần đây:\n\n"
        for month, income, expense in trends:
            balance = income - expense
            status = "📈" if balance > 0 else "📉"
            trend_text += f"{status} Tháng {month}:\n"
            trend_text += f"   • Thu: {income:,.0f} VNĐ\n"
            trend_text += f"   • Chi: {expense:,.0f} VNĐ\n"
            trend_text += f"   • Dư: {balance:,.0f} VNĐ\n\n"
        
        return trend_text
    
    def chat_with_context(self, user_message, include_data=True):
        """
        Gửi tin nhắn đến ChatBot với context tài chính
        
        Args:
            user_message: Câu hỏi từ người dùng
            include_data: Có gửi kèm dữ liệu tài chính không
        """
        if not self.is_available():
            return "❌ ChatBot chưa được cấu hình. Vui lòng nhập API Key trong file config.py"
        
        try:
            # Thêm context về dữ liệu tài chính nếu cần
            if include_data:
                financial_summary = self.get_user_financial_summary()
                full_message = f"{financial_summary}\n\n❓ Câu hỏi: {user_message}"
            else:
                full_message = user_message
            
            # Gửi tin nhắn và nhận phản hồi
            response = self.chat.send_message(full_message)
            
            return response.text
            
        except Exception as e:
            error_msg = str(e).lower()
            if "api key" in error_msg or "invalid" in error_msg:
                return "❌ Lỗi: API Key không hợp lệ. Vui lòng kiểm tra lại config.py"
            elif "quota" in error_msg or "limit" in error_msg:
                return "❌ Đã vượt quá giới hạn API. Vui lòng thử lại sau."
            else:
                return f"❌ Có lỗi xảy ra: {str(e)}"
    
    def get_financial_advice(self):
        """Lấy lời khuyên tài chính tự động"""
        if not self.is_available():
            return "❌ ChatBot chưa được cấu hình. Vui lòng nhập API Key trong file config.py"
        
        summary = self.get_user_financial_summary()
        trend = self.get_spending_trend(3)
        
        # Thêm thông tin hạn mức nếu có
        limit_amount = self.get_budget_limit()
        limit_text = ""
        if limit_amount:
            used = 0
            try:
                # Tính phần trăm đã dùng
                expense_line = [line for line in summary.splitlines() if 'Chi tiêu:' in line]
                if expense_line:
                    # extract numeric from line
                    import re
                    m = re.search(r"Chi tiêu:\s*([\d,]+)", expense_line[0])
                    if m:
                        expense_val = float(m.group(1).replace(',', ''))
                        used = expense_val / limit_amount * 100 if limit_amount > 0 else 0
            except Exception:
                used = 0

            limit_text = f"\n💡 Hạn mức chi tiêu tháng: {limit_amount:,.0f} VNĐ (Đã sử dụng ~{used:.1f}%)\n"

        prompt = f"""
{summary}

{trend}

{limit_text}

Dựa trên dữ liệu trên, hãy đưa ra 3-5 lời khuyên CỤ THỂ và HÀNH ĐỘNG để quản lý tài chính tốt hơn.
Mỗi lời khuyên nên:
- Ngắn gọn, dễ hiểu
- Có thể thực hiện được ngay
- Phù hợp với tình hình tài chính hiện tại và hạn mức nếu có
"""

        return self.chat_with_context(prompt, include_data=False)
    
    def analyze_category(self, category):
        """Phân tích chi tiêu theo danh mục cụ thể"""
        if not self.is_available():
            return "❌ ChatBot chưa được cấu hình. Vui lòng nhập API Key trong file config.py"
        
        current_month = datetime.now().strftime('%Y-%m')
        has_user_id = self._check_user_id_column()
        
        # Tổng chi tiêu danh mục này tháng hiện tại
        if has_user_id:
            self.cursor.execute('''
                SELECT SUM(amount) 
                FROM transactions
                WHERE user_id = ? AND category = ? AND type = 'expense' 
                AND strftime('%Y-%m', date) = ?
            ''', (self.user_id, category, current_month))
        else:
            self.cursor.execute('''
                SELECT SUM(amount) 
                FROM transactions
                WHERE category = ? AND type = 'expense' 
                AND strftime('%Y-%m', date) = ?
            ''', (category, current_month))
        
        result = self.cursor.fetchone()
        current_amount = result[0] if result[0] else 0
        
        # Trung bình 3 tháng trước
        if has_user_id:
            self.cursor.execute('''
                SELECT AVG(monthly_total)
                FROM (
                    SELECT SUM(amount) as monthly_total
                    FROM transactions
                    WHERE user_id = ? AND category = ? AND type = 'expense'
                    AND strftime('%Y-%m', date) < ?
                    GROUP BY strftime('%Y-%m', date)
                    ORDER BY date DESC
                    LIMIT 3
                )
            ''', (self.user_id, category, current_month))
        else:
            self.cursor.execute('''
                SELECT AVG(monthly_total)
                FROM (
                    SELECT SUM(amount) as monthly_total
                    FROM transactions
                    WHERE category = ? AND type = 'expense'
                    AND strftime('%Y-%m', date) < ?
                    GROUP BY strftime('%Y-%m', date)
                    ORDER BY date DESC
                    LIMIT 3
                )
            ''', (category, current_month))
        
        result = self.cursor.fetchone()
        avg_amount = result[0] if result[0] else 0
        
        prompt = f"""
📊 Phân tích danh mục '{category}':

💰 Chi tiêu tháng này: {current_amount:,.0f} VNĐ
📈 Trung bình 3 tháng trước: {avg_amount:,.0f} VNĐ
"""
        
        if avg_amount > 0:
            change = ((current_amount - avg_amount) / avg_amount) * 100
            if change > 0:
                prompt += f"📈 Tăng: {change:.1f}%\n"
            else:
                prompt += f"📉 Giảm: {abs(change):.1f}%\n"
        
        prompt += f"""
Hãy phân tích:
1. Mức chi tiêu này có hợp lý không?
2. Có cách nào tối ưu chi phí cho danh mục này?
3. Đưa ra 2-3 gợi ý cụ thể để cải thiện.
"""
        
        return self.chat_with_context(prompt, include_data=False)
    
    def ask_question(self, question):
        """Hỏi câu hỏi thông thường"""
        return self.chat_with_context(question, include_data=True)
    
    def clear_history(self):
        """Reset lịch sử chat"""
        if not self.is_available():
            return
        
        try:
            self.chat = self.model.start_chat(history=[])
        except:
            pass
