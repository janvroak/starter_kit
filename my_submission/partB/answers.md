# Part B - Capacity Reconciliation

---

## B1. Capacity Reconciliation

### (a) KV-cache bytes per token

For each token, each transformer layer stores both a Key and a Value.

Formula:

KV bytes/token =
Layers × 2 × KV Heads × Head Dimension × Bytes/value

Substituting the model specification:

28 × 2 × 8 × 128 × 2
= 114,688 bytes/token

Therefore,

**KV Cache = 114,688 bytes/token (≈112 KB/token)**

### (b) Maximum concurrent 4096-token sequences

Usable GPU memory:

24 GB × 0.92 = 22.08 GB

Available for KV cache:

22.08 − 1.6 = 20.48 GB

Memory required for one sequence:

4096 × 114,688
= 469,762,048 bytes
≈448 MB

Maximum concurrent sequences:

20.48 GB / 448 MB ≈ 45

Therefore, the theoretical capacity is approximately **45 concurrent 4096-token sequences**.

### Comparison with benchmark

The benchmark shows:

| Batch | KV Util | Preempted |
|------:|---------:|----------:|
|24|0.93|0|
|32|0.97|7|
|48|0.97|23|

Although the theoretical calculation predicts around 45 sequences, the practical limit is reached between batches 24 and 32 because runtime memory, allocator overhead, fragmentation, and scheduler metadata reduce the usable KV-cache capacity.

---

## B2. Throughput Anomaly

### Observation

For the long-context workload (prompt length = 3584), throughput increases up to batch size 24 but decreases afterwards.

| Batch | Reported tok/s | KV Util | Preempted |
|------:|---------------:|---------:|----------:|
|24|1607.4|0.93|0|
|32|1384.0|0.97|7|
|48|1298.5|0.97|23|

### Explanation

The KV cache becomes almost full at batch 24. At batches 32 and 48, the scheduler begins preempting sequences because KV-cache utilization reaches 97%. Scheduler overhead and memory pressure reduce effective throughput.

### Proposed change

Limit long-context workloads to a maximum batch size of 24 (or increase KV-cache capacity).

Expected effect:

Throughput should increase from approximately 1384 tok/s to 1607 tok/s (about **16% improvement**) while eliminating scheduler preemption.

---

## B3. Correct Goodput

The report incorrectly interpreted **reported_tok_s** as generation throughput.

However, reported_tok_s includes both prompt tokens and generated tokens.

### Method 1

Generated tokens:

24 × 512 = 12,288

Goodput:

12,288 / 61.16

= 200.9 generated tok/s

### Method 2

Only one-eighth of the processed tokens are generated.

Goodput:

1607.4 × (512 / 4096)

= 200.9 generated tok/s

### Correct conclusion

Longer prompts do not inherently provide better generation throughput. The actual generation goodput for the batch-24 long-context run is approximately **201 generated tokens/s**, and throughput decreases beyond batch size 24 because KV-cache saturation causes scheduler preemption.

---

## B4. Production Metric

To confirm the mechanism identified in B2, I would monitor **preempted_seqs**.

This counter should remain close to zero while the workload fits comfortably in GPU memory and increase once KV-cache saturation forces the scheduler to preempt requests. In the benchmark, the value increases from 0 at batch 24 to 7 at batch 32 and 23 at batch 48, matching the observed drop in throughput.
