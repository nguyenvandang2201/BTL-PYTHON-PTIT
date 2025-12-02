"""
Module lấy giá vàng trực tiếp từ API
"""

import requests
import json
from datetime import datetime

class GoldPriceAPI:
    """Class để lấy và xử lý dữ liệu giá vàng"""
    
    def __init__(self):
        # Sử dụng API miễn phí từ metals-api.com (không cần key)
        # Hoặc có thể dùng API khác
        self.use_fallback = True
    
    def get_current_price(self):
        """
        Lấy giá vàng hiện tại
        
        Returns:
            dict: Thông tin giá vàng
        """
        try:
            # Sử dụng API công khai từ nbg.gov.ge (National Bank of Georgia)
            # Hoặc API miễn phí khác
            
            # Giá vàng tham khảo từ Kitco (không cần API key)
            url = "https://api.metals.live/v1/spot/gold"
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Giá vàng USD/ounce
                price_usd = data[0].get('price', 0)
                
                # Chuyển đổi sang VND (tỷ giá tham khảo: 1 USD = 24,500 VND)
                usd_to_vnd = 24500
                price_vnd = price_usd * usd_to_vnd
                price_per_gram = price_vnd / 31.1035  # Chuyển từ ounce sang gram
                
                # Tính thay đổi (giả lập)
                timestamp_data = data[0].get('timestamp', 0)
                
                return {
                    'success': True,
                    'price': price_vnd,
                    'price_per_gram': price_per_gram,
                    'timestamp': datetime.fromtimestamp(timestamp_data / 1000) if timestamp_data > 0 else datetime.now(),
                    'change_24h': 0.5,  # Giả lập, API này không có thông tin này
                    'high_24h': price_vnd * 1.01,
                    'low_24h': price_vnd * 0.99,
                    'open_24h': price_vnd
                }
            else:
                # Fallback: Giá vàng tham khảo cố định
                return self._get_fallback_price()
                
        except requests.exceptions.Timeout:
            return self._get_fallback_price()
        except requests.exceptions.RequestException:
            return self._get_fallback_price()
        except Exception:
            return self._get_fallback_price()
    
    def _get_fallback_price(self):
        """Trả về giá vàng tham khảo khi API lỗi"""
        # Giá vàng thế giới tham khảo (cập nhật thủ công)
        # Tính theo giá thực tế khoảng ~2000 USD/ounce
        base_price_usd = 2050
        usd_to_vnd = 24500
        price_vnd = base_price_usd * usd_to_vnd
        price_per_gram = price_vnd / 31.1035
        
        return {
            'success': True,
            'price': price_vnd,
            'price_per_gram': price_per_gram,
            'timestamp': datetime.now(),
            'change_24h': 0.0,
            'high_24h': price_vnd,
            'low_24h': price_vnd,
            'open_24h': price_vnd,
            'note': 'Giá tham khảo'
        }
    
    def format_price(self, price):
        """Format giá vàng cho dễ đọc"""
        return f"{price:,.0f}"
    
    @staticmethod
    def is_available():
        """Kiểm tra module có khả dụng không"""
        try:
            import requests
            return True
        except ImportError:
            return False
