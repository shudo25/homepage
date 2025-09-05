"""

"""
import re

address_line_re = re.compile(r"^\s*(\d+)\s+(.+)\s+(\d{3}-\d{4})\s(.*)\s\d{3,4}-")

output_lines = []

with open("members.txt", "r", encoding='utf-8') as file:
    for line in file:
        match = address_line_re.match(line)
        if match:
            member_id = match.group(1)
            member_name = match.group(2)
            post_code = match.group(3)
            address = match.group(4)
            print(f"ID: {member_id}, Name: {member_name}, Post Code: {post_code}, Address: {address}")
            output_lines.append([member_id, member_name, post_code, address])

with open("members.csv", "w", encoding='cp932') as file:
    for line in output_lines:
        file.write(",".join(line) + "\n")