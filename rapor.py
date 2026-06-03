import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class ReportGenerator:
    """Program açıkken verileri hafızada (RAM) toplar ve kapanışta PDF raporu üretir."""
    
    def __init__(self):
        # Fiyat geçmişinin anlık olarak birikeceği boş liste 
        self.log_list = []

    def add_to_log(self, asset_name, price):
        """Her 5 saniyede bir gelen fiyatı o anki tarih/saatle birleştirip listeye ekler."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_list.append([timestamp, asset_name, f"${price:.2f}"])
        print(f"[{timestamp}] {asset_name}: ${price:.2f} -> Belleğe kaydedildi.")

    def save_pdf_report(self):
        """Hafızadaki verileri kurumsal bir PDF tablosuna dönüştürür."""
        # Eğer program çok kısa çalıştıysa ve hiç veri birikmediyse PDF üretmeme
        if not self.log_list:
            print("[RAPOR] Kaydedilmiş veri bulunmadığı için PDF üretilmedi.")
            return

        # Benzersiz bir PDF dosya adı oluşturma
        pdf_filename = f"Kripto_Takip_Raporu_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Sayfa yapısını ayarlama
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        story = [] # PDF içindeki başlık, tablo gibi şeylerin dizileceği boş liste
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#1A365D"),
            spaceAfter=15
        )
        
        # PDF İçeriğini Tasarlama
        story.append(Paragraph("Kripto Takip Sistemi Raporu", title_style))
        story.append(Paragraph(f"Rapor Olusturulma Tarihi: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 20)) # Başlık ile tablo arasında boşluk
        
        # Tablo Verisi Hazırlama 
        table_data = [["Tarih", "Kripto Varlik", "Fiyat (USD)"]] + self.log_list
        
        # Tablo Görsel Tasarımı 
        report_table = Table(table_data, colWidths=[150, 100, 100])
        report_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")), # Tablo başlığı lacivert
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),          # Yazı rengi beyazımsı
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                       # Tüm verileri ortala
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),             # Başlık kalın yazı
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),                       # İç boşluk
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F7FAFC")), # Satırların arka planı hafif gri
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),  # İnce gri tablo çizgileri
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(report_table)
        
        # PDF dosyasını diske yazdırma
        try:
            doc.build(story)
            print(f"\n[MÜKEMMEL] Resmi PDF raporu başarıyla üretildi: '{pdf_filename}'")
        except Exception as e:
            print(f"[RAPOR HATASI] PDF üretilirken hata oluştu: {e}")