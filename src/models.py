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
    if model.base_cost <= 0:
        raise ValueError("Базовая стоимость операции должна быть больше нуля")
    if model.cache_miss_penalty < 0 or model.mispredict_penalty < 0:
        raise ValueError("Штрафы процессора не могут быть отрицательными")

    fragment = []
    for item in data["operations"]:
        op = Operation(item["name"], item["type"], item["mem_accesses"], item["branches"])

        # Проверяем данные сразу при загрузке, чтобы расчёты не дали неверный результат
        if op.op_type not in OP_TYPES:
            raise ValueError(f"Неизвестный тип у операции «{op.name}»: {op.op_type}")
        if op.mem_accesses < 0 or op.branches < 0:
            raise ValueError(f"У операции «{op.name}» число обращений и ветвлений не может быть отрицательным")

        fragment.append(op)

    # Пустой фрагмент даст BCET = 0 и деление на ноль в коэффициенте недетерминизма
    if not fragment:
        raise ValueError("Во фрагменте нет ни одной операции")

    deadline = data["deadline"]
    if deadline <= 0:
        raise ValueError("Дедлайн должен быть больше нуля")

    title = data.get("title", "без названия")  # если названия в файле нет, программа не упадёт
    return title, fragment, model, deadline