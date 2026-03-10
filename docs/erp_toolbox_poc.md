# ERP Toolbox PoC (Kodlama Başlangıcı)

Bu PoC, AI ajanının CAD/BIM parser katmanından gelecek özet metrikleri okuyup
"maliyeti artırabilecek detaylar" için erken uyarı üretmesini hedefler.

## Ne yapar?

- JSON metrik girdisi alır.
- Kural tabanlı maliyet riski analizi yapar.
- Toplam risk skoru ve seviye (low/medium/high/critical) üretir.
- Markdown veya JSON raporu üretir.
- Eşik değerlerini harici JSON dosyasıyla özelleştirir (`--rules`).
- Eksik verileri açıkça listeler.

## Çalıştırma

Varsayılan kurallarla markdown raporu:

```bash
python scripts/erp_toolbox_poc.py examples/project_metrics.sample.json --output docs/erp_toolbox_poc_rapor_ornek.md --format md
```

Varsayılan kurallarla JSON raporu:

```bash
python scripts/erp_toolbox_poc.py examples/project_metrics.sample.json --output docs/erp_toolbox_poc_rapor_ornek.json --format json
```

Özel eşik kurallarıyla rapor:

```bash
python scripts/erp_toolbox_poc.py examples/project_metrics.sample.json --rules examples/rules.elazig_conservative.json --output docs/erp_toolbox_poc_rapor_elazig.md --format md
```

## Test

```bash
python -m unittest tests/test_erp_toolbox_poc.py
```

## Beklenen entegrasyon

İleride bu scriptin `metrics` girdisi şu kaynaklardan beslenir:
- IFC/BIM parse çıktısı (IfcOpenShell),
- DXF parse çıktısı (ezdxf),
- Proje/ERP metraj verisi.

## Sonraki adım (hemen başla)

1. Clone-first motorları indir/güncelle:

```bash
DRY_RUN=1 bash scripts/bootstrap_clone_first.sh
```

2. PoC risk raporunu üret (pipeline smoke test):

```bash
python scripts/erp_toolbox_poc.py examples/project_metrics.sample.json --output docs/erp_toolbox_poc_rapor_ornek.md --format md
```

3. Testleri çalıştır:

```bash
python -m unittest tests/test_erp_toolbox_poc.py
```

