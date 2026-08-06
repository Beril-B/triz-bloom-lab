# TRIZ Bloom Lab

Kullanıcı girdilerini TRIZ araçlarıyla işleyip probleme özel teknik çözüm taslakları üreten, oyunlaştırılmış görünümlü Streamlit prototipi.

## Modüller

1. **Çelişki Radarı** — İyileştirilen/kötüleşen parametreyi alır, uygun buluş ilkelerini bulur ve problem bağlamına uygular.
2. **İdeallik Serası** — Yararlı işlev, zararlı etki ve maliyetleri puanlayarak ideallik profili ve gelişim önerileri üretir.
3. **Design-Around Atölyesi** — Patent istemlerindeki zorunlu teknik unsurlardan hareketle aynı ihtiyacı farklı teknik mimariyle karşılayan alternatifler üretir.
4. **Çözüm Dosyası** — Sonuçları Markdown ve JSON olarak indirir.

> Design-around çıktıları hukuki patent görüşü değildir; teknik fikir üretme ve ön karşılaştırma amaçlıdır.

## Yerelde çalıştırma

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub + Streamlit Community Cloud

1. Bu klasördeki tüm dosyaları yeni bir GitHub reposuna yükle.
2. Streamlit Community Cloud'da **Create app** seç.
3. Repo, branch olarak `main`, entrypoint olarak `app.py` seç.
4. Deploy'a bas.

`requirements.txt` repo kökünde, `app.py` ile aynı seviyede tutulmalıdır.

## Dosya yapısı

```text
triz_bloom_lab/
├── app.py
├── data.py
├── triz_engine.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

## Matris kapsamı

MVP, yüksek kullanım olasılığı bulunan seçilmiş çelişki hücrelerini içerir. Seçilen çift doğrudan bilgi tabanında yoksa uygulama bunu gizlemez; kategori tabanlı bağlamsal eşleştirmeye geçer. Tam klasik matris istenirse `data.py` içindeki `CONTRADICTION_CELLS` sözlüğü genişletilebilir.
