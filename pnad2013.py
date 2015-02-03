# -*- coding: utf-8; -*-

import io
import sys
import pandas
import numpy

## TOTAL_LINES = 362556

CONVERT_TABLE = {c: lambda value: int(value or 0) for c in [
    'V4746',
    'V4747',
    'V4748',
    'V4749',
]}

REGIOES_TABLE = {
    'norte': [11, 12, 13, 14, 15, 16, 17, 21, 22],
}

IDADES_TABLE = {
    'ate_18':      [('lt',  18)],
    'de_19_a_30':  [('gte', 18), ('lt', 30)],
    'de_31_a_45':  [('gte', 30), ('lt', 45)],
    'de_46_a_50':  [('gte', 45), ('lt', 50)],
    'mais_de_50':  [('gte', 50)],
}

CLASSES_TABLE = {
    'e': [('lt',  1085)],
    'd': [('gte', 1085), ('lt', 1734)],
    'c': [('gte', 1734), ('lt', 7475)],
    'b': [('gte', 7475), ('lt', 9745)],
    'a': [('gte', 9745)],
}


def filtrar_regiao(pnad, name):
    all_codes = REGIOES_TABLE[name][:]   # Do not touch actual value
    flag = (pnad.UF == all_codes.pop(0)) # Initialize flag
    for uf_id in REGIOES_TABLE[name]:
        flag |= (pnad.UF == uf_id)
    return flag


def filtrar_range(pnad, name, table, variable_name):
    all_ranges = table[name][:]   # Do not touch actual value
    variable = getattr(pnad, variable_name)
    operators = {
        'lt':  lambda v: (variable < v),
        'gte': lambda v: (variable >= v),
    }

    # Initialize flag
    initial_flag_data = all_ranges.pop(0)
    operator, value = initial_flag_data
    flag = operators[operator](value)

    # Add more flags
    for item in all_ranges:
        operator, value = item
        flag &= operators[operator](value)
    return flag


def filtrar_idade(pnad, name):
    return filtrar_range(pnad, name, table=IDADES_TABLE, variable_name='V8005')


def filtrar_classe(pnad, name):
    return filtrar_range(pnad, name, table=CLASSES_TABLE, variable_name='V4722')


def read_file(path):
    pnad = pandas.read_csv(
        path, sep=',', header=0, low_memory=False,
        converters=CONVERT_TABLE)

    # Separa por região
    for regiao in REGIOES_TABLE:
        print 'regiao:', regiao
        view = pnad[filtrar_regiao(pnad, regiao)]
        for idade in IDADES_TABLE:
            print '  idade:', idade
            idade_view = view[filtrar_idade(view, idade)]
            for classe in CLASSES_TABLE:
                print '    classe:', classe,
                classe_view = idade_view[filtrar_classe(idade_view, classe)]
                print len(classe_view)


if __name__ == '__main__':
    try:
        read_file(sys.argv[1])
    except IndexError:
        print("Usage: {0} dataset.csv".format(sys.argv[0]))