"""
Smart Question Suggestions Engine
----------------------------------
Derives grounded, relevant clinical question suggestions based on user input
and indexed medical content (WHO Guidelines 2021 & MedlinePlus topics).
Supports Arabic, English, French, and Spanish.
"""

GROUNDED_CLINICAL_QUESTIONS = [
    # Symptoms & Diagnosis
    {
        "keywords": ["s", "sy", "sym", "symptom", "symptoms", "sign", "warning",
                     "علام", "اعراض", "أعراض", "عرض", " symptôme", "síntoma"],
        "questions": [
            "What are the symptoms of high blood pressure?",
            "What are the symptoms of high blood pressure in pregnancy?",
            "What are the symptoms of pulmonary hypertension?",
            "Are there warning signs or symptoms associated with hypertension?"
        ],
        "questions_ar": [
            "ما هي أعراض ارتفاع ضغط الدم؟",
            "ما هي أعراض ارتفاع ضغط الدم أثناء الحمل؟",
            "ما هي أعراض ارتفاع ضغط الدم الرئوي؟",
            "هل هناك علامات تحذيرية مرتبطة بارتفاع ضغط الدم؟"
        ]
    },
    # Treatment & Medication
    {
        "keywords": ["t", "tr", "treat", "treatment", "medication", "drug", "medicine", "pill", "therapy", "first-line",
                     "علاج", "دواء", "أدوية", "علاج", "traitement", "tratamiento"],
        "questions": [
            "What blood pressure level does WHO recommend for starting treatment?",
            "What are the recommended first-line drugs for hypertension treatment?",
            "What combination drug therapy is recommended for blood pressure control?",
            "When should pharmacological treatment for hypertension be started?"
        ],
        "questions_ar": [
            "ما مستوى ضغط الدم الذي توصي منظمة الصحة العالمية ببدء العلاج عنده؟",
            "ما هي الأدوية الأولى الموصى بها لعلاج ارتفاع ضغط الدم؟",
            "ما هو العلاج الدوائي المركب الموصى به للتحكم في ضغط الدم؟",
            "متى يجب بدء العلاج الدوائي لارتفاع ضغط الدم؟"
        ]
    },
    # Targets & Thresholds
    {
        "keywords": ["tar", "target", "goal", "level", "reading", "threshold", "cutoff",
                     "هدف", "مستوى", "ضغط", "قراءة", "cible", "objetivo"],
        "questions": [
            "What is the target blood pressure according to the WHO guideline?",
            "What is the target blood pressure for patients with known cardiovascular disease?",
            "What blood pressure threshold should trigger starting medication?",
            "What is considered normal vs high blood pressure?"
        ],
        "questions_ar": [
            "ما هو هدف ضغط الدم وفقاً لإرشادات منظمة الصحة العالمية؟",
            "ما هو هدف ضغط الدم للمرضى المصابين بأمراض القلب والأوعية الدموية؟",
            "ما مستوى ضغط الدم الذي يجب أن يثير بدء تناول الدواء؟",
            "ما هو ضغط الدم الطبيعي مقارنة بالمرتفع؟"
        ]
    },
    # Pregnancy & Special Populations
    {
        "keywords": ["p", "pr", "preg", "pregnant", "pregnancy", "preeclampsia",
                     "حامل", "حمل", "ولادة", "grossesse", "embarazo"],
        "questions": [
            "What are the symptoms of high blood pressure in pregnancy?",
            "What blood pressure threshold applies in pregnancy?",
            "How is high blood pressure managed in pregnancy according to clinical guidelines?"
        ],
        "questions_ar": [
            "ما هي أعراض ارتفاع ضغط الدم أثناء الحمل؟",
            "ما مستوى ضغط الدم المطبق أثناء الحمل؟",
            "كيف يتم التعامل مع ارتفاع ضغط الدم أثناء الحمل وفقاً للإرشادات السريرية؟"
        ]
    },
    # Lifestyle & Salt
    {
        "keywords": ["l", "li", "life", "lifestyle", "diet", "salt", "exercise", "prevent",
                     "نمط", "حياة", "غذاء", "ملح", "رياضة", "وقاية", "mode de vie", "estilo de vida"],
        "questions": [
            "What lifestyle interventions are recommended for managing hypertension?",
            "How does dietary salt reduction affect blood pressure?",
            "What non-pharmacological measures help lower blood pressure?"
        ],
        "questions_ar": [
            "ما هي التدخلات في نمط الحياة الموصى بها لإدارة ارتفاع ضغط الدم؟",
            "كيف يؤثر تقليل الملح في النظام الغذائي على ضغط الدم؟",
            "ما هي التدابير غير الدوائية التي تساعد في خفض ضغط الدم؟"
        ]
    },
    # Risk factors & Cardiovascular
    {
        "keywords": ["r", "ri", "risk", "complication", "heart", "stroke", "kidney", "cardiovascular",
                     "خطر", "مخاطر", "قلب", "سكتة", "كلى", "وعائي", "risque", "riesgo"],
        "questions": [
            "What are the cardiovascular risks associated with untreated hypertension?",
            "How does high blood pressure affect heart and kidney health?",
            "Which patient groups are at highest risk from high blood pressure?"
        ],
        "questions_ar": [
            "ما هي المخاطر القلبية الوعائية المرتبطة مع عدم علاج ارتفاع ضغط الدم؟",
            "كيف يؤثر ارتفاع ضغط الدم على صحة القلب والكلى؟",
            "ما هي فئات المرضى الأكثر عرضة للخطر من ارتفاع ضغط الدم؟"
        ]
    }
]

DEFAULT_SUGGESTIONS = [
    "What are the symptoms of high blood pressure?",
    "What blood pressure level does WHO recommend for starting treatment?",
    "What is the target blood pressure according to the WHO guideline?"
]

DEFAULT_SUGGESTIONS_AR = [
    "ما هي أعراض ارتفاع ضغط الدم؟",
    "ما مستوى ضغط الدم الذي توصي منظمة الصحة العالمية ببدء العلاج عنده؟",
    "ما هو هدف ضغط الدم وفقاً لإرشادات منظمة الصحة العالمية؟"
]


def _is_arabic(text: str) -> bool:
    """Check if text contains Arabic characters."""
    for ch in text:
        if '\u0600' <= ch <= '\u06FF' or '\u0750' <= ch <= '\u077F' or '\u08A0' <= ch <= '\u08FF':
            return True
    return False


def get_smart_suggestions(user_input: str, max_suggestions: int = 4) -> list:
    """Returns top 3-4 grounded clinical question suggestions matching user_input in real-time.
    Supports Arabic, English, French, and Spanish inputs.
    """
    if not user_input or len(user_input.strip()) == 0:
        return DEFAULT_SUGGESTIONS[:max_suggestions]

    query_lower = user_input.strip().lower()
    is_ar = _is_arabic(user_input)
    matched_questions = []

    # 1. Direct prefix / keyword group matching
    for group in GROUNDED_CLINICAL_QUESTIONS:
        if any(query_lower == kw or query_lower.startswith(kw) or kw.startswith(query_lower) for kw in group["keywords"]):
            pool = group.get("questions_ar", []) if is_ar else group.get("questions", [])
            for q in pool:
                if q not in matched_questions:
                    matched_questions.append(q)

    # 2. Substring & word-level matching within questions
    word_matches = []
    if is_ar:
        all_pool = [q for group in GROUNDED_CLINICAL_QUESTIONS for q in group.get("questions_ar", [])]
    else:
        all_pool = [q for group in GROUNDED_CLINICAL_QUESTIONS for q in group.get("questions", [])]

    for q in all_pool:
        q_lower = q.lower()
        if query_lower in q_lower:
            if q not in matched_questions and q not in word_matches:
                word_matches.append(q)
        else:
            q_words = q_lower.split()
            if any(w.startswith(query_lower) or query_lower in w for w in q_words):
                if q not in matched_questions and q not in word_matches:
                    word_matches.append(q)

    final_suggestions = matched_questions + word_matches

    # Fallback to default if empty
    if not final_suggestions:
        final_suggestions = DEFAULT_SUGGESTIONS_AR if is_ar else DEFAULT_SUGGESTIONS

    return final_suggestions[:max_suggestions]
