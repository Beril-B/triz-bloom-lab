# TRIZ Bloom Lab

Kullanıcının tanımladığı problemi TRIZ araçlarıyla sistematik biçimde inceleyen; teknik çelişkilere, ideallik düzeyine ve patent istemlerine göre probleme özel çözüm alternatifleri üreten etkileşimli web uygulaması.

🔗 [Uygulama Bağlantısı](https://triz-bloom-lab.streamlit.app/)

## Problem

TRIZ; Çelişki Matrisi, 40 Buluş İlkesi, İdeallik Analizi ve patent etrafından dolaşma gibi farklı araçlardan oluşmaktadır. Ancak kullanıcıların doğru aracı seçmesi, teknik çelişkiyi uygun parametrelerle ifade etmesi ve genel TRIZ ilkelerini kendi problemine uyarlaması zor olabilir.
Bu uygulama yalnızca TRIZ kavramlarını açıklamak yerine kullanıcıdan problem hakkında bilgi alır, bu bilgileri seçilen TRIZ araçlarıyla işler ve probleme yönelik teknik çözüm taslakları üretir.

## Uygulama

Uygulama üç analiz istasyonundan oluşmaktadır:

1. **Çelişki Radarı**  
   Kullanıcı iyileştirmek istediği özelliği ve bu iyileştirme sonucunda kötüleşen özelliği seçer. Uygulama ilgili çelişki için uygun buluş ilkelerini belirler ve bu ilkelerin kullanıcının problemine nasıl uygulanabileceğine ilişkin öneriler üretir.

2. **İdeallik Serası**  
   Kullanıcı sistemin yararlı işlevlerini, zararlı etkilerini ve maliyetlerini tanımlar. Uygulama yararların, zararların ve maliyetlerin göreli düzeylerine göre ideallik skoru hesaplar ve sistemi daha ideal hâle getirmeye yönelik gelişim önerileri sunar.

3. **Design-Around Atölyesi**  
   Kullanıcı patentte karşılanan temel ihtiyacı, korunan teknik mekanizmayı, bağımsız istemdeki zorunlu teknik unsurları ve yeni çözümün kısıtlarını girer. Uygulama, seçilen TRIZ dönüşüm stratejileriyle aynı ihtiyacı farklı bir teknik yöntemle karşılayan alternatif çözüm mimarileri üretir.

Tamamlanan analizler "Çözüm Dosyası" bölümünde birleştirilerek Markdown raporu ve JSON çalışma dosyası olarak indirilebilir.

## Yöntem

### Çelişki analizi

İyileştirilen ve kötüleşen TRIZ parametreleri eşleştirilir. Seçilen çift uygulamanın bilgi tabanında bulunuyorsa tanımlı Çelişki Matrisi hücresi kullanılır. Doğrudan tanımlı olmayan çiftlerde kategori tabanlı bağlamsal eşleştirme yapılır.
Önerilen buluş ilkeleri, kullanıcının problem açıklaması ve seçtiği uygulama alanı dikkate alınarak somut teknik değişikliklere dönüştürülür.

### İdeallik analizi

İdeallik değeri aşağıdaki temel ilişkiye göre hesaplanır:

**İdeallik = Yararlı işlevler / (Zararlı etkiler + Maliyetler)**

Uygulama, baskın zararlı etkiyi ve maliyet unsurunu belirleyerek mevcut kaynakların yeniden kullanılması, zararlı etkilerin yerel olarak sınırlandırılması ve yararlı işlevlerin artırılması yönünde öneriler oluşturur.

### Patent etrafından dolaşma

Patentteki zorunlu teknik unsurlar ayrı ayrı ele alınır. Segmentasyon, tersine çevirme, dinamiklik, aracı kullanma, önceden eylem ve farklı bir teknik alana geçme gibi TRIZ ilkeleri kullanılarak bu unsurlardan en az birini anlamlı biçimde değiştiren alternatifler üretilir.

Her alternatif için:

- Değiştirilen teknik unsur
- Kullanılan TRIZ ilkeleri
- Teknik uzaklık
- Uygulanabilirlik
- Yenilik potansiyeli

göstergeleri sunulur.

## Kullanım

1. Sol panelden çalışma adı ve uygulama alanı seçilir.
2. Problem kısa bir teknik çelişki biçiminde tanımlanır.
3. Çelişki Radarı, İdeallik Serası veya Design-Around Atölyesi açılır.
4. İlgili problem bilgileri girilerek analiz çalıştırılır.
5. Üretilen çözüm önerileri incelenir.
6. Tamamlanan çalışmalar Çözüm Dosyası bölümünden rapor olarak indirilir.

Modüllerin tamamını kullanmak zorunlu değildir. Kullanıcı problemine uygun olan bir veya birden fazla analiz istasyonunu tamamlayabilir.

## Sınırlılıklar

- Uygulama, klasik 39×39 Çelişki Matrisinin bütün hücrelerini içermemektedir. Seçilmiş çelişki çiftleri ve kategori tabanlı bağlamsal eşleştirme kullanılmaktadır.
- Üretilen öneriler, TRIZ ilkelerinin probleme uyarlanmasıyla oluşturulan teknik fikir taslaklarıdır; kesin veya tek doğru çözümü garanti etmez.
- İdeallik puanı, kullanıcının verdiği öznel yarar, zarar ve maliyet değerlerine bağlıdır.
- Teknik uzaklık, uygulanabilirlik ve yenilik potansiyeli göstergeleri sezgisel karşılaştırma değerleridir.
- Design-around bölümü hukuki patent ihlali, patent geçerliliği veya patentlenebilirlik görüşü vermez.
- Nihai bir tasarım kararı verilmeden önce patent istemlerinin uzmanlar tarafından ayrıntılı biçimde incelenmesi ve teknik alternatiflerin doğrulanması gerekir.
- Uygulama internet bağlantısı, haricî yapay zekâ servisi veya API anahtarı kullanmadan çalışır.

## Proje

TOBB ETÜ lisans programı kapsamında, kullanıcıların TRIZ yöntemlerini daha kolay ve sistematik biçimde uygulayabilmesi amacıyla geliştirilmiş eğitim ve teknik fikir üretme prototipidir.
Uygulama, TRIZ araçlarını yalnızca açıklamak yerine kullanıcı girdilerini analiz ederek probleme özel dönüşüm ilkeleri ve alternatif teknik çözüm taslakları üretmektedir.

## İlgili Kaynaklar

- Altshuller, G. S., *The Innovation Algorithm*
- Altshuller, G. S., *Creativity as an Exact Science*
- Altshuller ve Shulyak, *40 Principles: TRIZ Keys to Technical Innovation*
- WIPO, *Patent Drafting Manual*
- WIPO, *Guidelines for Preparing Patent Landscape Reports*
