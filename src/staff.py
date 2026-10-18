"""Первые запросы к справочнику сотрудников (data/agents.csv).

Запуск из корня репозитория: python3 src/staff.py
"""

import csv
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE agents (id TEXT, login TEXT, team TEXT, hired_at TEXT)")

with open("data/agents.csv", encoding="utf-8") as f:
    rows = [(r["id"], r["login"], r["team"], r["hired_at"]) for r in csv.DictReader(f)]
con.executemany("INSERT INTO agents VALUES (?, ?, ?, ?)", rows)

print("1. Первые три сотрудника")
for row in con.execute("SELECT login, team FROM agents LIMIT 3"):
    print(row)

print("2. Количество строк в справочнике")
print(con.execute("SELECT COUNT(*) FROM agents").fetchone())

print("3. Три сотрудника, нанятых раньше всех")
for row in con.execute("SELECT login, hired_at FROM agents ORDER BY hired_at LIMIT 3"):
    print(row)

print("4. Количество строк по сменам")
for row in con.execute("SELECT team, COUNT(*) FROM agents GROUP BY team ORDER BY team"):
    print(row)

print("5. Сотрудники, нанятые в 2025 году")
for row in con.execute("SELECT login, hired_at FROM agents WHERE hired_at LIKE '2025%'"):
    print(row)
