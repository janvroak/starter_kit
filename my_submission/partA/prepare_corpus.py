from datasets import load_dataset
from pathlib import Path

# -------------------------------------------------------
# Load FLORES-200 validation split
# -------------------------------------------------------

dataset = load_dataset(
    "facebook/flores",
    "all",
    split="dev"
)

# -------------------------------------------------------
# Languages to extract
# -------------------------------------------------------

LANGUAGES = {
    "eng": "sentence_eng_Latn",
    "hin": "sentence_hin_Deva",
    "kan": "sentence_kan_Knda",
    "tam": "sentence_tam_Taml",
}

# -------------------------------------------------------
# Output directory
# -------------------------------------------------------

OUTPUT_DIR = Path("my_submission/partA/corpus")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NUM_SENTENCES = 100

# -------------------------------------------------------
# Save first 100 sentences for each language
# -------------------------------------------------------

for short_name, column in LANGUAGES.items():

    output_file = OUTPUT_DIR / f"{short_name}.txt"

    with output_file.open("w", encoding="utf-8") as f:

        for row in dataset.select(range(NUM_SENTENCES)):
            sentence = str(row[column]).strip()
            f.write(sentence + "\n")

print("Corpus created successfully!")