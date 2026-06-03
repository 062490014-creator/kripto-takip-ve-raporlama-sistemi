import datetime
import aiohttp

class NotificationManager:
    """Alarm durumlarında Telegram API üzerinden kullanıcının telefonuna
    asenkron olarak anlık bildirim fırlatan sınıf."""
    
    def __init__(self):
        self.bot_token = "BURAYA_KENDI_TELEGRAM_BOT_TOKENINIZI_YAZIN"
        self.chat_id = "BURAYA_KENDI_TELEGRAM_CHAT_ID_INIZI_YAZIN"
        
        # Telegram'ın mesaj gönderme API adresi
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    async def send_alarm(self, asset_name, current_price):
        """Telegram API'sine asenkron POST isteği atarak mesajı telefona gönderir."""
        
        # Telefona gelecek olan bildirim tablosu
        message = (
            f"🚨 ALARM! {asset_name} hedef fiyata ulaştı!\n"
            f"💰 Anlık Fiyat: ${current_price:.2f}\n"
            f"⏰ Zaman: {datetime.datetime.now().strftime('%H:%M:%S')}"
        )
        
        print(f"\n[BİLDİRİM] Telegram API'sine asenkron istek atılıyor...")
        
        try:
            # İnternete bağlanırken programı dondurmayan asenkron oturum açıyoruz
            async with aiohttp.ClientSession() as session:
                payload = {"chat_id": self.chat_id, "text": message}
                
                # Telegram sunucusuna asenkron veri gönderiyoruz
                async with session.post(self.api_url, json=payload) as response:
                    if response.status == 200:
                        print("[TELEGRAM] 🚨 Mesaj başarıyla telefonunuza gönderildi!")
                    else:
                        print(f"[TELEGRAM HATA] Sunucu durum kodu: {response.status}")
        except Exception as e:
            print(f"[TELEGRAM HATA] Bağlantı hatası oluştu: {e}")