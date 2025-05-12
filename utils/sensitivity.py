import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol

def run_sensitivity_analysis(model_func, problem, base_values, num_samples=512):
    """
    Выполняет глобальный анализ чувствительности (метод Соболя + Saltelli sampling).

    :param model_func: функция модели, принимающая массив параметров и возвращающая результат (например, IRR)
    :param problem: словарь с описанием переменных для SALib
    :param base_values: базовые значения переменных
    :param num_samples: количество выборок для анализа
    :return: словарь с индексами чувствительности
    """
    # Сэмплирование
    param_values = saltelli.sample(problem, num_samples)

    # Моделирование
    Y = np.array([model_func(*params) for params in param_values])

    # Анализ чувствительности
    Si = sobol.analyze(problem, Y)

    return {
        "S1": Si['S1'],      # Первичные индексы (вклад отдельных переменных)
        "ST": Si['ST'],      # Общие индексы (включая взаимодействие)
        "names": problem['names']
    }