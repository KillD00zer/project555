# خطة مشروع DS555 — تحليل متعدد المتغيرات التطبيقي
## HATCO Customer Satisfaction Study — دراسة رضا عملاء الموردين الصناعيين

**تاريخ الإعداد:** 29 أبريل 2026  
**المقرر:** DS555 — Multivariate Statistical Analysis  
**البرنامج:** Data Science Diploma

---

## 1. وصف البيانات (HATCO Dataset)

| البند | التفاصيل |
|---|---|
| **المصدر** | Hair, Anderson & Tatham Company (HATCO) |
| **الكتاب المرجعي** | Multivariate Data Analysis, 7th Edition |
| **عدد المشاهدات** | 100 عميل |
| **عدد المتغيرات** | 14 متغيراً |
| **نوع البيانات** | استطلاع عملاء شركة توريد صناعية (B2B) |
| **ملفات البيانات** | `data/HATCO.xlsx` + `data/HATCO_Documentation.pdf` |

**فكرة البيانات:**  
الداتا بتمثل عملاء HATCO (مديري مشتريات في شركات) بيقيّموا الشركة على 7 خصائص (تقديرات إدراكية)، بالإضافة لمعلومات عن نتائج الشراء وخصائص الشركة المشترية.

---

## 2. تصنيف المتغيرات

### أ) المتغيرات الكمية / Metric (مقياس 0–10 سنتيمتر)

| المتغير | الوصف | مستوى القياس |
|---|---|---|
| X1 | Delivery Speed — سرعة التسليم | Interval/Ratio |
| X2 | Price Level — مستوى السعر | Interval/Ratio |
| X3 | Price Flexibility — مرونة التسعير | Interval/Ratio |
| X4 | Manufacturer's Image — صورة الشركة | Interval/Ratio |
| X5 | Service Level — جودة الخدمة | Interval/Ratio |
| X6 | Salesforce Image — صورة فريق المبيعات | Interval/Ratio |
| X7 | Product Quality — جودة المنتج | Interval/Ratio |
| X9 | Usage Level — نسبة الشراء من HATCO (0–100%) | Ratio |
| X10 | Satisfaction Level — مستوى الرضا (0–10) | Interval/Ratio |

### ب) المتغيرات النوعية / Non-Metric

| المتغير | الوصف | الترميز | مستوى القياس |
|---|---|---|---|
| X8 | Firm Size — حجم الشركة | 1=كبيرة، 0=صغيرة | Nominal |
| X11 | Specification Buying — أسلوب الشراء | 1=Total Value، 0=Specification | Nominal |
| X12 | Procurement Structure — هيكل الشراء | 1=مركزي، 0=لامركزي | Nominal |
| X13 | Industry Type — نوع الصناعة | 1=صناعة A، 0=أخرى | Nominal |
| X14 | Buying Situation — نوع موقف الشراء | 1=New، 2=Modified، 3=Straight Rebuy | Ordinal |

---

## 3. أهداف البحث

يهدف هذا المشروع لدراسة رضا العملاء وسلوك الشراء لدى عملاء HATCO من خلال:

1. **هل يختلف مستوى الرضا (X10) باختلاف حجم الشركة (X8)؟**  
   → One-Way ANOVA (من المحاضرة 3)

2. **هل يختلف النمط الكلي للإدراك (X1+X5+X7 معاً) باختلاف حجم الشركة (X8)؟**  
   → MANOVA (من المحاضرة 4)

3. **هل يمكن تلخيص إدراك العملاء لـ HATCO (X1–X7) في عوامل أساسية أقل؟**  
   → Factor Analysis (من محاضرة Factor Analysis pptx)

---

## 4. النماذج الإحصائية المختارة

### النموذج الأول: One-Way ANOVA
**المصدر:** المحاضرة 3 (Lecture 3)

| البند | التفاصيل |
|---|---|
| **السؤال** | هل يختلف متوسط مستوى الرضا (X10) بين الشركات الكبيرة والصغيرة (X8)؟ |
| **IV (المستقل)** | X8 — Firm Size (2 فئات: كبيرة / صغيرة) |
| **DV (التابع)** | X10 — Satisfaction Level (0–10) |
| **H₀** | µ_كبيرة = µ_صغيرة |
| **H₁** | µ_كبيرة ≠ µ_صغيرة |
| **اختبارات مسبقة** | Shapiro-Wilk (الطبيعية) + Levene's Test (تجانس التباين) |

**مبرر الاختيار:** السؤال واضح ومباشر، الـ IV فئوي والـ DV كمي مستمر → الحالة الكلاسيكية لـ ANOVA كما في المحاضرة 3.

---

### النموذج الثاني: MANOVA
**المصدر:** المحاضرة 4 (Lecture 4)

| البند | التفاصيل |
|---|---|
| **السؤال** | هل يختلف النمط الكلي للإدراك (X1+X5+X7 معاً) باختلاف حجم الشركة (X8)؟ |
| **IV (المستقل)** | X8 — Firm Size (كبيرة / صغيرة) |
| **DVs (التابعة)** | X1 (سرعة التسليم) + X5 (الخدمة) + X7 (جودة المنتج) |
| **H₀** | لا يوجد فرق في الـ Centroid بين المجموعتين |
| **H₁** | يوجد فرق في الـ Centroid |
| **اختبارات** | Box's M Test + Wilks' Lambda + Univariate Tests لكل DV |

**مبرر الاختيار:** عندنا أكثر من DV واحدة مترابطة (X1, X5, X7 كلها تقيس إدراك العميل لـ HATCO)، MANOVA أدق من 3 ANOVAs منفصلة لأنه يحافظ على α ويتجنب Type I Error inflation (كما شرح الدكتور في المحاضرة 4).

---

### النموذج الثالث: Factor Analysis (EFA)
**المصدر:** محاضرة Factor Analysis (pptx في lecs/)

| البند | التفاصيل |
|---|---|
| **الهدف** | تجميع الـ 7 متغيرات الإدراكية (X1–X7) في عوامل كامنة أقل |
| **المتغيرات** | X1, X2, X3, X4, X5, X6, X7 |
| **طريقة الاستخراج** | Principal Component Analysis (PCA) |
| **اختبار الملاءمة** | KMO (يجب ≥ 0.6) + Bartlett's Test of Sphericity (يجب p < 0.05) |
| **تحديد العوامل** | Eigenvalue > 1 + Scree Plot |
| **دوران العوامل** | Varimax Rotation |
| **المخرجات المتوقعة** | عاملان أو ثلاثة: (عامل القيمة = X2+X3) + (عامل الجودة = X4+X5+X6+X7) + (عامل التوريد = X1) |

**مبرر الاختيار:** الـ 7 متغيرات الإدراكية مترابطة → Factor Analysis يكشف البنية الكامنة ويبسط التفسير.

---

## 5. خطة التنفيذ (المراحل)

### القسم الأول: المقدمة والمتغيرات
- [ ] وصف كامل للبيانات والمصدر (HATCO Dataset)
- [ ] فقرة عن أهداف البحث
- [ ] جدول تصنيف كل متغير (نوعي/كمي + مستوى القياس)

### القسم الثاني: التصور البياني والمقاييس الوصفية
- [ ] **للمتغيرات النوعية (X8, X11, X12, X13, X14):**
  - جداول التكرارات والتكرارات النسبية
  - Bar Charts مع عنوان ورقم تسلسلي وتفسير
- [ ] **للمتغيرات الكمية (X1–X7, X9, X10):**
  - Histograms
  - مقاييس النزعة المركزية (Mean, Median, Mode)
  - مقاييس الموقع (Percentiles, Quartiles)
  - مقاييس التشتت (Std, Variance, Range, IQR)
  - تعليق على كل مقياس

### القسم الثالث: النمذجة والتحليل المتعمق
- [ ] **ANOVA (One-Way):**
  - Normality Test (Shapiro-Wilk)
  - Levene's Test للتجانس
  - ANOVA Table + تفسير
- [ ] **MANOVA:**
  - Box's M Test
  - Wilks' Lambda (Multivariate Test)
  - Tests of Between-Subjects Effects (Univariate)
  - تفسير النتائج
- [ ] **Factor Analysis:**
  - KMO + Bartlett's Test
  - Scree Plot
  - Rotated Component Matrix (Varimax)
  - تسمية العوامل وتفسير التحميلات

### القسم الرابع: الخاتمة
- [ ] ملخص النتائج الرئيسية
- [ ] محدودية الدراسة
- [ ] توصيات مستقبلية

---

## 6. هيكل الملفات

```
project555/
├── data/
│   ├── HATCO.xlsx                      ← البيانات الرئيسية
│   └── HATCO_Documentation.pdf         ← توثيق المتغيرات
├── reports/
│   └── project_plan.md                 ← هذا الملف
├── output/
│   ├── section2_frequencies.txt        ← التكرارات
│   ├── section2_descriptives.txt       ← المقاييس الوصفية
│   ├── section3_anova.txt              ← نتائج ANOVA
│   ├── section3_manova.txt             ← نتائج MANOVA
│   └── section3_factor.txt             ← نتائج Factor Analysis
├── plots/
│   ├── Figure_01_firmsize_bar.png
│   ├── Figure_02_buyingsituation_bar.png
│   ├── Figure_03_X1_delivery_hist.png
│   ├── ...
│   └── Figure_XX_scree_plot.png
└── analysis.py / analysis.R            ← الكود الإحصائي
```

---

## 7. Practice Script — `practice_project.py`

Run with:
```bash
python -X utf8 practice_project.py
```

Script structure:

```
STEP 0  │ Import libraries + Load data
        │
SEC 1   │ Variables Classification
        │ (metric_cols vs nonmetric_cols)
        │
SEC 2A  │ Frequency Tables  → for non-metric columns
SEC 2B  │ Bar Charts        → Figure 1–5  (saved as PNG)
SEC 2C  │ Descriptive Stats → mean, median, std, IQR, range
SEC 2D  │ Histograms        → Figure 6–14 (saved as PNG)
        │
SEC 3A  │ ONE-WAY ANOVA
        │   1. Shapiro-Wilk normality test
        │   2. Levene's test
        │   3. F-test → decision
        │   → Figure 15: boxplot
        │
SEC 3B  │ MANOVA
        │   1. Wilks' Lambda (manual)
        │   2. Approx F-test → decision
        │   3. Univariate follow-up ANOVAs
        │
SEC 3C  │ FACTOR ANALYSIS (PCA)
        │   1. Correlation matrix check
        │   2. PCA eigenvalues table
        │   3. Scree Plot → Figure 16
        │   4. Component loadings table
```

---

## 8. ملاحظات مهمة

> **الطبيعية:** X1–X7 و X10 كلها Continuous (0–10)، ومعظمها سيتبع التوزيع الطبيعي تقريباً.  
> X9 (Usage Level = 0–100%) قد يكون skewed — يُذكر في الوصف الوصفي.

> **تحذير أكاديمي:** يُمنع استخدام أي أداة ذكاء اصطناعي في كتابة التقرير النهائي.  
> هذا الملف للتخطيط فقط — التقرير النهائي يكتبه الطالب بكلامه الخاص.

> **البرنامج المقترح:** SPSS (هو الأساس في المحاضرات) أو R أو Python — حسب تفضيل الفريق.

---
