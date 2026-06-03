import asyncio
import sys
from takip import PriceTracker 

async def main():
    # Kullanıcının takip etmek istediği hedef fiyatı belirliyoruz
    target_btc_price = 98500.0  
    
    # Canlı takip motorumuzu başlatıyoruz (Varsayılan BTCUSDT)
    takip = PriceTracker(target_price=target_btc_price)
    
    try:
        # Asenkron döngüyü (start_tracking) çalıştırıyoruz
        await takip.start_tracking()
        
    except asyncio.CancelledError:
        # Kod arka planda kapatılmaya zorlandığında buraya düşer
        pass
        
    except KeyboardInterrupt:
        # Kullanıcı terminalde Ctrl + C yaptığı an burası çalışır
        print("\n[DURDURULDU] Kullanıcı isteği ile takip sonlandırılıyor...")
        
    finally:
        print("[RAPOR MOTORU] RAM'deki veriler PDF'e aktarılıyor...")
        takip.reporter.save_pdf_report()
        print("[ÇIKIŞ] Program başarıyla kapatıldı. Görüşmek üzere!")

if __name__ == "__main__":
    # Windows işletim sistemlerinde asenkron döngünün (asyncio) Ctrl+C sinyallerini düzgün yakalayabilmesi için gerekli olan özel ayar
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    # Ana asenkron fonksiyonunu çalıştırma
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Windows bazen KeyboardInterrupt'ı en dışta yakalamak ister
        print("\n[ÇIKIŞ] Program kapatıldı.")