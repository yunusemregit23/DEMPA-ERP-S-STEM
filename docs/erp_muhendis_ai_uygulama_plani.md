# ERP Mühendis AI Modülü – Derin Mimari/Mühendislik Uygulama Planı

Bu plan; ERP içinde çalışan, AutoCAD/ideCAD tabanlı 2B çizimleri teknik karara dönüştüren ve nihai aşamada Blender ile 3B model + render üreten özel AI modülünün hızlı ve güvenli hayata alınması için hazırlanmıştır.

## 1) Stratejik hedef

- Kullanıcının “mimar + mühendis + maliyet uzmanı + görselleştirme uzmanı” beklentisini tek modülde karşılamak.
- Modül çıktısı sadece öneri değil, **karar gerekçesi + karşılaştırma + ERP’ye yazılabilir aksiyon** olmalıdır.

Beklenen nihai çıktı seti:
- Oda boyut/yerleşim önerileri,
- Cephe ve malzeme alternatifleri,
- Yönetmelik uyum raporu,
- Simülasyon kıyas tablosu,
- 3B modelleme ve render üretim planı,
- ERP’de metraj/keşif/revizyon kayıtları.

## 2) Clone-first icra modeli (zorunlu)

> Prensip: Sıfırdan geliştirme yalnızca açık kaynakla kapatılamayan boşluklarda.

### 2.1 Değerlendirme kriterleri
- Lisans uygunluğu (ticari kullanım riski yok),
- Son commit ve bakım sıklığı,
- Topluluk büyüklüğü/issue çözüm hızı,
- API/CLI entegrasyon kolaylığı,
- ERP ile veri akışı uyumluluğu.

### 2.2 İlk klonlanacak adaylar (PoC havuzu)
- **IfcOpenShell** (IFC/BIM veri işleme)
- **BlenderBIM** (Blender-BIM köprüsü)
- **FreeCAD** (parametrik modelleme araçları)
- **ezdxf** (DXF veri okuma/yazma)
- **Blender + Python API örnekleri** (otomatik modelleme/render)
- **LangChain / LlamaIndex** (ajan orkestrasyonu)

### 2.3 Çıktı: Uygunluk matrisi
Her repo için şu puanlar verilir: Lisans / Teknik Uyum / Entegrasyon Maliyeti / Risk.

## 3) Mimari (modül bileşenleri)

1. **Dosya Alım ve Çözümleme Katmanı**
   - DWG/DXF/PDF/IFC alır, normalize eder, katman-semantiği çıkarır.
2. **Mahal ve Geometri Anlamlandırma**
   - oda sınırları, alanlar, dolaşım, cephe ilişkisi.
3. **Karar Motoru (Mimari + Mühendislik)**
   - alternatif üretir: oda planı, cephe tipi, malzeme kombinasyonu.
4. **Yönetmelik Motoru**
   - checklist + ihlal riski + düzeltme önerisi.
5. **Simülasyon/Kıyas Motoru**
   - enerji, maliyet, süre, yapım riski kıyaslar.
6. **3B Üretim Orkestratörü (Blender)**
   - seçilen varyanttan modelleme scriptleri ve render presetleri üretir.
7. **ERP Geri Yazım Katmanı**
   - metraj, keşif kalemi, tedarik önerisi, revizyon kayıtları.

## 4) Senaryo-1 için uçtan uca akış

Senaryo: “AutoCAD/ideCAD çiziminden oda boyutu + cephe + malzeme + yönetmelik + 3B render üret.”

1. Çizim ingest: plan/kesit/görünüş dosyaları alınır.
2. 2B analiz: mahaller, net-brüt m², cephe açıklıkları çıkartılır.
3. Varyant üretimi:
   - V1: maliyet odaklı,
   - V2: enerji/verim odaklı,
   - V3: dengeli seçenek.
4. Yönetmelik kontrolü: her varyant için ihlal ve risk puanı.
5. Simülasyon: enerji + maliyet + yapım süresi kıyası.
6. Karar önerisi: en iyi varyant ve gerekçesi.
7. Blender pipeline: modelleme adımları + materyal/ışık + render.
8. ERP işlemleri: metraj farkı, bütçe etkisi, revizyon task’ları.

## 5) Fazlandırma ve teslimatlar

### Faz 0 (1 hafta): Keşif + Klonlama
- 20+ repo kısa listesi
- ilk 6 repo klonlama ve smoke test
- uygunluk matrisi

### Faz 1 (2 hafta): Karar ve Rapor Çekirdeği
- master prompt entegrasyonu
- karar formatı (alternatif + avantaj/dezavantaj + gerekçe)
- ERP veri sözlüğü bağlantısı

### Faz 2 (3 hafta): 2B Analiz + Yönetmelik
- DXF/PDF parse pipeline
- mahal/alan çıkarımı
- kural motoru ilk sürüm

### Faz 3 (3 hafta): Simülasyon + Blender
- senaryo kıyas katmanı
- Blender script üretimi
- taslak ve final render presetleri

### Faz 4 (2 hafta): Pilot ve Üretim Hazırlığı
- gerçek proje pilotu
- KPI ölçümü
- operasyon devri ve eğitim

## 6) KPI’lar

- Tasarım karar süresinde %30+ kısalma
- Revizyon döngüsünde %20+ azalma
- Yönetmelik kaynaklı geç fark edilen risklerde düşüş
- 3B sunum hazırlama süresinde belirgin hızlanma

## 7) Riskler ve azaltma planı

- **DWG kapalı format riski:** DXF/IFC ara format stratejisi.
- **Yönetmelik güncelliği riski:** versiyonlu kural seti ve periyodik güncelleme.
- **Model kalitesi riski:** insan onayı (human-in-the-loop) ve kalite kontrol checklist.
- **Render süre riski:** taslak/final preset ayrımı ve batch render kuyruğu.

## 8) Hemen başlanacak backlog (ilk sprint)

1. Repo kısa liste + klon + lisans/teknik puanlama.
2. Örnek bir ideCAD/AutoCAD dosyası ile parse PoC.
3. Senaryo-1 için karar şablonu (oda/cephe/malzeme).
4. Yönetmelik checklist’inin v1 hazırlanması.
5. Blender otomasyonunda tek bina kütlesi için script PoC.
6. ERP’ye “alternatif karşılaştırma raporu” nesnesi ekleme.


## 9) Eksik yetenekleri tamamlamak için senden isteyeceğim girdiler

Ajanın daha doğru öneri üretmesi için aşağıdaki verileri kullanıcıdan aktif istemesi zorunludur:

- Proje lokasyonu (ülke/şehir/ilçe) ve bağlayıcı yönetmelik seti,
- Bina tipi (konut/ofis/karma), hedef kalite seviyesi ve bütçe bandı,
- Öncelik sırası (maliyet / enerji / hız / estetik),
- Mevcut çizim dosyaları (DWG/DXF/PDF/IFC) ve revizyon numarası,
- Zorunlu malzeme/marka tercihleri ve tedarik kısıtları,
- Teslim tarihi ve kritik kilometre taşları.

> Kural: Bu bilgiler eksikse asistan, öneri üretmeden önce eksik alanları kullanıcıya soru listesi halinde geri sormalıdır.

## 10) Benzer projelerde popülerlik kontrolü (yıldız/indirme)

- Bu repo içinde `scripts/oss_benchmark.py` eklendi.
- Script, benzer açık kaynak adaylarının GitHub yıldız/fork sayılarını ve mümkün olan paketler için PyPI indirme sayılarını toplar.
- Ağ erişimi olan ortamda çıktılar doğrudan karar matrisine eklenmelidir.

Örnek komut:

```bash
python scripts/oss_benchmark.py
```
