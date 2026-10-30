import re

POSITIVE_WORDS = {
    "great", "awesome", "amazing", "best", "love", "good", "ultimate", "perfect",
    "genius", "top", "easy", "proven", "hack", "pro", "fast", "win", "secret", "incredible"
}
NEGATIVE_WORDS = {
    "bad", "worst", "terrible", "horrible", "hate", "fail", "mistake", "warning",
    "stop", "never", "ruin", "danger", "dead", "wrong", "dark", "trap", "avoid"
}

def compute_sentiment(text: str) -> dict:
    words = re.findall(r"\w+", text.lower())
    if not words:
        return {"compound": 0.0, "pos": 0.0, "neg": 0.0}
    pos_matches = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_matches = sum(1 for w in words if w in NEGATIVE_WORDS)
    total = len(words)
    pos_score = round(pos_matches / total, 3)
    neg_score = round(neg_matches / total, 3)
    diff = pos_matches - neg_matches
    if diff > 0:
        compound = round(min(1.0, 0.25 * diff), 3)
    elif diff < 0:
        compound = round(max(-1.0, 0.25 * diff), 3)
    else:
        compound = 0.0
    return {"compound": compound, "pos": pos_score, "neg": neg_score}

def extract_title_features(title: str) -> dict:
    title_str = str(title or "")
    sentiment = compute_sentiment(title_str)
    length = len(title_str)
    words = title_str.split()
    word_count = len(words)
    alpha_chars = [c for c in title_str if c.isalpha()]
    caps_count = sum(1 for c in alpha_chars if c.isupper())
    caps_ratio = (caps_count / len(alpha_chars)) if alpha_chars else 0.0
    has_digits = int(bool(re.search(r"\d", title_str)))
    has_exclamation = int("!" in title_str)
    has_question = int("?" in title_str)
    power_keywords = [
        "ultimate", "secret", "how to", "best", "worst", "insane",
        "easy", "fast", "must", "never", "stop", "proven", "guide"
    ]
    title_lower = title_str.lower()
    power_word_flag = int(any(pw in title_lower for pw in power_keywords))
    return {
        "title_char_length": length,
        "title_word_count": word_count,
        "title_caps_ratio": round(caps_ratio, 3),
        "title_has_digits": has_digits,
        "title_has_exclamation": has_exclamation,
        "title_has_question": has_question,
        "title_has_power_word": power_word_flag,
        "sentiment_compound": sentiment["compound"],
        "sentiment_positive": sentiment["pos"],
        "sentiment_negative": sentiment["neg"]
    }
