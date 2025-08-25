import re
from collections import Counter

# Small, hand-curated stopword list to avoid heavy NLP downloads
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "else", "when", "while", "for", "to", "in", "on", "of", "at", "by",
    "from", "with", "without", "as", "is", "are", "was", "were", "be", "been", "being", "it", "its", "this", "that", "these", "those",
    "you", "your", "yours", "we", "our", "ours", "they", "their", "theirs", "i", "me", "my", "mine",
    "will", "shall", "can", "could", "should", "would", "may", "might", "must", "do", "does", "did",
    "have", "has", "had", "not", "no", "yes", "than", "such", "via", "etc", "per", "within", "across",
    # job-ish filler
    "responsibilities", "required", "requirements", "preferred", "preference", "nice", "plus", "ability", "skills",
    "experience", "experiences", "year", "years", "month", "months", "team", "teams", "work", "working", "environment",
    "knowledge", "strong", "excellent", "good", "great", "including", "include", "includes", "using", "use", "used",
    "build", "built", "develop", "developed", "implement", "implemented", "support", "supported", "maintain", "maintained",
    "collaborate", "collaboration", "deliver", "delivery", "problem", "problems", "solve", "solutions"
}

# Regex that keeps tech tokens like c++, c#, node.js, react.js, etc.
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9\+\#\.\-]{1,}")


def tokenize(text: str):
    return [t.lower() for t in TOKEN_RE.findall(text or "")]


def keywords_from_text(text: str, top_n: int = 40):
    tokens = [t for t in tokenize(text) if t not in STOPWORDS and len(t) >= 2]
    if not tokens:
        return [], Counter()
    freq = Counter(tokens)
    # choose top N by frequency to keep JD-focused signal
    top_tokens = [w for w, _ in freq.most_common(top_n)]
    return top_tokens, freq


def score_resume_vs_jd(resume_text: str, jd_text: str):
    jd_keywords, jd_freq = keywords_from_text(jd_text, top_n=40)
    resume_tokens_set = set(tokenize(resume_text))

    matched = [kw for kw in jd_keywords if kw in resume_tokens_set]
    missing = [kw for kw in jd_keywords if kw not in resume_tokens_set]

    total = max(len(jd_keywords), 1)
    coverage = len(matched) / total
    score10 = round(coverage * 10, 1)

    suggestions = []
    if missing:
        top_missing = ", ".join(missing[:10])
        suggestions.append(
            f"Consider adding these relevant keywords or examples: {top_missing}.")
    if score10 < 7:
        suggestions.append(
            "Tailor your summary/bullets to mirror terminology in the job description.")
    if "react" in resume_tokens_set and "typescript" in resume_tokens_set and "fastapi" in jd_keywords:
        suggestions.append(
            "Mention API integration experience (e.g., FastAPI endpoints) in a bullet point.")

    return {
        "score": score10,
        "coverage_percentage": round(coverage * 100, 1),
        "matched_keywords": matched,
        "missing_keywords": missing,
        "considered_keywords": jd_keywords,
        "suggestions": suggestions
    }
