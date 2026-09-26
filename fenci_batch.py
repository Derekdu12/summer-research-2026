# -*- coding: utf-8 -*-
"""
批量分词脚本（IDLE版）

运行后：
1. 选择原始 Excel / CSV
2. 读取“文章提取”列
3. 对全部文献进行 jieba 分词
4. 输出：原文件名_segmented.xlsx

输出新增列：
- words
- word_list
- token_count
"""

import os
import re
import pandas as pd
import jieba
from tkinter import Tk, filedialog

TEXT_COL = "文章提取"
KEEP_NUMBERS = True

CUSTOM_WORDS = [
    "左脚", "右脚", "左手", "右手", "双手", "双脚",
    "左膝", "右膝", "左臂", "右臂", "左腿", "右腿",
    "向前", "向后", "向左", "向右",
    "左前方", "右前方", "左后方", "右后方",
    "前半拍", "后半拍", "小节", "原地",
    "脚掌", "脚跟", "脚尖",
    "踢踏舞", "集体舞", "儿童歌舞", "学校舞蹈", "体育舞蹈",
    "唱歌游戏", "唱游", "土风舞", "形意舞", "秧歌",
    "红绸舞", "圆场步", "大头娃娃", "走马灯", "瞎子摸人",
    "少年宫", "红领巾", "解放军叔叔",
]

KEEP = re.compile(r"[\u4e00-\u9fffA-Za-z0-9]")


def load_custom_words():
    for word in CUSTOM_WORDS:
        jieba.add_word(word)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    custom_file = os.path.join(script_dir, "custom_words.txt")

    if os.path.exists(custom_file):
        jieba.load_userdict(custom_file)
        print("已加载自定义词典：", custom_file)


def segment(text):
    if pd.isna(text):
        return []

    text = str(text).strip()
    if not text:
        return []

    words = jieba.lcut(text, cut_all=False)
    result = []

    for word in words:
        word = word.strip()

        if not word:
            continue

        if not KEEP.search(word):
            continue

        if not KEEP_NUMBERS and word.isdigit():
            continue

        result.append(word)

    return result


def load_file(path):
    ext = os.path.splitext(path)[1].lower()

    if ext in [".xlsx", ".xlsm"]:
        return pd.read_excel(path, sheet_name=0, engine="openpyxl")

    if ext == ".xls":
        return pd.read_excel(path, sheet_name=0)

    if ext == ".csv":
        try:
            return pd.read_csv(path, encoding="utf-8-sig")
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="gb18030")

    raise ValueError("只支持 .xlsx、.xls、.xlsm、.csv")


def main():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="选择原始舞蹈 Excel / CSV",
        filetypes=[
            ("Excel files", "*.xlsx *.xls *.xlsm"),
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

    df = load_file(file_path)

    print("\n原始记录数：", len(df))
    print("列名：", list(df.columns))

    if TEXT_COL not in df.columns:
        print("\n错误：找不到正文列：", TEXT_COL)
        return

    load_custom_words()

    print("\n开始批量分词……")

    segmented_results = []
    total_rows = len(df)

    for i, text in enumerate(df[TEXT_COL], start=1):
        words = segment(text)
        segmented_results.append(words)

        if i % 10 == 0 or i == total_rows:
            print(f"已完成 {i} / {total_rows} 篇")

    df["words"] = [" / ".join(words) for words in segmented_results]
    df["word_list"] = [" ".join(words) for words in segmented_results]
    df["token_count"] = [len(words) for words in segmented_results]

    base = os.path.splitext(file_path)[0]
    output_path = base + "_segmented.xlsx"

    df.to_excel(output_path, index=False, engine="openpyxl")

    print("\n==============================")
    print("分词完成")
    print("==============================")
    print("处理记录数：", len(df))
    print("输出文件：")
    print(output_path)


if __name__ == "__main__":
    main()
