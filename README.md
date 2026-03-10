# DEMPA-ERP-S-STEM

## İlk kodlama adımı (PoC)

Markdown raporu üret:

```bash
python scripts/erp_toolbox_poc.py examples/project_metrics.sample.json --output docs/erp_toolbox_poc_rapor_ornek.md --format md
```

JSON raporu üret:

```bash
python scripts/erp_toolbox_poc.py examples/project_metrics.sample.json --output docs/erp_toolbox_poc_rapor_ornek.json --format json
```

Özel eşik kurallarıyla çalıştır:

```bash
python scripts/erp_toolbox_poc.py examples/project_metrics.sample.json --rules examples/rules.elazig_conservative.json --output docs/erp_toolbox_poc_rapor_elazig.md --format md
```

Test çalıştır:

```bash
python -m unittest tests/test_erp_toolbox_poc.py
```

Detaylar: `docs/erp_toolbox_poc.md`

## Clone-first hızlı başlangıç

Açık kaynak motorları tek komutla klonla/güncelle:

```bash
DRY_RUN=1 bash scripts/bootstrap_clone_first.sh
```

Gerçek klonlama için:

```bash
bash scripts/bootstrap_clone_first.sh
```

Farklı hedef klasör kullanmak için:

```bash
bash scripts/bootstrap_clone_first.sh external/my_stack
```

Önerilen akış:
1. Önce motorları klonla (`bootstrap_clone_first.sh`)
2. PoC risk motorunu çalıştır (`erp_toolbox_poc.py`)
3. Ardından parse + 3B entegrasyonuna geç

