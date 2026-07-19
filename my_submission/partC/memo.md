# Decision Memo

## Recommendation

I recommend **Option (b): deploy a small (≤1B parameter) inference-time rewriter model after the main assistant model.** This approach provides better control over conversational style than prompt engineering while avoiding the cost and schedule risk of fine-tuning the main model.

---

## Assumptions

- The main assistant already produces factually correct responses.
- Only the writing style (formal vs conversational) needs improvement.
- Synthetic style-transfer data can be generated locally without paid APIs.
- The rewriter model is significantly cheaper to train than the main model.
- Reviewer time is limited to Hindi and Kannada.

---

## Back-of-the-envelope arithmetic

### Reviewer capacity

One reviewer:

10 hours/week × 2 weeks = **20 hours**

Assuming approximately 2 minutes per example:

20 × 60 / 2 = **600 reviewed examples**

These reviews will be used for Hindi and Kannada validation rather than manually labeling all six languages.

### Training data

Generate approximately **50,000 synthetic style-transfer pairs** locally.

Use approximately:

- 45,000 for training
- 5,000 for validation

### Compute

A ≤1B parameter model can comfortably be fine-tuned on one A100 80GB within the available two-week budget, leaving time for evaluation and iteration.

### Serving cost

The rewriter adds one additional inference pass, increasing latency slightly but requiring much less compute than running another large language model.

---

## Success Metric

On a held-out evaluation set:

- At least **85%** of Hindi and Kannada responses should be judged by the reviewer as sounding natural and conversational.
- Less than **2%** of responses should introduce factual changes compared with the original model output.

---

## Kill Criterion

After the first week, if reviewer evaluation shows **less than 70% conversational preference** or factual errors exceed **5%**, stop development of the rewriter and fall back to prompt engineering for launch.

---

## Day 1 Experiment

Create a small evaluation set of approximately **100 responses**.

Compare:

1. Original model
2. Prompt-only rewriting
3. Small rewriter model

Have the reviewer score Hindi and Kannada outputs for:

- Conversational tone
- Meaning preservation
- Overall preference

Use these results to decide whether training the rewriter is justified before investing further effort.