"""Вывод таблицы по операциям и заключения в консоль."""

from calculations import (best_case, worst_case, bcet, wcet,
                          total_mem_accesses, total_branches)


def print_table(fragment, model):
    """Печатает таблицу: Операция | Тип | Память | Ветвл. | Лучшее | Худшее."""
    # Ширина первой колонки подстраивается под самое длинное название операции
    name_w = max(len("Операция"), max(len(op.name) for op in fragment))

    header = (f"{'Операция':<{name_w}} | {'Тип':<10} | {'Память':>6} | {'Ветвл.':>6} | "
              f"{'Лучшее':>6} | {'Худшее':>6}")
    print(header)
    print("-" * len(header))

    for op in fragment:
        print(f"{op.name:<{name_w}} | {op.op_type:<10} | {op.mem_accesses:>6} | "
              f"{op.branches:>6} | {best_case(op, model):>6} | {worst_case(op, model):>6}")

    print("-" * len(header))
    print(f"{'Итого':<{name_w}} | {'':<10} | {total_mem_accesses(fragment):>6} | "
          f"{total_branches(fragment):>6} | {bcet(fragment, model):>6} | {wcet(fragment, model):>6}")