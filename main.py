#!/usr/bin/env python3
"""Simple lexicon-based sentiment analysis.

Scores text against small positive/negative word lists (with basic
negation handling, e.g. "not good"), and classifies it as positive,
negative, or neutral. Standard library only.
"""
import argparse
import re
import sys

POSITIVE = set("""good great excellent amazing awesome wonderful fantastic
love lovely best beautiful happy joy joyful pleased delight delightful
perfect brilliant superb outstanding success successful win winning
positive hope hopeful kind friendly helpful easy simple fast smooth
clean strong smart clever impressive inspiring enjoy enjoyed fun
recommend satisfied grateful thank thanks nice cool wow incredible""".split())

NEGATIVE = set("""bad terrible awful horrible hate hated worst ugly sad
angry anger disappointed disappointing fail failed failure poor weak
slow broken bug error crash wrong mistake problem issue trouble
difficult hard confusing boring dull useless waste expensive
frustrating annoyed upset worried fear afraid sorry shame
negative loss lose lost dead kill hurt pain sick ill disgusting
annoying stupid dumb terrible horrible dreadful miserable""".split())

NEGATORS = {"not", "no", "never", "n't", "cannot", "can't", "won't",
            "don't", "doesn't", "didn't", "isn't", "wasn't", "aren't"}


def analyse(text):
    """Return (score, positive_hits, negative_hits, label)."""
    tokens = re.findall(r"[a-z']+", text.lower())
    pos = neg = 0
    negated = False
    for token in tokens:
        if token in NEGATORS or token.endswith("n't"):
            negated = True
            continue
        if token in POSITIVE:
            if negated:
                neg += 1
            else:
                pos += 1
            negated = False
        elif token in NEGATIVE:
            if negated:
                pos += 1
            else:
                neg += 1
            negated = False
        elif token not in {"very", "really", "so", "too"}:
            negated = False
    score = pos - neg
    total = pos + neg
    if total == 0:
        label = "neutral"
    elif score > 0:
        label = "positive"
    elif score < 0:
        label = "negative"
    else:
        label = "neutral"
    return score, pos, neg, label


def main():
    parser = argparse.ArgumentParser(
        description="Simple lexicon-based sentiment analysis: classify "
                    "text as positive, negative, or neutral.")
    parser.add_argument("text", nargs="?", help="Text to analyse. If omitted, "
                        "read from a file (--file) or stdin.")
    parser.add_argument("-f", "--file", help="Text file to analyse.")
    parser.add_argument("--json", action="store_true",
                        help="Print the result as JSON.")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                text = f.read()
        except OSError as exc:
            print(f"Error: cannot read {args.file}: {exc}", file=sys.stderr)
            return 1
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("Error: no text provided.", file=sys.stderr)
        return 1

    score, pos, neg, label = analyse(text)
    if args.json:
        import json
        print(json.dumps({"sentiment": label, "score": score,
                          "positive_words": pos, "negative_words": neg}))
    else:
        print(f"Sentiment: {label}")
        print(f"Score: {score} (positive words: {pos}, negative words: {neg})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
