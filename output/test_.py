# -*- coding: utf-8; -*-
# ---------------------------------------------------------------------------------------------------------------------
#                            Разработано ООО «ЛаБС», все права принадлежат ОАО "ПМЗ "Восход"
# ---------------------------------------------------------------------------------------------------------------------

test_script_header = """
# ---------------------------------------------------------------------------------------------------------------------
# [PURPOSE]: BUKSUPK_SW.######: Тест проверки модуля ######.
#
# [VERIFIED REQUIREMENTS]: BUKSUPK_SW.######
#
# [FUNCTIONS]:
#
# execute_testcase: Проверить значения параметров после отработки функции
#
# test_01: pcrInit 
#
# test_02: pcrGetConfigValue if (type == InitialValue) 
#
# test_03: pcrGetConfigValue if ! (type == InitialValue) 
#
# test_04: pcrCheckConfig 
#
# ---------------------------------------------------------------------------------------------------------------------
#
# [MODIFICATION HISTORY]:
#     [VERSION]     : 1.0
#     [DATE]        : 01-January-1970
#     [AUTHOR]      : Иванов И. И.
#     [DESCRIPTION] : Начальная разработка.
#     [CR]          : N/A
#
# ---------------------------------------------------------------------------------------------------------------------
"""

from ctypes import *
import copy
from libs.low_test_drv import *
import framework.globals as test_globals_module


class pcrREG(Structure):
    _fields_ = [("PMPROTSET0", c_uint32),
        ("PMPROTSET1", c_uint32),
        ("PPROTSET0", c_uint32),
        ("PPROTSET1", c_uint32),
        ("PPROTSET2", c_uint32),
        ("PPROTSET3", c_uint32),
        ("PCSPWRDWNSET0", c_uint32),
        ("PCSPWRDWNSET1", c_uint32),
        ("PSPWRDWNSET0", c_uint32),
        ("PSPWRDWNSET1", c_uint32),
        ("PSPWRDWNSET2", c_uint32),
        ("PSPWRDWNSET3", c_uint32),
        ("PSPWRDWNCLR0", c_uint32),
        ("PSPWRDWNCLR1", c_uint32),
        ("PSPWRDWNCLR2", c_uint32),
        ("PSPWRDWNCLR3", c_uint32),
        ]


# Номер теста (технический)
test_number = c_uint32(1)

# Входные данные
pcrREG_in = pcrREG()
# Поставить значения отличные от всех остальных!
pcrREG_in.PSPWRDWNCLR0 = 0  # Поменять значение!
pcrREG_in.PSPWRDWNCLR1 = 0  # Поменять значение!
pcrREG_in.PSPWRDWNCLR2 = 0  # Поменять значение!
pcrREG_in.PSPWRDWNCLR3 = 0  # Поменять значение!
pcrREG_in.PMPROTSET0 = 0  # Поменять значение!
pcrREG_in.PMPROTSET1 = 0  # Поменять значение!
pcrREG_in.PPROTSET0 = 0  # Поменять значение!
pcrREG_in.PPROTSET1 = 0  # Поменять значение!
pcrREG_in.PPROTSET2 = 0  # Поменять значение!
pcrREG_in.PPROTSET3 = 0  # Поменять значение!
pcrREG_in.PCSPWRDWNSET0 = 0  # Поменять значение!
pcrREG_in.PCSPWRDWNSET1 = 0  # Поменять значение!
pcrREG_in.PSPWRDWNSET0 = 0  # Поменять значение!
pcrREG_in.PSPWRDWNSET1 = 0  # Поменять значение!
pcrREG_in.PSPWRDWNSET2 = 0  # Поменять значение!
pcrREG_in.PSPWRDWNSET3 = 0  # Поменять значение!


# Данные для проверки
test_01_pcrREG_out = pcrREG
test_01_pcrREG_out.PSPWRDWNCLR0 = 0  # Поменять значение!
test_01_pcrREG_out.PSPWRDWNCLR1 = 0  # Поменять значение!
test_01_pcrREG_out.PSPWRDWNCLR2 = 0  # Поменять значение!
test_01_pcrREG_out.PSPWRDWNCLR3 = 0  # Поменять значение!

data_common_in = {
    "test_number": test_number,
    "pcrREG_in": pcrREG_in,
}

data_common_out = {
    "test_01_pcrREG_out": test_01_pcrREG_out,
}

# Список регистров для проверки
REGlist = []


def execute_testcase(in_data, verify_data, out_data, REGlist):
    """
    Назначение: Проверить значения параметров после отработки функции

    Идентификатор требований: BUKSUPK_SW.#####
    """

    #  входные данные теста
    test_globals_module.logger.print("==== Исходные значения ====")
    test_globals_module.logger.print(f"Входные данные: ")
    for structs in REGlist:
        reference_object = structs[0]
        for item in structs[1:]:
            attr = reference_object.item.__getattribute__(item)
            test_globals_module.logger.print(f"{reference_object}.{item} = {attr}")
            
    # Входные данные теста
    input_data = [in_data["pcrREG_in"], ]

    # выходные данные теста
    # out_data

    # ======= Обмен данными в БУК СУПК
    # получить массив входных данных теста
    tx_data = set_in_data(input_data)

    # получить массив выходных данных теста
    ptr = CAN_lib.LowTest(tx_data[0], tx_data[1])

    # получить выходные данные теста
    out_data = get_out_data(ptr, out_data)
    # ==========================================

    test_globals_module.logger.print("==== Выходные значения ====")
    # проверяем соответствие значений каждого проверяемого регистра

    for structs in REGlist:
        reference_object = structs[0]
        for item in structs[1:]:
            expected_value = verify_data.__getattribute__(item)
            actual_value = out_data[0].__getattribute__(item)
            test_globals_module.test_session.verify(expected_value, actual_value,
                                                    f"Значение параметра {reference_object}.{item} "
                                                    f"соответствует ожидаемому")
                                               
                                               
# ======================================================================================================================
#
# Тесткейс test_01
#
# 1. Проверяемые требования: BUKSUPK_SW.#####
#    тесткейс проверки работоспособности pcrInit 
#
# 2. Входные данные:
#    pcrREG | 
#    PSPWRDWNCLR0 PSPWRDWNCLR1 PSPWRDWNCLR2 PSPWRDWNCLR3 | 
#
# 2. Выходные данные:
#    pcrREG | 
#    PSPWRDWNCLR0 PSPWRDWNCLR1 PSPWRDWNCLR2 PSPWRDWNCLR3 | 
#    
# ======================================================================================================================

def test_01():
    in_data = copy.deepcopy(data_common_in)
    in_data["test_number"].value = 1
    verify_data = copy.deepcopy(data_common_out)
    out_data = copy.deepcopy(data_common_out)
    REGlist = [['pcrREG', ['PSPWRDWNCLR0', 'PSPWRDWNCLR1', 'PSPWRDWNCLR2', 'PSPWRDWNCLR3']]]
    execute_testcase(in_data, verify_data, out_data, REGlist)

