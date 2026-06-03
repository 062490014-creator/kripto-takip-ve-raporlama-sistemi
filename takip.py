import asyncio
import aiohttp
from bildirim import NotificationManager  # 1. yazdığımız bildirim.py dosyasındaki sınıfı çağırıyoruz
from rapor import ReportGenerator      # 2. yazdığımız rapor.py dosyasındaki sınıfı çağırıyoruz

class PriceTracker:
    """Binance API'sine asenkron bağlanarak fiyatları denetler ve diğer sınıfları yönetir."""
    
    def __init__(self, target_price, asset="BTCUSDT"):
        """Kurucu metot. Hedef fiyatı, takip edilecek varlığı ve diğer sınıfları tanımlar."""
        self.target_price = target_price
        self.asset = asset.upper()
        
        # Canlı Binance API adresi
        self.api_url = f"https://api.binance.com/api/v3/ticker/price?symbol={self.asset}"
        
        # Diğer sınıfları bu sınıfın içine katıyoruz
        self.notifier = NotificationManager()
        self.reporter = ReportGenerator()
        
        # Alarmın sürekli değil, hedefe ulaşıldığında sadece 1 kere çalması için kontrol bayrağı (Flag)
        self.alarm_triggered = False

    async def fetch_price(self, session):
        """API'ye non-blocking (asenkron) istek atarak o anki en güncel fiyatı çeker."""
        try:
            async with session.get(self.api_url) as response:
                if response.status == 200:
                    data = await response.json()  # Gelen veriyi JSON olarak çözüyoruz
                    return float(data['price'])
                else:
                    print(f"\n[API HATASI] Sunucu yanıt vermedi. Durum Kodu: {response.status}")
                    return None
        except Exception as e:
            print(f"\n[BAĞLANTI HATASI] Binance sunucusuna erişilemedi: {e}")
            return None

    async def start_tracking(self):
        """Sonsuz döngü başlatarak her 5 saniyede bir fiyatı asenkron kontrol eder."""
        print(f"\n[BAŞLADI] {self.asset} canlı takibi aktif.")
        print(f"[HEDEF] Takip Edilen Eşik Fiyat: ${self.target_price}")
        print("[İPUCU] Programı durdurup PDF raporu üretmek için terminalde 'Ctrl + C' yapın.\n")
        
        # Asenkron internet oturumu açma
        async with aiohttp.ClientSession() as session:
            while True:
                # Fiyat çekme fonksiyonunu 'await' ile asenkron çağırıyoruz
                current_price = await self.fetch_price(session)
                
                if current_price is not None:
                    # Gelen fiyatı zaman damgasıyla RAM loguna eklemesi için ReportGenerator'ı çalıştırıyoruz
                    self.reporter.add_to_log(self.asset, current_price)
                    
                    # Fiyat hedefe ulaştı mı ve daha önce alarm verilmedi mi kontrolü
                    if current_price >= self.target_price and not self.alarm_triggered:
                        # Alarm göndermesi için NotificationManager'ı asenkron olarak çalıştırıyoruz
                        await self.notifier.send_alarm(self.asset, current_price)
                        self.alarm_triggered = True  # Alarmın tekrar tekrar çalışmasını engelliyoruz
                
                # Programı kilitlemeden, arka planda 5 saniye uyutan asenkron bekleme
                await asyncio.sleep(5)