#!/usr/bin/python3

import sys
import re
from subprocess import check_output

# Цвета
green_color = "\033[1;32m"
red_color = "\033[1;31m"
yellow_color = "\033[1;33m"
color_off = "\033[0m"

# Название файла с именем коммита
commit_msg_filepath = sys.argv[1]

# Получаем название ветки для проверки номера ветки и ишью
branch = check_output(['git', 'symbolic-ref', '--short', 'HEAD']).decode('utf-8').strip()
print(f"{yellow_color} commit-msg: Проверяем имя коммита на ветке '{branch} {color_off}")

issue_number_on_issue_branch = re.match('issue[-\/](\d+)', branch)
issue_number_on_feature_branch = re.match('feature[-\/](\d+)', branch)

issue_number = None

if issue_number_on_issue_branch:
    issue_number = issue_number_on_issue_branch.group(1)

if issue_number_on_feature_branch:
    issue_number = issue_number_on_feature_branch.group(1)

if not issue_number:
    print(f"{red_color} commit-msg: Не найдено номера ишью на ветке '{branch}' {color_off}")
    sys.exit(1)

print(f"{green_color} commit-msg: Найден номер ишью '{issue_number}' {color_off}")

required_issue_message = f"#{issue_number}"

with open(commit_msg_filepath, 'r') as f:
    commit_msg = f.read()

    if required_issue_message not in commit_msg:
        print(f"{red_color} commit-msg: Не найдено '{required_issue_message}' в коммите {color_off}")
        sys.exit(1)

    print(f"{green_color} commit-msg: Найдено '{required_issue_message}' в коммите {color_off}")
    sys.exit(0)

print(f"{red_color} commit-msg: Ошибка при открытии сообщения коммита {color_off}")
sys.exit(1)
