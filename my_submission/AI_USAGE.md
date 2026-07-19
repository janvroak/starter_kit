# AI Usage

## Where AI Helped

ChatGPT was used throughout this assignment as a technical assistant rather than as a source of experimental evidence.

Specifically, AI was used to:

- Clarify the assignment requirements.
- Explain tokenizer concepts and multilingual evaluation metrics.
- Discuss possible hypotheses before implementing experiments.
- Suggest ways to isolate suspected issues in `fertility.py`.
- Review the design of the comparison script and suggest refactoring to support multiple corpora and tokenizers.
- Improve the organization and wording of the notebook and written report.

All AI-generated code suggestions were manually reviewed, adapted where necessary, executed locally, and verified before being included in the submission.

---

## Where AI Was Incorrect or Misleading

AI initially suggested loading FLORES-200 using a Hugging Face configuration that failed because authenticated access had not yet been configured. It also suggested switching to the OPUS dataset after the initial failure.

Rather than accepting these suggestions, the issue was investigated manually by checking the dataset page, accepting the required access terms, authenticating with Hugging Face, and rerunning the corpus preparation successfully. FLORES-200 was therefore retained because it matched the assignment recommendation and became accessible after authentication.

AI also proposed several potential issues in `fertility.py`. Each proposed issue was treated as a hypothesis rather than a confirmed bug. Experiments were performed to verify or reject these hypotheses. For example, whitespace splitting initially appeared suspicious, but testing on the provided corpus showed that it did not affect the reported results and therefore was not reported as a bug.

These experiences reinforced that AI suggestions should be treated as starting points for investigation rather than ground truth. Every experimental result and conclusion reported in this submission is based on code executed locally and verified manually.