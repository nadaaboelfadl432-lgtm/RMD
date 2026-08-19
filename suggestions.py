"""
Smart Question Suggestions Engine
----------------------------------
Derives grounded, relevant clinical question suggestions based on user input
and indexed medical content (WHO Guidelines 2021 & MedlinePlus topics).
"""

GROUNDED_CLINICAL_QUESTIONS = [
    # Symptoms & Diagnosis
    {
        "keywords": ["s", "sy", "sym", "symptom", "symptoms", "sign", "warning"],
        "questions": [
            "What are the symptoms of high blood pressure?",
            "What are the symptoms of high blood pressure in pregnancy?",
            "What are the symptoms of pulmonary hypertension?",
            "Are there warning signs or symptoms associated with hypertension?"
        ]
    },
    # Treatment & Medication
    {
        "keywords": ["t", "tr", "treat", "treatment", "medication", "drug", "medicine", "pill", "therapy", "first-line"],
        "questions": [
            "What blood pressure level does WHO recommend for starting treatment?",
            "What are the recommended first-line drugs for hypertension treatment?",
            "What combination drug therapy is recommended for blood pressure control?",
            "When should pharmacological treatment for hypertension be started?"
        ]
    },
    # Targets & Thresholds
    {
        "keywords": ["tar", "target", "goal", "level", "reading", "threshold", "cutoff"],
        "questions": [
            "What is the target blood pressure according to the WHO guideline?",
            "What is the target blood pressure for patients with known cardiovascular disease?",
            "What blood pressure threshold should trigger starting medication?",
            "What is considered normal vs high blood pressure?"
        ]
    },
    # Pregnancy & Special Populations
    {
        "keywords": ["p", "pr", "preg", "pregnant", "pregnancy", "preeclampsia"],
        "questions": [
            "What are the symptoms of high blood pressure in pregnancy?",
            "What blood pressure threshold applies in pregnancy?",
            "How is high blood pressure managed in pregnancy according to clinical guidelines?"
        ]
    },
    # Lifestyle & Salt
    {
        "keywords": ["l", "li", "life", "lifestyle", "diet", "salt", "exercise", "prevent"],
        "questions": [
            "What lifestyle interventions are recommended for managing hypertension?",
            "How does dietary salt reduction affect blood pressure?",
            "What non-pharmacological measures help lower blood pressure?"
        ]
    },
    # Risk factors & Cardiovascular
    {
        "keywords": ["r", "ri", "risk", "complication", "heart", "stroke", "kidney", "cardiovascular"],
        "questions": [
            "What are the cardiovascular risks associated with untreated hypertension?",
            "How does high blood pressure affect heart and kidney health?",
            "Which patient groups are at highest risk from high blood pressure?"
        ]
    }
]

DEFAULT_SUGGESTIONS = [
    "What are the symptoms of high blood pressure?",
    "What blood pressure level does WHO recommend for starting treatment?",
    "What is the target blood pressure according to the WHO guideline?"
]


def get_smart_suggestions(user_input: str, max_suggestions: int = 4) -> list:
    """Returns top 3-4 grounded clinical question suggestions matching user_input in real-time."""
    if not user_input or len(user_input.strip()) == 0:
        return DEFAULT_SUGGESTIONS[:max_suggestions]

    query_lower = user_input.strip().lower()
    matched_questions = []

    # 1. Direct prefix / keyword group matching
    for group in GROUNDED_CLINICAL_QUESTIONS:
        if any(query_lower == kw or query_lower.startswith(kw) or kw.startswith(query_lower) for kw in group["keywords"]):
            for q in group["questions"]:
                if q not in matched_questions:
                    matched_questions.append(q)

    # 2. Substring & word-level matching within questions
    word_matches = []
    all_pool = [q for group in GROUNDED_CLINICAL_QUESTIONS for q in group["questions"]]
    
    for q in all_pool:
        q_words = q.lower().split()
        if any(w.startswith(query_lower) or query_lower in w for w in q_words):
            if q not in matched_questions and q not in word_matches:
                word_matches.append(q)

    final_suggestions = matched_questions + word_matches

    # Fallback to default if empty
    if not final_suggestions:
        final_suggestions = DEFAULT_SUGGESTIONS

    return final_suggestions[:max_suggestions]
