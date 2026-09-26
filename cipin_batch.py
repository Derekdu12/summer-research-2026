# -*- coding: utf-8 -*-
"""
批量词频统计脚本（IDLE版）

运行前：
先使用 fenci_batch.py 生成：
原文件名_segmented.xlsx

运行后：
1. 选择已经分词好的 Excel
2. 读取 word_list 列
3. 统计全语料词频
4. 统计每个词出现于多少篇文献
5. 输出：原文件名_词频统计.xlsx

输出 Sheet：
- 总词频
- Top100
- 各文献统计
"""

import os
import pandas as pd
from collections import Counter
from tkinter import Tk, filedialog

WORD_COL = "word_list"


def main():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="选择已经分词好的 Excel",
        filetypes=[
            ("Excel files", "*.xlsx *.xls"),
            ("CSV files", "*.csv"),
            ("All files", "*.*"),
        ]
    )

    root.destroy()

    if not file_path:
        print("没有选择文件。")
        return

    print("\n选择的文件：")
    print(file_path)

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    else:
        df = pd.read_excel(file_path)

    print("记录数：", len(df))

    if WORD_COL not in df.columns:
        print("\n错误：找不到 word_list 列。")
        print("当前列名：")
        print(list(df.columns))
        return

    total_counter = Counter()
    document_counter = Counter()
    document_rows = []

    for i, row in df.iterrows():
        cell = row.get(WORD_COL, "")

        if pd.isna(cell):
            words = []
        else:
            words = str(cell).split()

        total_counter.update(words)
        document_counter.update(set(words))

        title = row["名称"] if "名称" in df.columns else f"第{i+1}篇"
        counter = Counter(words)

        top10 = "；".join(
            f"{word}({freq})"
            for word, freq in counter.most_common(10)
        )

        document_rows.append({
            "名称": title,
            "总词数": len(words),
            "不重复词数": len(counter),
            "Top10": top10,
        })

    total_tokens = sum(total_counter.values())
    unique_words = len(total_counter)
    total_docs = len(df)

    rows = []

    for rank, (word, freq) in enumerate(total_counter.most_common(), start=1):
        doc_freq = document_counter[word]

        rows.append({
            "排名": rank,
            "词语": word,
            "词频": freq,
            "出现文献数": doc_freq,
            "文献覆盖率": doc_freq / total_docs if total_docs else 0,
            "占总词数比例": freq / total_tokens if total_tokens else 0,
        })

    freq_df = pd.DataFrame(rows)
    document_df = pd.DataFrame(document_rows)

    base = os.path.splitext(file_path)[0]

    if base.endswith("_segmented"):
        base = base[:-10]

    output_path = base + "_词频统计.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        freq_df.to_excel(writer, sheet_name="总词频", index=False)
        freq_df.head(100).to_excel(writer, sheet_name="Top100", index=False)
        document_df.to_excel(writer, sheet_name="各文献统计", index=False)

    print("\n==============================")
    print("词频统计完成")
    print("==============================")

    print("文献数：", total_docs)
    print("总词数：", total_tokens)
    print("不重复词数：", unique_words)

    print("\nTop 30 高频词：")
    print(freq_df.head(30).to_string(index=False))

    print("\n输出文件：")
    print(output_path)


if __name__ == "__main__":
    main()
