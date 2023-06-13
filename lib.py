import numpy as np
from scipy.stats import nakagami
from scipy.stats import gamma, norm
import random
import markovify


def init():
    nu = 0.5
    mean, var, skew, kurt = nakagami.stats(nu, moments='mvsk')
    print(mean, var, skew, kurt)
    r = nakagami.rvs(nu, size=10000)
    return r


def init_gamma():
    a = 1.99
    mean, var, skew, kurt = gamma.stats(a, moments='mvsk')
    gamma_values = gamma.rvs(a, size=10000)
    return gamma_values


def init_norm():
    norm_values = norm.rvs(size=10000)
    return norm_values

# Функция для создания односвязной марковской цепи
def create_markov_chain(data, order=1):
    # Границы диапазона значений
    min_val = np.min(data)
    max_val = np.max(data)

    # Разбиение диапазона на бины
    bins = np.linspace(min_val, max_val, num=100)

    # Создание матрицы переходных вероятностей
    transition_matrix = np.zeros((100, 100))

    for i in range(len(data) - order):
        bin_index = int(np.digitize(data[i], bins)) - 1
        next_bin_index = int(np.digitize(data[i + order], bins)) - 1
        transition_matrix[bin_index][next_bin_index] += 1

    # Нормализация матрицы
    row_sums = transition_matrix.sum(axis=1)
    transition_matrix /= row_sums[:, np.newaxis]

    return transition_matrix, bins

# Функция для генерации новой последовательности на базе односвязной марковской модели
def generate_sequence(transition_matrix, bins, length=10000):
    # Выбираем случайный стартовый бин
    bin_index = np.random.choice(np.arange(len(bins)))
    sequence = [bins[bin_index]]

    # Генерируем новую последовательность
    for i in range(1, length):
        # Выбираем следующий бин на основе матрицы переходных вероятностей
        prob = transition_matrix[bin_index]
        next_bin_index = np.random.choice(np.arange(len(bins)), p=prob)
        bin_index = next_bin_index
        sequence.append(bins[bin_index])

    return sequence


def func(data):
    transition_matrix, bins = create_markov_chain(data)
    # Генерация новой последовательности на базе модели
    new_sequence = generate_sequence(transition_matrix, bins, len(data))
    return bins, new_sequence
