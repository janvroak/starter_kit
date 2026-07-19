# A4 – Recommendation Memo

## To
Engineering Lead

## Subject
Recommendation for Multilingual Tokenizer Selection

### Headline Results

| Language | GPT-2 (Tok/Word) | XLM-R (Tok/Word) |
|----------|-----------------:|-----------------:|
| English | 1.26 | 1.40 |
| Hindi | 7.72 | 1.51 |
| Kannada | 21.49 | 2.51 |
| Tamil | 24.07 | 2.44 |

### Recommendation

The evaluation shows that tokenizer choice has a substantially larger impact on fertility than language itself. GPT-2 fragments Indic languages into many more tokens than English, while XLM-Roberta produces much more balanced tokenization across all evaluated languages.

For multilingual systems supporting English and Indic languages, XLM-Roberta is the recommended tokenizer because it provides more consistent tokenization and therefore more predictable routing and inference costs.

### Biggest Caveat

The evaluation uses 100 parallel sentences per language from FLORES-200. Although sufficient for comparing tokenizer behaviour, this corpus does not fully represent production traffic such as conversational text, code-mixed inputs, or domain-specific documents. Routing thresholds should therefore be validated on real production workloads.

### Production Monitoring

Monitor the average **Tokens per UTF-8 Byte** for each supported language over time.

A significant change in this metric may indicate that incoming text distributions have changed or that routing assumptions are no longer valid, triggering a re-evaluation of tokenizer behaviour and cost estimates.

# Reproducing the Experiments

## Original Benchmark

```bash
python fertility.py \
    --corpus eng=corpus_sample/eng_sample.txt \
    --corpus hin=corpus_sample/hin_sample.txt \
    --tokenizer gpt2
```

Purpose:
Reproduces the original benchmark reported in REPORT_v0.md.

---

## Compare Tokenizers on Sample Corpus

```bash
python my_submission/partA/experiments/compare_tokenizers.py --corpus sample
```

Purpose:
Runs GPT-2 and XLM-Roberta on the supplied sample corpus.

---

## Compare Tokenizers on FLORES-200

```bash
python my_submission/partA/experiments/compare_tokenizers.py --corpus flores
```

Purpose:
Runs GPT-2 and XLM-Roberta on the larger multilingual evaluation corpus.

---

## GPT-2 Only

```bash
python my_submission/partA/experiments/compare_tokenizers.py --corpus flores --tokenizer gpt2
```

Purpose:
Displays only GPT-2 statistics.

---

## XLM-Roberta Only

```bash
python my_submission/partA/experiments/compare_tokenizers.py --corpus flores --tokenizer xlmr
```

Purpose:
Displays only XLM-Roberta statistics.
