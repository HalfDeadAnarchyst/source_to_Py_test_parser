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
# test_01: dmaEnable 
#
# test_02: dmaSetCtrlPacket 
#
# test_03: dmaSetSWChEnable 
#
# test_04: dmaGetConfigValue if ! (type == InitialValue) 
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


class PCP(Structure):
    _fields_ = [("ISADDR", c_uint32),
        ("IDADDR", c_uint32),
        ("ITCOUNT", c_uint32),
        ("CHCTRL", c_uint32),
        ("EIOFF", c_uint32),
        ("FIOFF", c_uint32),
        ]


class dmaREG(Structure):
    _fields_ = [("GCTRL", c_uint32),
        ("SWCHENAS", c_uint32),
        ("CHPRIOS", c_uint32),
        ("GCHIENAS", c_uint32),
        ("DREQASI", c_uint32 * 8),
        ("PAR", c_uint32 * 4),
        ("FTCINTENAS", c_uint32),
        ("LFSINTENAS", c_uint32),
        ("HBCINTENAS", c_uint32),
        ("BTCINTENAS", c_uint32),
        ("DMAPCR", c_uint32),
        ("DMAMPCTRL", c_uint32),
        ]


class dmaRAMREG(Structure):
    _fields_ = [(PCP * 32),
        ]


# Номер теста (технический)
test_number = c_uint32(1)

# Входные данные
PCP_in = PCP()
# Поставить значения отличные от всех остальных!
PCP_in.ISADDR = 0  # Поменять значение!
PCP_in.IDADDR = 0  # Поменять значение!
PCP_in.ITCOUNT = 0  # Поменять значение!
PCP_in.CHCTRL = 0  # Поменять значение!
PCP_in.EIOFF = 0  # Поменять значение!
PCP_in.FIOFF = 0  # Поменять значение!

dmaREG_in = dmaREG()
# Поставить значения отличные от всех остальных!
dmaREG_in.GCTRL = 0  # Поменять значение!
dmaREG_in.PAR = 0  # Поменять значение!
dmaREG_in.SWCHENAS = 0  # Поменять значение!
dmaREG_in.CHPRIOS = 0  # Поменять значение!
dmaREG_in.GCHIENAS = 0  # Поменять значение!
dmaREG_in.DREQASI = 0  # Поменять значение!
dmaREG_in.FTCINTENAS = 0  # Поменять значение!
dmaREG_in.LFSINTENAS = 0  # Поменять значение!
dmaREG_in.HBCINTENAS = 0  # Поменять значение!
dmaREG_in.BTCINTENAS = 0  # Поменять значение!
dmaREG_in.DMAPCR = 0  # Поменять значение!
dmaREG_in.DMAMPCTRL = 0  # Поменять значение!

dmaRAMREG_in = dmaRAMREG()
# Поставить значения отличные от всех остальных!
dmaRAMREG_in.PCP = 0  # Поменять значение!


# Данные для проверки
test_01_dmaREG_out = dmaREG
test_01_dmaREG_out.GCTRL = 0  # Поменять значение!

test_02_dmaRAMREG_out = dmaRAMREG
test_02_dmaRAMREG_out.PCP = 0  # Поменять значение!

test_02_PCP_out = PCP
test_02_PCP_out.ISADDR = 0  # Поменять значение!
test_02_PCP_out.IDADDR = 0  # Поменять значение!
test_02_PCP_out.ITCOUNT = 0  # Поменять значение!
test_02_PCP_out.CHCTRL = 0  # Поменять значение!
test_02_PCP_out.EIOFF = 0  # Поменять значение!
test_02_PCP_out.FIOFF = 0  # Поменять значение!

test_02_dmaREG_out = dmaREG
test_02_dmaREG_out.PAR = 0  # Поменять значение!

test_03_dmaREG_out = dmaREG
test_03_dmaREG_out.SWCHENAS = 0  # Поменять значение!

data_common_in = {
    "test_number": test_number,
    "PCP_in": PCP_in,
    "dmaREG_in": dmaREG_in,
    "dmaRAMREG_in": dmaRAMREG_in,
}

data_common_out = {
    "test_01_dmaREG_out": test_01_dmaREG_out,
    "test_02_dmaRAMREG_out": test_02_dmaRAMREG_out,
    "test_02_PCP_out": test_02_PCP_out,
    "test_02_dmaREG_out": test_02_dmaREG_out,
    "test_03_dmaREG_out": test_03_dmaREG_out,
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
    input_data = [in_data["PCP_in"], in_data["dmaREG_in"], in_data["dmaRAMREG_in"], ]

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
#    тесткейс проверки работоспособности dmaEnable 
#
# 2. Входные данные:
#    dmaREG | 
#    GCTRL | 
#
# 2. Выходные данные:
#    dmaREG | 
#    GCTRL | 
#    
# ======================================================================================================================

def test_01():
    in_data = copy.deepcopy(data_common_in)
    in_data["test_number"].value = 1
    verify_data = copy.deepcopy(data_common_out)
    out_data = copy.deepcopy(data_common_out)
    REGlist = [['dmaREG', ['GCTRL']]]
    execute_testcase(in_data, verify_data, out_data, REGlist)


# ======================================================================================================================
#
# Тесткейс test_02
#
# 1. Проверяемые требования: BUKSUPK_SW.#####
#    тесткейс проверки работоспособности dmaSetCtrlPacket 
#
# 2. Входные данные:
#    dmaRAMREG | PCP | dmaREG | 
#    PCP | ISADDR IDADDR ITCOUNT CHCTRL EIOFF FIOFF | PAR | 
#
# 2. Выходные данные:
#    dmaRAMREG | PCP | dmaREG | 
#    PCP | ISADDR IDADDR ITCOUNT CHCTRL EIOFF FIOFF | PAR | 
#    
# ======================================================================================================================

def test_02():
    in_data = copy.deepcopy(data_common_in)
    in_data["test_number"].value = 2
    verify_data = copy.deepcopy(data_common_out)
    out_data = copy.deepcopy(data_common_out)
    REGlist = [['dmaRAMREG', ['PCP']], ['PCP', ['ISADDR', 'IDADDR', 'ITCOUNT', 'CHCTRL', 'EIOFF', 'FIOFF']], ['dmaREG', ['PAR']]]
    execute_testcase(in_data, verify_data, out_data, REGlist)


# ======================================================================================================================
#
# Тесткейс test_03
#
# 1. Проверяемые требования: BUKSUPK_SW.#####
#    тесткейс проверки работоспособности dmaSetSWChEnable 
#
# 2. Входные данные:
#    dmaREG | 
#    SWCHENAS | 
#
# 2. Выходные данные:
#    dmaREG | 
#    SWCHENAS | 
#    
# ======================================================================================================================

def test_03():
    in_data = copy.deepcopy(data_common_in)
    in_data["test_number"].value = 3
    verify_data = copy.deepcopy(data_common_out)
    out_data = copy.deepcopy(data_common_out)
    REGlist = [['dmaREG', ['SWCHENAS']]]
    execute_testcase(in_data, verify_data, out_data, REGlist)

