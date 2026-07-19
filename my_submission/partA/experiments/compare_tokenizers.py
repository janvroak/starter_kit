from pathlib import Path
import argparse
import csv

import tiktoken
from transformers import AutoTokenizer


# -------------------------------------------------------
# Command Line Arguments
# -------------------------------------------------------

parser = argparse.ArgumentParser(
    description="Compare tokenizer statistics on multilingual corpora."
)

parser.add_argument(
    "--corpus",
    choices=["sample", "flores"],
    default="sample",
    help="Corpus to evaluate.",
)

parser.add_argument(
    "--tokenizer",
    choices=["gpt2", "xlmr", "both"],
    default="both",
    help="Tokenizer to use.",
)

args = parser.parse_args()


# -------------------------------------------------------
# Corpus Selection
# -------------------------------------------------------

def get_languages(corpus):

    if corpus == "sample":
        return {
            "English": "starter_kit/corpus_sample/eng_sample.txt",
            "Hindi": "starter_kit/corpus_sample/hin_sample.txt",
        }

    elif corpus == "flores":
        return {
            "English": "my_submission/partA/corpus/eng.txt",
            "Hindi": "my_submission/partA/corpus/hin.txt",
            "Kannada": "my_submission/partA/corpus/kan.txt",
            "Tamil": "my_submission/partA/corpus/tam.txt",
        }

    raise ValueError(f"Unknown corpus: {corpus}")


languages = get_languages(args.corpus)


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
        add_special_tokens=False,
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
    total_bytes = 0

    for line in lines:

        line = line.strip()

        if not line:
            continue

        tokens = encode(line)

        total_tokens += len(tokens)
        total_words += len(line.split())
        total_chars += len(line)
        total_bytes += len(line.encode("utf-8"))

    return {
        "tokens": total_tokens,
        "words": total_words,
        "chars": total_chars,
        "bytes": total_bytes,
        "tok_per_word": total_tokens / total_words,
        "tok_per_char": total_tokens / total_chars,
        "tok_per_byte": total_tokens / total_bytes,
    }


# -------------------------------------------------------
# Tokenizer Selection
# -------------------------------------------------------

available_tokenizers = {
    "GPT-2": encode_gpt2,
    "XLM-Roberta": encode_xlmr,
}

if args.tokenizer == "gpt2":
    tokenizers = {
        "GPT-2": encode_gpt2
    }

elif args.tokenizer == "xlmr":
    tokenizers = {
        "XLM-Roberta": encode_xlmr
    }

else:
    tokenizers = available_tokenizers


# -------------------------------------------------------
# Results Directory
# -------------------------------------------------------

results_dir = Path("my_submission/partA/results")
results_dir.mkdir(parents=True, exist_ok=True)

comparison_rows = []


# -------------------------------------------------------
# Run Comparison
# -------------------------------------------------------

print(f"\nCorpus : {args.corpus}")

for tokenizer_name, tokenizer_fn in tokenizers.items():

    print("\n" + "=" * 90)
    print(f"TOKENIZER : {tokenizer_name}")
    print("=" * 90)

    print(
        f"{'Language':<12}"
        f"{'Tokens':>10}"
        f"{'Words':>10}"
        f"{'Chars':>10}"
        f"{'Bytes':>10}"
        f"{'Tok/Word':>12}"
        f"{'Tok/Char':>12}"
        f"{'Tok/Byte':>12}"
    )

    print("-" * 90)

    rows = []

    for language, path in languages.items():

        lines = read_file(path)

        result = analyze(lines, tokenizer_fn)

        print(
            f"{language:<12}"
            f"{result['tokens']:>10}"
            f"{result['words']:>10}"
            f"{result['chars']:>10}"
            f"{result['bytes']:>10}"
            f"{result['tok_per_word']:>12.2f}"
            f"{result['tok_per_char']:>12.3f}"
            f"{result['tok_per_byte']:>12.3f}"
        )

        row = {
            "Language": language,
            "Tokens": result["tokens"],
            "Words": result["words"],
            "Chars": result["chars"],
            "Bytes": result["bytes"],
            "Tok/Word": round(result["tok_per_word"], 2),
            "Tok/Char": round(result["tok_per_char"], 3),
            "Tok/Byte": round(result["tok_per_byte"], 3),
        }

        rows.append(row)

        comparison_rows.append({
            "Tokenizer": tokenizer_name,
            **row
        })

    filename = (
        "gpt2_results.csv"
        if tokenizer_name == "GPT-2"
        else "xlmr_results.csv"
    )

    with open(results_dir / filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


with open(results_dir / "comparison_table.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=comparison_rows[0].keys())
    writer.writeheader()
    writer.writerows(comparison_rows)


print("\n" + "=" * 90)
print("CSV files successfully saved!")
print(results_dir.resolve())
print("=" * 90)