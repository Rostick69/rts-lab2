"""Модель операции и модель процессора, загрузка исходных данных из JSON."""

import json
from dataclasses import dataclass

# Допустимые типы операций
OP_TYPES = ("чтение", "запись", "вычисление", "ветвление")


@dataclass
class Operation:
    """Одна операция фрагмента кода."""
    name: str          # название операции
    op_type: str       # тип: чтение / запись / вычисление / ветвление
    mem_accesses: int  # число обращений к памяти
    branches: int      # число условных переходов (ветвлений)


@dataclass
class ProcessorModel:
    """Модель процессора. Все значения в тактах."""
    base_cost: int           # базовая стоимость одной операции
    cache_miss_penalty: int  # штраф за промах кэша (на одно обращение к памяти)
    mispredict_penalty: int  # штраф за ошибку предсказания перехода (на одно ветвление)


def load_variant(path):
    """Читает файл варианта и возвращает (название, список операций, модель процессора, дедлайн)."""
    # utf-8-sig читает файл и с BOM, и без него
    # (Visual Studio иногда сохраняет файлы с BOM, и обычный utf-8 на этом падает)
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)

    p = data["processor"]
    model = ProcessorModel(p["base_cost"], p["cache_miss_penalty"], p["mispredict_penalty"])

    fragment = []
    for item in data["operations"]:
        op = Operation(item["name"], item["type"], item["mem_accesses"], item["branches"])
        fragment.append(op)

    deadline = data["deadline"]
    title = data.get("title", "без названия")  # если названия в файле нет, программа не упадёт
    return title, fragment, model, deadline