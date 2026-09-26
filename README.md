# Chinese Dance Text Analysis

A small Python pipeline that segments Chinese-language dance instruction texts into words and computes corpus-wide and per-document word frequencies.

I built it as an undergraduate research assistant on a faculty-led digital humanities project at Dickinson College (Summer 2026, advisor: Prof. Xiaolu Wang). The corpus was about 160 mid-20th-century Chinese group and children's dance publications. We digitized the paper originals, converted them from scanned PDFs into editable text, and compiled them into a spreadsheet with one row per work. These scripts turn that spreadsheet into word-frequency tables for analysis.

## Pipeline

```
source spreadsheet (one row per work, full text in column 文章提取)
        │
        ▼
fenci_batch.py   →  <name>_segmented.xlsx     (adds tokenized text + token counts)
        │
        ▼
cipin_batch.py   →  <name>_词频统计.xlsx       (frequency tables)
```

### 1. `fenci_batch.py`: word segmentation

- Reads the first sheet of an Excel or CSV file (UTF-8 or GB18030) and uses the text column `文章提取`.
- Segments each text with [jieba](https://github.com/fxsjy/jieba) in precise mode.
- Adds a domain dictionary of dance and movement terms so jieba keeps them as single words. Examples: 左脚 (left foot), 前半拍 (first half-beat), 小节 (measure), 集体舞 (group dance), 圆场步 (circling step). You can add more terms, one per line, in an optional `custom_words.txt` next to the script.
- Drops punctuation and whitespace tokens. Numbers are kept by default; set `KEEP_NUMBERS = False` to remove them.
- Writes three new columns: `words` (slash-separated for reading), `word_list` (space-separated, used by the next step) and `token_count`.

### 2. `cipin_batch.py`: word frequency

Reads the segmented file and writes a workbook with three sheets:

| Sheet | Contents |
|---|---|
| 总词频 (overall frequency) | Every word with its rank, total count, number of documents it appears in, document coverage rate, and share of all tokens |
| Top100 | The first 100 rows of the table above |
| 各文献统计 (per-document stats) | For each work: total tokens, unique words, and its 10 most frequent words |

## Usage

```bash
pip install -r requirements.txt
python fenci_batch.py      # a file picker opens: choose the source spreadsheet
python cipin_batch.py      # choose the *_segmented.xlsx file produced above
```

Both scripts use a Tkinter file dialog, so they also run from IDLE with no command-line arguments. Output files are saved next to the input file.

To try the pipeline, `sample/sample_input.csv` has two short made-up texts in the expected format.

## Data

The research corpus and outputs are not included in this repository. They belong to the research project.

## Tech

Python · pandas · jieba · openpyxl · Tkinter
