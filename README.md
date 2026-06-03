# 🚀 Asenkron Kripto Para Takip ve Raporlama Sistemi

Bu proje, Python 3.11 kullanılarak, tamamen Asenkron Mimari (asyncio) ve Nesne Yönelimli Programlama (OOP) prensiplerine uygun olarak geliştirilmiş modüler bir kripto para takip otomasyonudur. 

Sistem, Binance API üzerinden canlı fiyat verilerini non-blocking (asenkron) olarak çeker, belirlenen eşik fiyat aşıldığında Telegram üzerinden anlık mobil bildirim fırlatır ve program kapatıldığında tüm süreç verilerini kurumsal bir PDF raporuna dönüştürür.

---

## 🛠️ Teknolojik Altyapı ve Kütüphaneler

Projede asenkron performansın en üst düzeyde tutulması ve sistem kaynaklarının verimli kullanılması amacıyla aşağıdaki modern teknolojiler tercih edilmiştir:

* **Python asyncio:** API isteklerinin ve zamanlayıcıların birbirini engellemeden (non-blocking) eş zamanlı çalışmasını sağlar.
* **aiohttp:** Binance API ve Telegram API entegrasyonlarında yüksek performanslı, asenkron HTTP istekleri yönetimi için kullanılmıştır.
* **ReportLab:** Program açık olduğu sürece RAM (bellek) üzerinde toplanan fiyat hareketlerini, çıkış esnasında şık ve nizami bir PDF tablosuna dönüştürür.
* **Telegram Bot API:** Kritik fiyat alarmlarını kullanıcının akıllı telefonuna anlık olarak iletir.

---

## 📂 Proje Mimarisi (Modüller)

Proje, yazılımda sürdürülebilirlik ve genişletilebilirlik sağlayan Modüler Tasarım yaklaşımıyla 4 ana sınıfa bölünmüştür:

1. **main.py (Giriş Kapısı):** Asenkron event loop'u başlatan ve sistemin yaşam döngüsünü (açılış/kapanış) yöneten ana tetikleyicidir.
2. **takipci.py (Takip Sınıfı):** Projenin kalbidir. Binance API'sine asenkron istekler atar, fiyatları denetler ve diğer alt modülleri koordine eder.
3. **bildirimci.py (Bildirim Sınıfı):** Alarm durumlarında aiohttp kullanarak Telegram sunucularına asenkron POST istekleri fırlatır.
4. **raporcu.py (Rapor Sınıfı):** Verileri program açıkken bellek loglarında saklar ve kullanıcı Ctrl + C ile sistemi kapattığında kurumsal bir PDF raporu üretir.

---

## 🚀 Kurulum ve Çalıştırma

Projenin bilgisayarınızda çalıştırılabilmesi için aşağıdaki adımları takip etmeniz yeterlidir:

### 1. Gerekli Kütüphanelerin Yüklenmesi
Terminal veya komut satırını açarak proje klasörünün içinde şu komutu çalıştırın:
pip install -r gerekli.txt

### 2. Programın Başlatılması
Sistemi devreye sokmak için ana modülü tetikleyin:
python main.py

### 3. Raporun Alınması
Canlı takip ekranını sonlandırmak ve RAM'de biriken verilerden PDF raporu üretmek için terminalde Ctrl + C kombinasyonunu tuşlamanız yeterlidir. Rapor otomatik olarak proje klasöründe oluşturulacaktır.
