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