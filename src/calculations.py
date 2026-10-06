"""Оценка лучшего и наихудшего времени выполнения фрагмента (BCET, WCET)."""


def best_case(op, model):
    """Лучшее время операции: все обращения к памяти — попадания в кэш,
    все переходы предсказаны верно."""
    # В лучшем случае память и переходы не добавляют задержек,
    # поэтому операция стоит ровно базовую стоимость
    return model.base_cost


def worst_case(op, model):
    """Худшее время операции: каждое обращение к памяти — промах кэша,
    каждый переход предсказан неверно."""
    return (model.base_cost
            + op.mem_accesses * model.cache_miss_penalty
            + op.branches * model.mispredict_penalty)



def bcet(fragment, model):
    """Наилучшее время выполнения фрагмента — сумма лучших времён операций."""
    return sum(best_case(op, model) for op in fragment)


def wcet(fragment, model):
    """Наихудшее время выполнения фрагмента — сумма худших времён операций."""
    return sum(worst_case(op, model) for op in fragment)


def nondeterminism_ratio(fragment, model):
    """Коэффициент недетерминизма K = WCET / BCET."""
    return wcet(fragment, model) / bcet(fragment, model)



def total_mem_accesses(fragment):
    """Общее число обращений к памяти во фрагменте."""
    return sum(op.mem_accesses for op in fragment)


def total_branches(fragment):
    """Общее число ветвлений во фрагменте."""
    return sum(op.branches for op in fragment)


def source_breakdown(fragment, model):
    """Вклад каждого источника в WCET (в тактах)."""
    # Память и ветвления считаем отдельно: каждый источник даёт свой штраф,
    # а в сумме с базовым временем они дают ровно WCET
    return {
        "базовое выполнение": bcet(fragment, model),
        "память (промахи кэша)": total_mem_accesses(fragment) * model.cache_miss_penalty,
        "ветвления (ошибки предсказания)": total_branches(fragment) * model.mispredict_penalty,
    }


def fits_deadline(fragment, model, deadline):
    """Укладывается ли фрагмент в дедлайн в худшем случае (WCET <= дедлайн)."""
    return wcet(fragment, model) <= deadline