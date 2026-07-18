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