#!/usr/bin/python3

import sys
from subprocess import check_output, run

# Цвета
green_color = "\033[1;32m"
red_color = "\033[1;31m"
yellow_color = "\033[1;33m"
color_off = "\033[0m"

# Получаем ID Docker контейнера backend
backend_docker_id = check_output(['docker', 'ps', '--filter', 'name=djuxt_dev_backend', '-q']).decode('utf-8').strip()

# Проверяем существование
if not backend_docker_id:
    print(f"{red_color} pre-push: Не найден Docker контейнер backend {color_off}")
    sys.exit(1)

# Получаем ID Docker контейнера frontend
frontend_docker_id = check_output(['docker', 'ps', '--filter', 'name=djuxt_dev_frontend', '-q']).decode('utf-8').strip()

# Проверяем существование
if not frontend_docker_id:
    print(f"{red_color} pre-push: Не найден Docker контейнер frontend {color_off}")
    sys.exit(1)

print(f"{green_color} pre-push: Контейнер Backend для проверки: {backend_docker_id} {color_off}")
print(f"{green_color} pre-push: Контейнер Frontend для проверки: {frontend_docker_id} {color_off}")

# Проверяем backend
# ruff
print("pre-push: Backend: запускаем ruff check")
backend_ruff_output = run(['docker', 'exec', backend_docker_id, 'ruff', 'check'])

if backend_ruff_output.returncode != 0:
    print(f"{red_color} pre-push: Backend: ruff check не прошел {color_off}")
    sys.exit(1)

print("pre-push: Backend: ruff check успешно!")

# flake8
print("pre-push: Backend: запускаем flake8 --config .flake8 ./")
backend_flake8_output = run(['docker', 'exec', backend_docker_id, 'flake8', '--config', '.flake8', './'])

if backend_flake8_output.returncode != 0:
    print(f"{red_color} pre-push: Backend: flake8 --config .flake8 ./ не прошел {color_off}")
    sys.exit(1)

print("pre-push: Backend: flake8 --config .flake8 ./ успешно!")
print(f"{green_color} pre-push: Backend: все проверки успешно! {color_off}")

# Проверяем frontend
# docker exec -it 2933c6ab995a npm run lint
frontend_eslint_output = run(['docker', 'exec', frontend_docker_id, 'npm', 'run', 'lint'])

if frontend_eslint_output.returncode != 0:
    print(f"{red_color} pre-push: Frontend: npm run lint не прошел {color_off}")
    sys.exit(1)

print("pre-push: Frontend: npm run lint успешно!")
print(f"{green_color} pre-push: Frontend: все проверки успешно! {color_off}")

print(f"{green_color} pre-push: Можно отправлять! {color_off}")
sys.exit(0)