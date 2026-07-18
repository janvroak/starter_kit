from pathlib import Path

import tiktoken
from transformers import AutoTokenizer


# -------------------------------------------------------
# Load Tokenizers
# -------------------------------------------------------

gpt2 = tiktoken.get_encoding("gpt2")

xlmr = AutoTokenizer.from_pretrained(
    "FacebookAI/xlm-roberta-base"
)


# -------------------------------------------------------
# Tokenizer Wrapper Functions
# -------------------------------------------------------

def encode_gpt2(text):
    return gpt2.encode(text)


def encode_xlmr(text):
    return xlmr.encode(
        text,
        add_special_tokens=False
    )


# -------------------------------------------------------
# Read Corpus
# -------------------------------------------------------

def read_file(path):
    return Path(path).read_text(
        encoding="utf-8"
    ).splitlines()


# -------------------------------------------------------
# Metric Calculation
# -------------------------------------------------------

def analyze(lines, encode):

    total_tokens = 0
    total_words = 0
    total_chars = 0

    for line in lines:

        line = line.strip()

        if not line:
            continue

        tokens = encode(line)

        total_tokens += len(tokens)
        total_words += len(line.split())
        total_chars += len(line)

    return {
        "tokens": total_tokens,
        "words": total_words,
        "chars": total_chars,
        "tok_per_word": total_tokens / total_words,
        "tok_per_char": total_tokens / total_chars,
    }


# -------------------------------------------------------
# Corpus Files
# -------------------------------------------------------

languages = {
    "English": "starter_kit/corpus_sample/eng_sample.txt",
    "Hindi": "starter_kit/corpus_sample/hin_sample.txt",
}


# -------------------------------------------------------
# Run Comparison
# -------------------------------------------------------

tokenizers = {
    "GPT-2": encode_gpt2,
    "XLM-Roberta": encode_xlmr,
}


for tokenizer_name, tokenizer_fn in tokenizers.items():

    print("\n" + "=" * 60)
    print(f"TOKENIZER : {tokenizer_name}")
    print("=" * 60)

    print(
        f"{'Language':<12}"
        f"{'Tokens':>10}"
        f"{'Words':>10}"
        f"{'Chars':>10}"
        f"{'Tok/Word':>12}"
        f"{'Tok/Char':>12}"
    )

    print("-" * 60)

    for language, path in languages.items():

        lines = read_file(path)

        result = analyze(lines, tokenizer_fn)

        print(
            f"{language:<12}"
            f"{result['tokens']:>10}"
            f"{result['words']:>10}"
            f"{result['chars']:>10}"
            f"{result['tok_per_word']:>12.2f}"
            f"{result['tok_per_char']:>12.3f}"
        )