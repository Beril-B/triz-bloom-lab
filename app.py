from __future__ import annotations

import json

import streamlit as st

from data import PARAMETERS, PRINCIPLES, SECTORS, DESIGN_AROUND_STRATEGIES
from triz_engine import (
    build_markdown_report,
    contradiction_solution,
    generate_design_around,
    ideality_advice,
    ideality_score,
)

st.set_page_config(
    page_title="TRIZ Bloom Lab",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --ink: #f8f7ff;
  --muted: #c9c4e6;
  --navy: #0d1028;
  --navy2: #171638;
  --lilac: #bda7ff;
  --purple: #8c6dfd;
  --mint: #62e7c8;
  --orange: #ffad66;
  --blue: #7dc8ff;
}

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
  background:
    radial-gradient(circle at 15% 0%, rgba(140,109,253,.22), transparent 28%),
    radial-gradient(circle at 100% 20%, rgba(98,231,200,.12), transparent 24%),
    linear-gradient(145deg, #090b1c 0%, #11132d 55%, #0d1028 100%);
  color: var(--ink);
}
[data-testid="stSidebar"] {
  background: rgba(13,16,40,.88);
  border-right: 1px solid rgba(189,167,255,.16);
}
[data-testid="stHeader"] { background: transparent; }

h1, h2, h3, .hero-title { font-family: 'Space Grotesk', sans-serif; }
.hero {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(189,167,255,.24);
  background: linear-gradient(135deg, rgba(189,167,255,.16), rgba(98,231,200,.07));
  border-radius: 28px;
  padding: 34px 36px;
  margin-bottom: 22px;
  box-shadow: 0 22px 70px rgba(0,0,0,.28);
}
.hero:after {
  content: "";
  position: absolute;
  width: 240px; height: 240px; border-radius: 50%;
  right: -70px; top: -90px;
  background: radial-gradient(circle, rgba(255,173,102,.45), transparent 68%);
}
.hero-kicker { color: var(--mint); letter-spacing: .14em; font-weight: 700; font-size: .78rem; }
.hero-title { font-size: 3rem; line-height: 1.02; margin: 8px 0 10px; color: white; }
.hero-copy { max-width: 760px; color: var(--muted); font-size: 1.04rem; }

.module-card, .result-card, .mini-card {
  border: 1px solid rgba(189,167,255,.18);
  background: rgba(22,22,56,.72);
  border-radius: 22px;
  padding: 20px;
  box-shadow: 0 16px 44px rgba(0,0,0,.20);
}
.module-card { min-height: 178px; }
.module-card .num { font-family: 'Space Grotesk'; color: var(--orange); font-weight: 700; }
.module-card h3 { margin: 8px 0 8px; }
.module-card p, .mini-card p { color: var(--muted); }

.principle-badge {
  display: inline-block; padding: 6px 10px; margin-bottom: 8px;
  border-radius: 999px; color: #0d1028; background: linear-gradient(90deg, var(--mint), var(--blue));
  font-weight: 800; font-size: .82rem;
}
.source-badge {
  display: inline-block; padding: 5px 9px; border-radius: 999px;
  background: rgba(255,173,102,.14); color: var(--orange); border: 1px solid rgba(255,173,102,.25);
  font-size: .78rem; font-weight: 700;
}
.metric-orb {
  width: 170px; height: 170px; margin: 6px auto 12px; border-radius: 50%;
  display:flex; align-items:center; justify-content:center; flex-direction:column;
  background: radial-gradient(circle at 35% 25%, rgba(255,255,255,.22), transparent 20%),
              conic-gradient(var(--mint), var(--lilac), var(--orange), var(--mint));
  box-shadow: 0 0 50px rgba(140,109,253,.28);
  color: #0d1028;
}
.metric-orb .score { font: 700 2.2rem 'Space Grotesk'; }
.metric-orb .label { font-size: .78rem; font-weight: 800; letter-spacing:.08em; }

.step-line { color: var(--muted); margin-bottom: 12px; }
.stButton > button, .stDownloadButton > button {
  border-radius: 14px !important;
  border: 1px solid rgba(189,167,255,.35) !important;
  background: linear-gradient(90deg, #8c6dfd, #6d55dc) !important;
  color: white !important;
  font-weight: 700 !important;
  min-height: 46px;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  border-color: var(--mint) !important;
  transform: translateY(-1px);
}
div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div, div[data-baseweb="select"] > div {
  background: rgba(255,255,255,.045) !important;
  border-color: rgba(189,167,255,.22) !important;
}
[data-testid="stMetric"] {
  background: rgba(255,255,255,.045); border: 1px solid rgba(189,167,255,.16);
  padding: 12px 14px; border-radius: 16px;
}
hr { border-color: rgba(189,167,255,.15); }
.small-note { color: var(--muted); font-size: .86rem; }
.footer { text-align:center; color:#8f89b8; font-size:.78rem; padding: 28px 0 8px; }
</style>
""",
    unsafe_allow_html=True,
)


def init_state() -> None:
    defaults = {
        "page": "Ana Laboratuvar",
        "project_name": "Yeni TRIZ Çalışması",
        "sector": SECTORS[0],
        "problem": "",
        "report": {},
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


init_state()

with st.sidebar:
    st.markdown("## ✦ TRIZ Bloom Lab")
    st.caption("Problemi ek → çelişkiyi çöz → teknik alternatifi büyüt")
    st.session_state.project_name = st.text_input("Çalışma adı", st.session_state.project_name)
    st.session_state.sector = st.selectbox("Alan", SECTORS, index=SECTORS.index(st.session_state.sector))
    st.session_state.problem = st.text_area(
        "Problem tohumu",
        st.session_state.problem,
        placeholder="Örn. Karar kalitesi artsın fakat çözüm süresi ve karmaşıklık artmasın.",
        height=118,
    )
    st.divider()
    page = st.radio(
        "Laboratuvar istasyonu",
        ["Ana Laboratuvar", "Çelişki Radarı", "İdeallik Serası", "Design-Around Atölyesi", "Çözüm Dosyası"],
        index=["Ana Laboratuvar", "Çelişki Radarı", "İdeallik Serası", "Design-Around Atölyesi", "Çözüm Dosyası"].index(st.session_state.page),
    )
    st.session_state.page = page
    completed = sum(
        1 for key in ["contradiction", "ideality", "design_around"] if key in st.session_state.report
    )
    st.progress(completed / 3, text=f"Çözüm yolculuğu: {completed}/3 istasyon")
    st.caption("Bu prototip internet veya API anahtarı gerektirmez.")


def hero(kicker: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
<div class="hero">
  <div class="hero-kicker">{kicker}</div>
  <div class="hero-title">{title}</div>
  <div class="hero-copy">{copy}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def set_page(page_name: str) -> None:
    st.session_state.page = page_name
    st.rerun()


if page == "Ana Laboratuvar":
    hero(
        "INTERAKTİF TRIZ STÜDYOSU",
        "Problemi anlat. Çelişkiyi yakala. Çözümü büyüt.",
        "Bu uygulama yalnızca TRIZ kavramlarını açıklamaz; kullanıcı girdilerini çelişki analizi, ideallik ve design-around akışlarıyla işleyerek probleme özel teknik çözüm taslakları üretir.",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """<div class="module-card"><div class="num">01 / RADAR</div><h3>Çelişki Radarı</h3><p>İyileşen ve kötüleşen parametreyi seç. Uygulama TRIZ ilkelerini bulsun ve problemine uyarlasın.</p></div>""",
            unsafe_allow_html=True,
        )
        if st.button("Radarı aç", use_container_width=True):
            set_page("Çelişki Radarı")
    with col2:
        st.markdown(
            """<div class="module-card"><div class="num">02 / GROW</div><h3>İdeallik Serası</h3><p>Yararlı işlevleri büyütürken zararlı etkileri ve maliyetleri azaltan gelişim yönlerini keşfet.</p></div>""",
            unsafe_allow_html=True,
        )
        if st.button("Seraya gir", use_container_width=True):
            set_page("İdeallik Serası")
    with col3:
        st.markdown(
            """<div class="module-card"><div class="num">03 / SHIFT</div><h3>Design-Around Atölyesi</h3><p>Patentteki teknik unsurları parçala; aynı ihtiyacı farklı teknik mimariyle karşılayan alternatifler üret.</p></div>""",
            unsafe_allow_html=True,
        )
        if st.button("Atölyeyi aç", use_container_width=True):
            set_page("Design-Around Atölyesi")

    st.markdown("### Neden klasik bir form değil?")
    a, b, c, d = st.columns(4)
    for col, title, text in [
        (a, "Akış tabanlı", "Kullanıcı tek ekranda kaybolmaz; üç istasyonda adım adım ilerler."),
        (b, "Bağlamsal", "İlkeler sektör ve problem metnine göre somut öneriye çevrilir."),
        (c, "Teknik iz bırakır", "Hangi unsurun hangi ilkeyle değiştirildiği raporda görünür."),
        (d, "Teslim edilebilir", "Sonuç tek tıkla Markdown ve JSON olarak indirilebilir."),
    ]:
        with col:
            st.markdown(f"<div class='mini-card'><h4>{title}</h4><p>{text}</p></div>", unsafe_allow_html=True)

elif page == "Çelişki Radarı":
    hero(
        "İSTASYON 01 · CONTRADICTION",
        "Çelişki Radarı",
        "İyileştirmek istediğin özelliği ve bunun sonucunda kötüleşen özelliği seç. Radar, küratörlü matris hücrelerini veya şeffaf kategori eşleştirmesini kullanarak ilkeleri probleme uygular.",
    )

    left, right = st.columns([1, 1])
    parameter_options = [f"{key}. {value}" for key, value in PARAMETERS.items()]
    with left:
        improve_text = st.selectbox("İyileştirilecek özellik", parameter_options, index=26)
        worsen_text = st.selectbox("Kötüleşen özellik", parameter_options, index=35)
    with right:
        context = st.text_area(
            "Çelişkiyi kendi cümlenle yaz",
            st.session_state.problem,
            placeholder="Örn. Daha fazla ölçüt kullanarak karar güvenilirliği artsın; ancak model karmaşıklığı ve çözüm süresi artmasın.",
            height=132,
        )

    improve_id = int(improve_text.split(".", 1)[0])
    worsen_id = int(worsen_text.split(".", 1)[0])

    if st.button("Radarı çalıştır", type="primary", use_container_width=True):
        suggestions, source = contradiction_solution(
            improve_id, worsen_id, context, st.session_state.sector
        )
        st.session_state.report["name"] = st.session_state.project_name
        st.session_state.report["sector"] = st.session_state.sector
        st.session_state.report["problem"] = context or st.session_state.problem
        st.session_state.report["contradiction"] = {
            "improving": PARAMETERS[improve_id],
            "worsening": PARAMETERS[worsen_id],
            "source": source,
            "suggestions": [item.to_dict() for item in suggestions],
        }

    result = st.session_state.report.get("contradiction")
    if result:
        st.markdown(f"<span class='source-badge'>{result['source']}</span>", unsafe_allow_html=True)
        st.markdown("### Önerilen dönüşüm ilkeleri")
        cols = st.columns(2)
        for idx, item in enumerate(result["suggestions"]):
            with cols[idx % 2]:
                st.markdown(
                    f"""
<div class="result-card">
  <div class="principle-badge">İLKE {item['number']}</div>
  <h3>{item['name']}</h3>
  <p class="small-note">{item['explanation']}</p>
  <hr>
  <strong>Probleme uygulanışı</strong>
  <p>{item['application']}</p>
</div>
""",
                    unsafe_allow_html=True,
                )
        st.success("Çelişki analizi çözüm dosyasına eklendi.")

elif page == "İdeallik Serası":
    hero(
        "İSTASYON 02 · IDEALITY",
        "İdeallik Serası",
        "İdeal sistem, yararlı işlevleri artırırken zararlı etkileri ve maliyetleri azaltır. Burada girdilerini puanlayıp en güçlü gelişim yönünü görürsün.",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        useful_text = st.text_area("Yararlı işlevler", "", placeholder="Her satıra bir işlev\nDaha hızlı müdahale\nDaha fazla kullanıcıya hizmet", height=150)
        useful_score = st.slider("Toplam yarar düzeyi", 1, 30, 18)
    with c2:
        harmful_text = st.text_area("Zararlı etkiler", "", placeholder="Her satıra bir etki\nUzun çözüm süresi\nYanlış yönlendirme", height=150)
        harmful_score = st.slider("Toplam zarar düzeyi", 1, 30, 10)
    with c3:
        cost_text = st.text_area("Maliyet ve kaynak kullanımı", "", placeholder="Her satıra bir maliyet\nHesaplama süresi\nİnsan emeği", height=150)
        cost_score = st.slider("Toplam maliyet düzeyi", 1, 30, 8)

    if st.button("İdeallik profilini büyüt", type="primary", use_container_width=True):
        score = ideality_score([useful_score], [harmful_score], [cost_score])
        advice = ideality_advice(useful_text, harmful_text, cost_text)
        st.session_state.report.update({
            "name": st.session_state.project_name,
            "sector": st.session_state.sector,
            "problem": st.session_state.problem,
        })
        st.session_state.report["ideality"] = {
            "score": score,
            "useful": useful_text,
            "harmful": harmful_text,
            "costs": cost_text,
            "advice": advice,
        }

    result = st.session_state.report.get("ideality")
    if result:
        score = result["score"]
        left, right = st.columns([0.7, 1.3])
        with left:
            st.markdown(
                f"""<div class="metric-orb"><div class="score">{score:.2f}</div><div class="label">İDEALLİK</div></div>""",
                unsafe_allow_html=True,
            )
            if score < 0.8:
                st.warning("Zarar ve maliyetler yarara yakın. Önce baskın zararlı etkiyi hedefle.")
            elif score < 1.5:
                st.info("Dengeli bir başlangıç. Mevcut kaynakları yeniden kullanarak iyileştirme alanı var.")
            else:
                st.success("Yarar baskın. Şimdi çözümü daha az kaynakla aynı sonucu verecek şekilde sadeleştir.")
        with right:
            st.markdown("### Büyüme reçetesi")
            for item in result["advice"]:
                st.markdown(f"<div class='mini-card'><p>✦ {item}</p></div>", unsafe_allow_html=True)
        st.success("İdeallik analizi çözüm dosyasına eklendi.")

elif page == "Design-Around Atölyesi":
    hero(
        "İSTASYON 03 · DESIGN-AROUND",
        "Patent Etrafından Dolaşma Atölyesi",
        "Amaç, ürün adını veya arayüzü değiştirmek değil; bağımsız istemdeki en az bir zorunlu teknik unsuru anlamlı biçimde değiştirerek aynı ihtiyacı farklı teknik yöntemle karşılamaktır.",
    )

    need = st.text_input("Aynı kalması gereken ihtiyaç / işlev", placeholder="Örn. Ağ sorunlarına hızlı müdahale planı üretmek")
    mechanism = st.text_area("Patentte korunan temel teknik mekanizma", placeholder="Örn. Çok kaynaklı ağ verisi + eğitilmiş ML modeli + kök neden tahmini + düzeltme önceliklendirmesi", height=100)
    claim_elements = st.text_area(
        "Bağımsız istemdeki zorunlu teknik unsurlar (her satıra bir unsur)",
        placeholder="Ağ performans verisinin alınması\nSorunlu alanın belirlenmesi\nEğitilmiş modelle kök neden tahmini\nDüzeltme önerisinin kullanıcıya sunulması",
        height=150,
    )
    constraints = st.text_area("Yeni çözümün uyması gereken kısıtlar", placeholder="Gerçek zamanlı çalışmalı; düşük hesaplama maliyeti; açık kaynak veri kullanmalı", height=90)
    strategies = st.multiselect(
        "Dönüşüm stratejileri",
        list(DESIGN_AROUND_STRATEGIES),
        default=["İşlevi böl ve dağıt", "Sabit yapıyı dinamik yap", "Fiziksel yöntemi başka alanla değiştir"],
        max_selections=4,
    )

    if st.button("Teknik alternatifleri üret", type="primary", use_container_width=True):
        alternatives = generate_design_around(need, mechanism, claim_elements, constraints, strategies)
        st.session_state.report.update({
            "name": st.session_state.project_name,
            "sector": st.session_state.sector,
            "problem": st.session_state.problem or need,
        })
        st.session_state.report["design_around"] = {
            "need": need,
            "mechanism": mechanism,
            "claim_elements": claim_elements,
            "alternatives": alternatives,
        }

    result = st.session_state.report.get("design_around")
    if result:
        st.markdown("### Teknik olarak ayrılan alternatifler")
        for alt in result["alternatives"]:
            with st.expander(alt["title"], expanded=True):
                st.write(alt["concept"])
                st.caption(f"Değiştirilen unsur: {alt['changed_element']}")
                st.caption(f"TRIZ dayanağı: {alt['principles']}")
                x, y, z = st.columns(3)
                x.metric("Teknik uzaklık", f"%{alt['technical_distance']}")
                y.metric("Uygulanabilirlik", f"%{alt['feasibility']}")
                z.metric("Yenilik potansiyeli", f"%{alt['novelty']}")
                st.info(alt["verification"])
        st.warning("Bu modül teknik fikir üretir; hukuki patent ihlali veya geçerlilik görüşü vermez.")
        st.success("Design-around çalışması çözüm dosyasına eklendi.")

elif page == "Çözüm Dosyası":
    hero(
        "EXPORT · SOLUTION PACK",
        "Çözüm Dosyası",
        "Tamamladığın istasyonları tek raporda birleştir. Ders teslimi, proje notu veya ekip içi değerlendirme için indir.",
    )

    report = st.session_state.report
    if not report:
        st.info("Henüz bir analiz yok. Önce en az bir laboratuvar istasyonunu tamamla.")
    else:
        completed = [
            label for key, label in [
                ("contradiction", "Çelişki"),
                ("ideality", "İdeallik"),
                ("design_around", "Design-around"),
            ] if key in report
        ]
        st.write("**Tamamlanan modüller:** " + " · ".join(completed))
        markdown_report = build_markdown_report(report)
        st.text_area("Rapor önizleme", markdown_report, height=520)
        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                "Markdown raporu indir",
                markdown_report,
                file_name="triz_cozum_raporu.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with d2:
            st.download_button(
                "JSON çalışma dosyasını indir",
                json.dumps(report, ensure_ascii=False, indent=2),
                file_name="triz_calisma.json",
                mime="application/json",
                use_container_width=True,
            )
        if st.button("Yeni çalışma başlat", use_container_width=True):
            st.session_state.report = {}
            st.session_state.problem = ""
            st.session_state.project_name = "Yeni TRIZ Çalışması"
            st.rerun()

st.markdown("<div class='footer'>TRIZ Bloom Lab · eğitim amaçlı karar ve fikir üretme prototipi</div>", unsafe_allow_html=True)
