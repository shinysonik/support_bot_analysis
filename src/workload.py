"""Сколько людей на первой линии и сколько времени уходит на обращение.

Запуск из корня репозитория: python3 src/workload.py
"""

import statistics

from db import connect
from sql_functions import Median, unicode_lower


def main():
    con = connect()
    con.create_function("unicode_lower", 1, unicode_lower)
    con.create_aggregate("MEDIAN", 1, Median)

    print("1. Строк в справочнике и разных людей")
    print(con.execute("SELECT COUNT(*), COUNT(DISTINCT login) FROM agents").fetchone())

    print("1a. Какая строка лишняя")
    print(con.execute("""
        SELECT MIN(id), login, team, hired_at, COUNT(*)
        FROM agents
        GROUP BY login, team, hired_at
        HAVING COUNT(*) > 1
    """).fetchone())

    print("2. Смены, где меньше 6 человек")
    for row in con.execute("""
        SELECT team, COUNT(DISTINCT login)
        FROM agents
        GROUP BY team
        HAVING COUNT(DISTINCT login) < 6
    """):
        print(row)

    print("3. Каналы в сырой выгрузке: встроенный lower()")
    for row in con.execute("""
        SELECT lower(channel), COUNT(*)
        FROM tickets
        GROUP BY lower(channel)
        ORDER BY 1
    """):
        print(row)

    print("3a. Каналы в сырой выгрузке: unicode_lower()")
    for row in con.execute("""
        SELECT unicode_lower(channel), COUNT(*)
        FROM tickets
        GROUP BY unicode_lower(channel)
        ORDER BY 1
    """):
        print(row)

    print("4. Время обработки до апреля: среднее и медиана")
    # Среднее тянут вверх редкие долгие обращения, медиана показывает
    # типичное время, поэтому в выводах я пользуюсь медианой.
    print(con.execute("""
        SELECT ROUND(AVG(handle_min), 1), MEDIAN(handle_min)
        FROM clean
        WHERE period = 'до'
    """).fetchone())

    print("5. Медиана: SQL и Python")
    sql_median = con.execute(
        "SELECT MEDIAN(handle_min) FROM clean WHERE period = 'до'"
    ).fetchone()[0]
    values = [r[0] for r in con.execute(
        "SELECT handle_min FROM clean WHERE period = 'до'"
    )]
    print(sql_median, statistics.median(values))


if __name__ == "__main__":
    main()
