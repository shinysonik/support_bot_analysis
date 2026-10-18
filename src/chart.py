"""График для записки: доля решённых обращений по сегментам.

Запуск из корня репозитория: python3 src/chart.py
Результат: analysis/report_chart.png (нужен matplotlib)
"""

from pathlib import Path

import matplotlib.pyplot as plt

from db import connect
from run_sql import register_own_functions

OUT = Path(__file__).resolve().parent.parent / "analysis" / "report_chart.png"

TITLE = "Из обращений второй линии бот решил с первого раза 48%, люди — 77%"
YLABEL = "Решено без переоткрытия и возврата, % обращений"

ORDER = "CASE segment WHEN 'первая' THEN 1 WHEN 'серая' THEN 2 ELSE 3 END"

SERIES = [
    ("Люди, до апреля", f"""
        SELECT segment, ROUND(AVG(reopened = 0 AND came_back = 0) * 100, 1)
        FROM segmented
        WHERE period = 'до' AND written = 1
        GROUP BY segment ORDER BY {ORDER}
    """),
    ("Закрыл бот, после апреля", f"""
        SELECT segment, ROUND(AVG(reopened = 0 AND came_back = 0) * 100, 1)
        FROM segmented
        WHERE period = 'после' AND written = 1 AND bot_result = 'закрыл'
        GROUP BY segment ORDER BY {ORDER}
    """),
]

con = connect()
register_own_functions(con)

labels = None
top = 0
fig, ax = plt.subplots(figsize=(8, 4.5))
width = 0.8 / len(SERIES)
for k, (name, query) in enumerate(SERIES):
    rows = con.execute(query).fetchall()
    if labels is None:
        labels = [str(r[0]) for r in rows]
    values = {str(r[0]): r[1] for r in rows}
    xs = [i - 0.4 + width * (k + 0.5) for i in range(len(labels))]
    ys = [values.get(label) or 0 for label in labels]
    ax.bar(xs, ys, width=width, label=name)
    top = max([top] + ys)
    for x, y in zip(xs, ys):
        ax.text(x, y, f"{y:g}", ha="center", va="bottom", fontsize=9)

ax.set_xticks(range(len(labels)), labels)
ax.set_title(TITLE)
ax.set_ylabel(YLABEL)
ax.set_ylim(0, top * 1.25 if top else 1)
ax.legend(loc="upper right", ncol=len(SERIES))
fig.tight_layout()
fig.savefig(OUT, dpi=150)
print(f"Сохранено: {OUT}")
