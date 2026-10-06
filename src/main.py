"""Практическая работа 2 (СРВ). Вариант 2: шаг ПИД-регулятора.

Запуск: python src/main.py [путь_к_файлу.json]
Без аргумента берётся data/variant2.json.
"""

import sys
from pathlib import Path

from models import load_variant
from output import print_table, print_conclusion

# Путь строим от расположения этого файла, а не от текущей папки,
# поэтому программа находит данные при запуске и из Visual Studio, и из консоли
DEFAULT_DATA = Path(__file__).parent.parent / "data" / "variant2.json"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA
    title, fragment, model, deadline = load_variant(path)

    print(f"Оценка WCET: {title}\n")
    print_table(fragment, model)
    print_conclusion(fragment, model, deadline)


if __name__ == "__main__":
    main()