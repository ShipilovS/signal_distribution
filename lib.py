import numpy as np
from scipy.stats import nakagami
from scipy.stats import gamma, norm
from scipy.stats import kurtosis
import random
import markovify


def init(size=10000):
    nu = 0.5
    mean, var, skew, kurt = nakagami.stats(nu, moments='mvsk')
    print(mean, var, skew, kurt)
    r = nakagami.rvs(nu, size=size)
    return r

def init_gamma(size=10000):
    a = 1.99
    mean, var, skew, kurt = gamma.stats(a, moments='mvsk')
    gamma_values = gamma.rvs(a, size=size)
    return gamma_values

def init_norm(size=10000):
    norm_values = norm.rvs(size=size)
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

    print(f"Входные данные: \n")
    get_info_in_console_1d(data)

    return transition_matrix, bins

# Функция для генерации новой последовательности на базе односвязной марковской модели
def generate_sequence(transition_matrix, bins, length=10):
    # Выбираем случайный стартовый бин
    bin_index = np.random.choice(np.arange(len(bins)))
    sequence = [bins[bin_index]]

    # Генерируем новую последовательность
    for i in range(1, length):
        # Выбираем следующий бин на основе матрицы переходных вероятностей
            prob = transition_matrix[bin_index]

            if not np.all(np.isnan(prob)):
                next_bin_index = np.random.choice(np.arange(len(bins)), p=prob)
                bin_index = next_bin_index
                sequence.append(bins[bin_index])

    print(f"Промоделированный сигнал: \n")
    get_info_in_console_1d(sequence)

    return sequence


def func(data):
    transition_matrix, bins = create_markov_chain(data)
    # Генерация новой последовательности на базе модели
    new_sequence = generate_sequence(transition_matrix, bins, len(data))
    return bins, new_sequence

def create_markov_chain_2d(data, num_bins=1000, order=1):
    min_val = np.amin(data)
    max_val = np.amax(data)

    bins = np.linspace(min_val, max_val, num=num_bins)

    transition_matrix = np.zeros((num_bins, num_bins))

    for i in range(len(data) - order):
        bin_index = int(np.digitize(data[i], bins)) - 1
        if bin_index == num_bins:
           bin_index -= 1
        next_bin_index = int(np.digitize(data[i + order], bins)) - 1
        if next_bin_index == num_bins:
           next_bin_index -= 1
        transition_matrix[bin_index][next_bin_index] += 1

    row_sums = transition_matrix.sum(axis=1)
    transition_matrix /= row_sums[:,np.newaxis]
    print(f"Входные данные: \n")
    get_info_in_console(data)
    return transition_matrix, bins

def generate_sequence_2d(transition_matrix, bins, length=100):
    num_bins = transition_matrix.shape[0]

    bin_index = np.random.choice(np.arange(num_bins))
    sequence = [bins[bin_index]]

    for i in range(1, length):
        prob = transition_matrix[bin_index]
        if not np.all(np.isnan(prob)):
            next_bin_index = np.random.choice(np.arange(num_bins), p=prob)
            if next_bin_index == num_bins:
                next_bin_index -= 1
            bin_index = next_bin_index
            if bin_index == num_bins:
                bin_index -= 1
            sequence.append(bins[bin_index])

    print(f"Промоделированный сигнал: \n")
    get_info_in_console(sequence)

    return sequence


def get_info_in_console(sequence):
    mean = np.mean(sequence)
    variance = np.var(sequence)
    module = np.sqrt(variance)
    media = np.median(sequence)
    print("Мат. ожидание: ", mean)
    print("Дисперсия: ", variance)
    print("Мода: ", module)
    print("Медиана: ", media)

    corr_coef_new = np.corrcoef(sequence[:-1], sequence[1:])[0][1]
    print("Коэффициент корреляции сгенерированного сигнала: ", corr_coef_new)

    kurtosis_new = kurtosis(sequence)
    print("Эксцесс сгенерированного сигнала: ", kurtosis_new)

    stdgen = np.std(sequence)
    print("Стандартное отклонение сигнала: ", stdgen)
    print('\n\n')

def get_info_in_console_1d(data):
    mean_new = np.mean(data)
    variance_new = np.var(data)
    mode_new = np.sqrt(np.var(data))
    median_new = np.median(data)
    corr_coef_new = np.corrcoef(data[:-1], data[1:])[0][1]
    kurtosis_new = kurtosis(data)
    std_dev_new = np.sqrt(variance_new)

    print("Мат. ожидание сигнала: ", mean_new)
    print("Дисперсия сигнала: ", variance_new)
    print("Мода сигнала: ", mode_new)
    print("Медиана сигнала: ", median_new)
    print("Коэффициент корреляции сигнала: ", corr_coef_new)
    print("Эксцесс сигнала: ", kurtosis_new)
    print("Среднеквадратическое отклонение сигнала: ", std_dev_new)
    print(f"\n\n")