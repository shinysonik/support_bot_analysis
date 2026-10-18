"""Две функции, которых нет в SQLite: нижний регистр для кириллицы и медиана.

run_sql.py и workload.py регистрируют их в базе как unicode_lower() и MEDIAN().
"""


def unicode_lower(text):
    """Нижний регистр для любого текста. Встроенный lower() в SQLite
    приводит только латиницу, поэтому 'Чат' и 'чат' остались бы разными каналами."""
    if text is None:
        return None
    return text.lower()


class Median:
    """Агрегатная функция MEDIAN: SQLite создаёт объект на каждую группу,
    вызывает step() для каждой строки и в конце finalize()."""

    def __init__(self):
        self.values = []

    def step(self, value):
        if value is not None:
            self.values.append(value)

    def finalize(self):
        if not self.values:
            return None
        data = sorted(self.values)
        n = len(data)
        mid = n // 2
        if n % 2 == 1:
            return data[mid]
        return (data[mid - 1] + data[mid]) / 2
