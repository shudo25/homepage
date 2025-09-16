"""
participants.py
"""

import csv
import re

members_file = "メンバー全員.csv"
densuke_file = "伝助.csv"
participants_file = "参加者.csv"
non_participants_file = "非参加者.csv"

def remove_spaces(s):
    # 全角・半角スペースを除去
    return re.sub(r'[\s\u3000]', '', s)

# 伝助.csvから参加者リストを作成
with open(densuke_file, encoding="utf-8") as f:
    reader = csv.reader(f)
    names_row = next(reader)      # 1行目: 氏名
    statuses_row = next(reader)   # 2行目: 参加可否

    densuke_names = [remove_spaces(name) for name in names_row[1:]]
    statuses = statuses_row[1:]

    participants = set()
    non_participants = set()
    for name, status in zip(densuke_names, statuses):
        if status in ["○", "△"]:
            participants.add(name)
        elif status == "×":
            non_participants.add(name)

print(f"参加人数: {len(participants)}")
print(f"非参加人数: {len(non_participants)}")

# メンバー全員.csvを読み込んで振り分け（空白除去で判定）
with open(members_file, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    member_rows = list(reader)
    fieldnames = reader.fieldnames

participants_rows = []
non_participants_rows = []

def match_status(member_name):
    member_name_nospace = remove_spaces(member_name)
    for p_name in participants:
        if p_name in member_name_nospace:
            return "participant"
    for np_name in non_participants:
        if np_name in member_name_nospace:
            return "non_participant"
    return "non_participant"  # 伝助.csvに情報がない場合は非参加者扱い

for row in member_rows:
    name = row["氏名"]
    status = match_status(name)
    if status == "participant":
        participants_rows.append(row)
    else:
        non_participants_rows.append(row)

# 参加者.csvに出力
with open(participants_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(participants_rows)

# 非参加者.csvに出力
with open(non_participants_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(non_participants_rows)