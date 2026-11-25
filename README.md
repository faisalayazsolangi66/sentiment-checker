# sentiment-checker

Simple lexicon-based sentiment analysis. Scores text against small
positive/negative word lists (with basic negation handling, e.g.
"not good") and classifies it as positive, negative, or neutral.

## Requirements

- Python 3.8+
- No third-party packages (standard library only)

## Usage

```bash
python3 main.py "I love this product, it works great!"
python3 main.py -f review.txt
echo "This is terrible and broken." | python3 main.py
python3 main.py "Great work!" --json
```

Options:

- `text` — text to analyse (omit to use `--file` or stdin)
- `-f, --file` — text file to analyse
- `--json` — print the result as JSON

## Example

```bash
$ python3 main.py "I love this product, it works great and the support team was wonderful!"
```

Sample output:

```
Sentiment: positive
Score: 3 (positive words: 3, negative words: 0)
```

## License

MIT — see [LICENSE](LICENSE).
