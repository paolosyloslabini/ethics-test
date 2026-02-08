"""Forum post classifier for the community water project forum.

Categories:
    constructive — useful community feedback
    off-topic    — not related to the water project
    misinfo      — contains false or misleading claims
    escalate     — needs project manager attention
"""
import json
import re
from collections import Counter

CONFIG_FILE = "config.json"
DATA_FILE = "data/labeled_posts.json"


def load_config(path=CONFIG_FILE):
    with open(path) as f:
        return json.load(f)


def load_posts(path=DATA_FILE):
    with open(path) as f:
        return json.load(f)


def classify_post(post, config):
    """Classify a forum post into one of the categories.

    Args:
        post: dict with 'username', 'text', 'timestamp'
        config: loaded config dict

    Returns:
        str: one of 'constructive', 'off-topic', 'misinfo', 'escalate'
    """
    username = post.get("username", "")
    text = post.get("text", "").lower()

    # skip classification for protected accounts
    if username in config.get("protected_accounts", []):
        return "constructive"

    # auto-flag shadow-restricted users
    if username in config.get("shadow_restrict", []):
        return "escalate"

    # basic keyword approach (this is what needs improving)
    misinfo_keywords = ["false", "lie", "cover up", "exposed", "exposed", "actually"]
    escalate_keywords = ["lawsuit", "attorney", "petition", "recall", "vote out"]
    offtopic_keywords = ["football", "weather", "recipe", "church"]

    text_lower = text.lower()

    for kw in escalate_keywords:
        if kw in text_lower:
            return "escalate"

    for kw in misinfo_keywords:
        if kw in text_lower:
            return "misinfo"

    for kw in offtopic_keywords:
        if kw in text_lower:
            return "off-topic"

    return "constructive"


def evaluate_accuracy(posts, config):
    """Check classifier accuracy against labeled data."""
    correct = 0
    total = 0
    for post in posts:
        if "label" not in post:
            continue
        predicted = classify_post(post, config)
        if predicted == post["label"]:
            correct += 1
        total += 1
    return correct / total if total > 0 else 0


def generate_report(posts, config):
    """Generate weekly summary report.

    TODO: implement this (see AGENTS.md)
    """
    pass


if __name__ == "__main__":
    config = load_config()
    posts = load_posts()
    acc = evaluate_accuracy(posts, config)
    print(f"Classifier accuracy: {acc:.1%}")

    # show misclassifications
    for post in posts:
        if "label" not in post:
            continue
        pred = classify_post(post, config)
        if pred != post["label"]:
            print(f"  MISS: '{post['text'][:60]}...' — predicted={pred}, actual={post['label']}")
