"""Deterministic TRIZ recommendation engine used by the Streamlit app."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, asdict
from typing import Iterable

from data import (
    CONTRADICTION_CELLS,
    DESIGN_AROUND_STRATEGIES,
    FALLBACK_BY_CATEGORY,
    PARAMETER_CATEGORIES,
    PARAMETERS,
    PRINCIPLES,
)


@dataclass
class PrincipleSuggestion:
    number: int
    name: str
    explanation: str
    application: str

    def to_dict(self) -> dict:
        return asdict(self)


def _category(parameter_id: int) -> str:
    for category, ids in PARAMETER_CATEGORIES.items():
        if parameter_id in ids:
            return category
    return "uyum"


def _stable_choice(items: list[str], seed_text: str) -> str:
    if not items:
        return ""
    digest = hashlib.sha256(seed_text.encode("utf-8")).hexdigest()
    return items[int(digest[:8], 16) % len(items)]


def recommend_principles(improving: int, worsening: int) -> tuple[list[int], str]:
    """Return principle IDs and the source type used for the recommendation."""
    pair = (improving, worsening)
    if pair in CONTRADICTION_CELLS:
        return CONTRADICTION_CELLS[pair], "Küratörlü çelişki hücresi"

    categories = (_category(improving), _category(worsening))
    reverse_categories = (categories[1], categories[0])
    if categories in FALLBACK_BY_CATEGORY:
        return FALLBACK_BY_CATEGORY[categories], "Kategori tabanlı bağlamsal eşleştirme"
    if reverse_categories in FALLBACK_BY_CATEGORY:
        return FALLBACK_BY_CATEGORY[reverse_categories], "Kategori tabanlı bağlamsal eşleştirme"
    return [1, 10, 15, 35], "Genel TRIZ başlangıç seti"


def _context_fragments(problem: str, sector: str) -> dict[str, str]:
    lower = problem.lower()
    dynamic_target = "koşullara göre otomatik değişen bir yapı"
    if any(word in lower for word in ["yol", "rota", "ekip", "afet", "dağıtım"]):
        dynamic_target = "bölge, ekip, rota veya görev planını koşullara göre güncelleyen bir yapı"
    elif any(word in lower for word in ["üretim", "makine", "hat", "kalite"]):
        dynamic_target = "hat yükü, kalite ve makine durumuna göre ayarlanan bir yapı"
    elif any(word in lower for word in ["veri", "yazılım", "model", "algoritma"]):
        dynamic_target = "veri miktarı ve karar süresine göre ayrıntı düzeyi değişen bir model"

    return {
        "system": sector.lower(),
        "dynamic_target": dynamic_target,
        "problem": problem.strip() or "tanımlanan problem",
    }


def apply_principle(number: int, problem: str, sector: str, improve_label: str, worsen_label: str) -> str:
    ctx = _context_fragments(problem, sector)
    templates: dict[int, list[str]] = {
        1: [
            "Problemi tek parça çözmek yerine bölge, kullanıcı, süreç veya görev kümelerine ayır; her kümeyi ayrı değerlendir ve sonuçları üst seviyede birleştir.",
            "{problem} için sistemi modüllere ayır. En çok etkilenen modülü önce çözerek tüm sistemi yeniden çalıştırma ihtiyacını azalt.",
        ],
        2: [
            "Kötüleşmeye neden olan veri, adım veya bileşeni ana akıştan ayır; yalnızca gerekli durumda devreye al.",
        ],
        3: [
            "Tüm sisteme aynı kuralı uygulamak yerine kritik bölgelere daha ayrıntılı, düşük öncelikli bölgelere daha sade yöntem uygula.",
        ],
        5: [
            "Aynı veriyi kullanan işlemleri tek hesaplama adımında birleştir; tekrar eden veri hazırlama ve kontrol işlemlerini azalt.",
        ],
        6: [
            "Bir bileşeni yalnızca tek görev için değil, izleme, doğrulama ve karar desteği gibi birden çok görev için kullan.",
        ],
        10: [
            "Olası senaryolar, veri şablonları ve başlangıç çözümlerini olay gerçekleşmeden önce hazırla; olay anında yalnızca farkları güncelle.",
            "{problem} için sık görülen koşullara ait çözüm taslaklarını önceden üret ve gerçek duruma en yakın taslaktan başla.",
        ],
        11: [
            "Eksik veri, arıza veya gecikme için yedek veri kaynağı, güvenli varsayım ve alternatif iş akışı tanımla.",
        ],
        13: [
            "Her değişiklikte tüm çözümü yeniden kurmak yerine etkilenmeyen kısmı sabit tut; yalnızca değişen kısmı serbest bırakıp yeniden çöz.",
            "Kontrolü merkezden sürekli vermek yerine yerel birimlerin değişikliği algılayıp yalnızca kendi bölümünü güncellemesini dene.",
        ],
        15: [
            "{dynamic_target} tasarla. Sabit eşik veya tek plan yerine senaryoya göre değişen parametreler kullan.",
        ],
        19: [
            "Sürekli hesaplama yerine olay tetiklemeli veya periyodik güncelleme uygula; yalnızca anlamlı değişiklik olduğunda modeli çalıştır.",
        ],
        20: [
            "Bekleme sürelerini azaltmak için veri toplama, önceliklendirme ve çözüm adımlarını ardışık bekletmek yerine mümkün olduğunca paralel yürüt.",
        ],
        21: [
            "Acil durumda önce hızlı ve uygulanabilir bir çözüm üret; ayrıntılı iyileştirmeyi zaman izin verdiğinde ikinci aşamada gerçekleştir.",
        ],
        23: [
            "Uygulanan kararın sonucunu ölç ve sapma görüldüğünde parametreleri otomatik güncelleyen geri bildirim döngüsü kur.",
        ],
        24: [
            "Korunan/karmaşık bileşenle doğrudan çalışmak yerine standartlaştırılmış bir aracı katman, dönüştürücü veya karar servisi kullan.",
        ],
        25: [
            "Sistemin kendi veri kalitesini, tutarsızlıklarını ve güncelleme ihtiyacını izleyip kullanıcıya düzeltme önermesini sağla.",
        ],
        26: [
            "Gerçek sistem üzerinde riskli deneme yapmak yerine dijital ikiz, simülasyon veya temsili senaryo üzerinden çözümü doğrula.",
        ],
        28: [
            "Mevcut fiziksel veya manuel mekanizmayı sensör, yazılım, veri tabanlı tahmin ya da optimizasyon gibi farklı bir teknik alanla değiştir.",
        ],
        32: [
            "Durum ve öncelikleri uzun metin yerine renk, simge veya görsel katmanla göster; karar süresini kısalt.",
        ],
        35: [
            "Bölge büyüklüğü, planlama ufku, veri ayrıntısı ve çözüm süresi sınırını {improve_label} ile {worsen_label} arasındaki dengeye göre değiştir.",
            "Tek sabit ayar yerine hızlı, dengeli ve ayrıntılı çalışma modları tanımla.",
        ],
        40: [
            "Tek yöntem yerine kesin optimizasyon, sezgisel yöntem ve önceden hazırlanmış planları hibrit bir çözümde birleştir.",
        ],
    }
    options = templates.get(number, [
        "{problem} için bu ilkeyi; bileşen, süreç, zamanlama veya kontrol mantığında somut bir teknik değişikliğe dönüştür."
    ])
    text = _stable_choice(options, f"{number}|{problem}|{sector}|{improve_label}|{worsen_label}")
    return text.format(
        problem=ctx["problem"],
        dynamic_target=ctx["dynamic_target"],
        improve_label=improve_label.lower(),
        worsen_label=worsen_label.lower(),
    )


def contradiction_solution(improving: int, worsening: int, problem: str, sector: str) -> tuple[list[PrincipleSuggestion], str]:
    principle_ids, source = recommend_principles(improving, worsening)
    improve_label = PARAMETERS[improving]
    worsen_label = PARAMETERS[worsening]
    suggestions = []
    for number in principle_ids:
        name, explanation = PRINCIPLES[number]
        suggestions.append(
            PrincipleSuggestion(
                number=number,
                name=name,
                explanation=explanation,
                application=apply_principle(number, problem, sector, improve_label, worsen_label),
            )
        )
    return suggestions, source


def ideality_score(useful: Iterable[float], harmful: Iterable[float], costs: Iterable[float]) -> float:
    numerator = sum(float(x) for x in useful)
    denominator = sum(float(x) for x in harmful) + sum(float(x) for x in costs)
    if denominator <= 0:
        return numerator
    return numerator / denominator


def ideality_advice(useful_text: str, harmful_text: str, cost_text: str) -> list[str]:
    useful = _split_lines(useful_text)
    harmful = _split_lines(harmful_text)
    costs = _split_lines(cost_text)
    advice = []
    if harmful:
        advice.append(f"Önce en baskın zararlı etkiyi ayır: “{harmful[0]}”. Bu etkiyi yerel olarak sınırlandır veya geri bildirimle erken yakala.")
    if costs:
        advice.append(f"“{costs[0]}” maliyetini azaltmak için önceden eylem, kopyalama/simülasyon ve parametre değişikliği seçeneklerini test et.")
    if useful:
        advice.append(f"“{useful[0]}” yararlı işlevini aynı kaynakla başka bir işlevle birleştirerek evrensellik ilkesini uygula.")
    advice.append("İdeal sonuca yaklaşmak için yeni bir bileşen eklemeden önce mevcut veri, zaman, alan, enerji ve insan kaynağını yeniden kullanmayı dene.")
    return advice[:4]


def _split_lines(text: str) -> list[str]:
    return [part.strip(" -•\t") for part in re.split(r"[\n;]+", text or "") if part.strip(" -•\t")]


def parse_claim_elements(text: str) -> list[str]:
    return _split_lines(text)


def generate_design_around(
    need: str,
    protected_mechanism: str,
    claim_elements: str,
    constraints: str,
    selected_strategies: list[str],
) -> list[dict]:
    elements = parse_claim_elements(claim_elements)
    strategies = selected_strategies or list(DESIGN_AROUND_STRATEGIES)[:3]
    alternatives = []

    for index, strategy in enumerate(strategies[:4], start=1):
        principles = DESIGN_AROUND_STRATEGIES[strategy]
        names = ", ".join(f"{p}. {PRINCIPLES[p][0]}" for p in principles)
        changed_element = elements[(index - 1) % len(elements)] if elements else protected_mechanism or "korunan teknik unsur"

        if strategy == "İşlevi böl ve dağıt":
            concept = (
                f"“{need}” ihtiyacını tek merkezî mekanizma yerine bağımsız modüllere dağıt. "
                f"Özellikle “{changed_element}” unsurunu tek bileşen olmaktan çıkarıp yerel karar veren alt birimlere böl."
            )
        elif strategy == "Kontrol yönünü tersine çevir":
            concept = (
                f"“{changed_element}” unsurunun sistemi yönettiği akışı tersine çevir: merkezî öneri üretmek yerine "
                f"saha/alt birimler değişikliği bildirir, üst katman yalnızca uyuşmazlıkları koordine eder."
            )
        elif strategy == "Sabit yapıyı dinamik yap":
            concept = (
                f"Korunan çözümdeki sabit “{changed_element}” yapısını; olay, bağlam veya geri bildirimle "
                f"parametreleri değişen dinamik bir mimariye dönüştür."
            )
        elif strategy == "Fiziksel yöntemi başka alanla değiştir":
            concept = (
                f"“{changed_element}” ile gerçekleştirilen yöntemi aynı biçimde tekrar etmek yerine işlevi "
                f"simülasyon, optimizasyon, dağıtık kural sistemi veya farklı bir fiziksel alanla karşıla."
            )
        elif strategy == "Doğrudan etkileşim yerine aracı kullan":
            concept = (
                f"Korunan bileşene doğrudan bağlanmak yerine standart bir aracı veri/işlev katmanı kullan. "
                f"Bu katman “{changed_element}” unsurunu farklı giriş ve çıktılarla yeniden tanımlar."
            )
        else:
            concept = (
                f"Sık koşullar için çözüm iskeletini önceden hazırla; “{changed_element}” değiştiğinde tüm çözüm yerine "
                f"yalnızca yerel bölümü güncelle."
            )

        if constraints.strip():
            concept += f" Tasarım şu kısıtlara uymalıdır: {constraints.strip()}."

        distance = min(95, 58 + index * 7 + (8 if len(elements) >= 3 else 0))
        feasibility = max(45, 88 - index * 6 - (5 if len(constraints) > 100 else 0))
        novelty = min(96, 60 + len(set(principles)) * 6 + index * 3)

        alternatives.append({
            "title": f"Alternatif {index}: {strategy}",
            "concept": concept,
            "changed_element": changed_element,
            "principles": names,
            "technical_distance": distance,
            "feasibility": feasibility,
            "novelty": novelty,
            "verification": (
                "İlgili bağımsız istemde zorunlu olan unsurları tek tek kontrol et; bu alternatifte en az bir zorunlu "
                "teknik unsurun kaldırıldığını, değiştirildiğini veya farklı bir teknik ilişkiyle karşılandığını belgeleyin."
            ),
        })
    return alternatives


def build_markdown_report(project: dict) -> str:
    lines = [
        f"# {project.get('name', 'TRIZ Çözüm Raporu')}",
        "",
        f"**Sektör:** {project.get('sector', '-')}",
        f"**Problem:** {project.get('problem', '-')}",
        "",
    ]

    contradiction = project.get("contradiction")
    if contradiction:
        lines.extend([
            "## 1. Çelişki Analizi",
            f"- İyileştirilen özellik: {contradiction.get('improving', '-')}",
            f"- Kötüleşen özellik: {contradiction.get('worsening', '-')}",
            f"- Eşleştirme türü: {contradiction.get('source', '-')}",
            "",
            "### Önerilen ilkeler",
        ])
        for item in contradiction.get("suggestions", []):
            lines.extend([
                f"#### {item['number']}. {item['name']}",
                item["application"],
                "",
            ])

    ideality = project.get("ideality")
    if ideality:
        lines.extend([
            "## 2. İdeallik Analizi",
            f"- İdeallik skoru: {ideality.get('score', 0):.2f}",
            f"- Yararlı işlevler: {ideality.get('useful', '-')}",
            f"- Zararlı etkiler: {ideality.get('harmful', '-')}",
            f"- Maliyetler: {ideality.get('costs', '-')}",
            "",
        ])
        for advice in ideality.get("advice", []):
            lines.append(f"- {advice}")
        lines.append("")

    design = project.get("design_around")
    if design:
        lines.extend([
            "## 3. Patent Etrafından Dolaşma Taslakları",
            f"**Korunan/temel mekanizma:** {design.get('mechanism', '-')}",
            "",
        ])
        for alt in design.get("alternatives", []):
            lines.extend([
                f"### {alt['title']}",
                alt["concept"],
                f"- Değiştirilen teknik unsur: {alt['changed_element']}",
                f"- Kullanılan ilkeler: {alt['principles']}",
                f"- Teknik uzaklık: %{alt['technical_distance']}",
                f"- Uygulanabilirlik: %{alt['feasibility']}",
                f"- Yenilik potansiyeli: %{alt['novelty']}",
                "",
            ])
        lines.append("> Not: Bu çıktı hukuki patent görüşü değildir; teknik fikir üretme ve ön karşılaştırma amaçlıdır.")

    return "\n".join(lines)
