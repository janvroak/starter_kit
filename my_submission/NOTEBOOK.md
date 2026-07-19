# AI Team Intern Assignment

## Lab Notebook

---

## Day 1

### Initial Understanding

Objective:
Audit the previous intern's report rather than creating a new benchmark.

Actions:
- Read assignment instructions.
- Identified deliverables.
- Examined repository structure.
- Began reviewing REPORT_v0.md.

Initial observations:
- Report contains strong conclusions that require verification.
- Assignment emphasizes evidence over assumptions.
- Every future claim will be backed by experiments.

Next Step:
Review fertility.py and reproduce the original results.

## Investigation Step 1 – Reproducing the Original Results

Objective:
Run the original evaluation script without modifications to establish a baseline.

Reason:
Future changes can only be evaluated if the original behaviour is known.

Status:
In Progress.

## Investigation Step 2 – Reproduce Original Benchmark

### Question

Can the benchmark reported by the previous intern be reproduced using the provided script and sample corpora?

### Hypothesis

Running the original script without modifications should reproduce the benchmark values reported in REPORT_v0.md.

### Procedure

- No source code modifications were made.
- Used the provided English and Hindi sample corpora.
- Used the GPT-2 tokenizer.

Command:

```bash
python fertility.py \
    --corpus eng=corpus_sample/eng_sample.txt \
    --corpus hin=corpus_sample/hin_sample.txt \
    --tokenizer gpt2
```

### Result

| Language | Fertility (tok/word) | Tokens/Character |
|----------|----------------------:|-----------------:|
| English | 1.27 | 0.226 |
| Hindi | 7.45 | 1.579 |

Relative fertility:

Hindi is **5.89×** the fertility of English.

### Conclusion

The original benchmark is reproducible using the supplied script and sample data. Future experiments will use these values as the baseline for comparison.

## Experiment 1 – Sentence Average vs Corpus Average

### Question

Does averaging fertility per sentence produce different benchmark values than computing fertility over the entire corpus?

### Hypothesis

If sentence lengths vary, averaging sentence-level fertility may introduce bias.

### Method

Copied the original script and modified only the aggregation logic.

Original:
Average of sentence-level fertility.

Modified:
Total tokens divided by total words across the corpus.

No other changes were made.

### Results

| Metric | Original | Modified |
|--------|---------:|---------:|
| English Fertility | 1.27 | 1.25 |
| Hindi Fertility | 7.45 | 7.40 |
| Hindi/English Ratio | 5.89× | 5.91× |

### Conclusion

The aggregation strategy changes the reported values, but the effect is small on the supplied sample corpus.

This suggests that sentence-level averaging is not the primary reason for the large English–Hindi difference observed in the benchmark.

## Experiment 2 – Effect of Lowercasing

### Question

Does converting all text to lowercase influence the tokenizer fertility comparison?

### Hypothesis

Lowercasing may affect English while having little or no effect on Indic languages because most Indic scripts do not distinguish uppercase and lowercase.

### Method

A copy of the original benchmark script was created.

Only the `line.lower()` preprocessing step was removed.

All other logic, tokenizer settings and corpus files remained unchanged.

### Results

| Metric | Original | Without Lowercasing |
|--------|---------:|--------------------:|
| English Fertility | 1.27 | 1.23 |
| Hindi Fertility | 7.45 | 7.45 |
| Hindi/English Ratio | 5.89× | 6.06× |

### Conclusion

Removing lowercasing affected the English benchmark but had no measurable effect on Hindi.

This demonstrates that the preprocessing step is language-dependent. While the numerical effect on this sample corpus is modest, it changes the reported cross-language fertility ratio and should therefore be documented when interpreting the benchmark.

## Experiment 3 – Comparing GPT-2 and XLM-Roberta

### Question

Does the observed English–Hindi tokenization disparity depend on the tokenizer used?

### Hypothesis

Since GPT-2 was primarily designed for English, a multilingual tokenizer such as XLM-Roberta should reduce the observed disparity.

### Method

Implemented a new comparison script (`compare_tokenizers.py`).

The script:
- Evaluates the same English and Hindi corpora.
- Uses two tokenizers:
  - GPT-2
  - XLM-Roberta
- Computes:
  - Tokens per word
  - Tokens per character

### Results

| Tokenizer | English (Tok/Word) | Hindi (Tok/Word) | Hindi / English |
|-----------|-------------------:|-----------------:|----------------:|
| GPT-2 | 1.23 | 7.52 | 6.11× |
| XLM-Roberta | 1.24 | 1.44 | 1.16× |

### Observations

The large disparity reported by the original benchmark is greatly reduced when using a multilingual tokenizer.

GPT-2 produces approximately six times more tokens per word for Hindi than English, whereas XLM-Roberta produces only a modest increase.

### Conclusion

The measured language disparity depends strongly on the tokenizer used.

Therefore, conclusions about multilingual tokenization quality should not be drawn from a single tokenizer alone.
# Experiment 5 – Building a Larger Multilingual Evaluation Corpus

## Objective

The provided sample corpus contains only around ten sentences, which is too small to draw reliable conclusions about tokenizer behaviour across languages. The objective of this experiment was to construct a larger multilingual evaluation corpus while keeping the evaluation methodology unchanged.

## Dataset

**Corpus:** FLORES-200

**Languages:**
- English
- Hindi
- Kannada
- Tamil

**Corpus Size:**
- 100 parallel sentences per language
- 400 sentences in total

## Why FLORES-200?

FLORES-200 is a professionally translated multilingual benchmark consisting of parallel sentences across many languages. Using a parallel corpus ensures that tokenizer statistics are compared on approximately equivalent semantic content rather than unrelated text.

## Preprocessing

- UTF-8 encoded text
- One sentence per line
- Original text preserved
- Empty lines ignored during analysis
- No additional normalization or cleaning performed

## Limitations

Although substantially larger than the provided sample corpus, 100 sentences per language is still a relatively small evaluation set. The corpus also represents only the domains included in FLORES-200. Therefore, the reported tokenizer statistics should be interpreted as comparative measurements for this corpus rather than universal estimates of tokenizer behaviour across all text.

# Experiment 6 – Tokenizer Comparison on FLORES-200

## Objective

Repeat the tokenizer comparison using the larger FLORES-200 corpus while keeping the analysis pipeline identical to the previous experiments.

## Method

The comparison script was updated to support multiple corpora using the `--corpus` command-line argument. The same implementation was executed on both the original sample corpus and the FLORES-200 corpus without changing the analysis logic.

Two tokenizers were evaluated:

- GPT-2
- XLM-Roberta

Three normalization metrics were computed:

- Tokens per Word
- Tokens per Character (Unicode code points)
- Tokens per UTF-8 Byte

## Results

### GPT-2

| Language | Tok/Word | Tok/Char | Tok/Byte |
|----------|---------:|---------:|---------:|
| English | 1.26 | 0.210 | 0.210 |
| Hindi | 7.72 | 1.515 | 0.592 |
| Kannada | 21.49 | 2.621 | 0.977 |
| Tamil | 24.07 | 2.691 | 0.993 |

### XLM-Roberta

| Language | Tok/Word | Tok/Char | Tok/Byte |
|----------|---------:|---------:|---------:|
| English | 1.40 | 0.235 | 0.234 |
| Hindi | 1.51 | 0.296 | 0.116 |
| Kannada | 2.51 | 0.306 | 0.114 |
| Tamil | 2.44 | 0.273 | 0.101 |

## Observations

Several important observations emerge from the larger multilingual corpus.

- GPT-2 produces substantially higher fertility for Indic languages than for English.
- Kannada and Tamil exhibit particularly high Tokens per Word values under GPT-2.
- XLM-Roberta produces much more balanced token counts across all four languages.
- Tokens per Byte also become considerably more consistent when using XLM-Roberta.

These results indicate that tokenizer vocabulary design has a much greater influence on fertility than language alone.

## Choosing the Routing Metric

The purpose of the denominator is to keep approximately the same quantity constant across languages.

- **Tokens per Word** depends on language-specific word segmentation.
- **Tokens per Character** removes whitespace dependence but still compares Unicode code points rather than displayed text or encoded size.
- **Tokens per UTF-8 Byte** measures tokenization relative to the encoded input processed by the tokenizer and therefore provides a more language-independent normalization.

For routing and cost estimation, **Tokens per UTF-8 Byte** is the most appropriate metric among those evaluated.

## Conclusion

The larger evaluation corpus confirms the trends observed using the sample corpus.

The experiments demonstrate that tokenizer selection has a much greater effect on fertility measurements than language alone. Therefore, multilingual routing and cost estimation should always be evaluated using the tokenizer intended for deployment.


#  Part B Capacity Reconciliation

## Goal

Answer the four capacity reconciliation questions using the provided
model specification and benchmark log.

---

## Initial hypothesis

Initially assumed that throughput should continue increasing as batch
size increases.

---

## Experiment 1

Calculated KV-cache memory per token using:

Layers × 2 × KV Heads × Head Dimension × FP16 bytes

Result:

114,688 bytes/token.

Estimated approximately 45 concurrent 4096-token sequences.

---

## Observation

The benchmark began preempting sequences between batch sizes 24 and 32,
despite the theoretical estimate of ~45 sequences.

---

## Revision

Realized that runtime memory, allocator overhead, and scheduler metadata
reduce practical capacity below the theoretical maximum.

---

## Experiment 2

Examined the long-context benchmark rows.

Found that throughput peaks at batch size 24 and decreases afterwards.

Observed:

- kv_cache_util increases to 0.97
- preempted_seqs increases from 0 → 7 → 23

Conclusion:

Scheduler preemption caused by KV-cache saturation reduces throughput.

---

## Experiment 3

Verified whether reported_tok_s represented generation throughput.

Computed:

(24 × (3584 + 512)) / wall_clock

Result exactly matched reported_tok_s.

Dead end:

Initially assumed reported_tok_s represented generated tokens per second.

Revision:

Determined that it actually counts prompt + generated tokens.

Computed generation goodput independently using:

1. generated_tokens / wall_clock

2. reported_tok_s × (generated_tokens / total_tokens)

Both produced approximately 200.9 generated tok/s.