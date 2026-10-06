"""Вывод таблицы по операциям и заключения в консоль."""

from calculations import (best_case, worst_case, bcet, wcet, nondeterminism_ratio,
                          total_mem_accesses, total_branches, source_breakdown,
                          fits_deadline)


def fmt(x):
    """Число без лишних нулей: 11.0 -> 11, 19.333 -> 19.33."""
    return f"{round(x, 2):g}"


def ticks(n):
    """Число со словом «такт» в нужной форме: 1 такт, 2 такта, 5 тактов."""
    n = int(n)
    if n % 10 == 1 and n % 100 != 11:
        word = "такт"
    elif 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        word = "такта"
    else:
        word = "тактов"
    return f"{n} {word}"


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


def print_conclusion(fragment, model, deadline):
    """Печатает заключение: BCET, WCET, коэффициент, вклад источников, дедлайн."""
    best = bcet(fragment, model)
    worst = wcet(fragment, model)
    n_mem = total_mem_accesses(fragment)
    n_br = total_branches(fragment)

    print("\nЗАКЛЮЧЕНИЕ")
    print(f"Модель процессора: базовая стоимость {ticks(model.base_cost)}, "
          f"промах кэша +{model.cache_miss_penalty}, "
          f"ошибка предсказания +{model.mispredict_penalty}")
    print(f"Операций: {len(fragment)}, обращений к памяти: {n_mem}, ветвлений: {n_br}")
    print(f"BCET = {ticks(best)} (все попадания в кэш и верные предсказания)")

    # Расписываем формулу, чтобы расчёт можно было проверить вручную
    print(f"WCET = {best} + {n_mem}·{model.cache_miss_penalty} + "
          f"{n_br}·{model.mispredict_penalty} = {ticks(worst)}")
    print(f"Коэффициент недетерминизма: K = WCET / BCET = {worst} / {best} = "
          f"{fmt(nondeterminism_ratio(fragment, model))}")

    print("Вклад источников в WCET:")
    parts = source_breakdown(fragment, model)
    src_w = max(len(name) for name in parts)
    for name, value in parts.items():
        share = value / worst * 100
        print(f"  {name:<{src_w}} {ticks(value):>11} ({share:.1f} %)")

    print(f"Дедлайн: {ticks(deadline)}")
    margin = deadline - worst
    if fits_deadline(fragment, model, deadline):
        print(f"Вывод: в худшем случае фрагмент укладывается в дедлайн (запас {ticks(margin)}).")
    else:
        print(f"Вывод: в худшем случае фрагмент НЕ укладывается в дедлайн "
              f"(превышение {ticks(-margin)}).")