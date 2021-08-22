//==============================================================================
// (C) Copyright 2021 ОАО "ПМЗ "Восход", разработано ООО «ЛаБС».
// г. Москва, Россия
//
// Блок:       БУК СУПК
// Вычислитель:A
// Компонент:  Драйвер теста test_
// Файл:       main_low_test.c
// Назначение: Обмен данными
//
// Состав:     main, 
//             set_test_out_data,
//             set_test_in_data,
//
// Примечания: нет
//------------------------------------------------------------------------------
// История изменений:
// Номер  Дата      Автор       CR       Описание
//------------------------------------------------------------------------------
//   1    01/01/70  Иванов И.   N/A      Начальная разработка
//==============================================================================

//------------------------------------------------------------------------------
// Включаемые файлы
//------------------------------------------------------------------------------
#include "low_test_drv.h"
#include "main.h"


//------------------------------------------------------------------------------
// Объявления и определения переменных
//------------------------------------------------------------------------------

// входные данные
uint32 test_number;

typedef static struct pcrREG_in_ {
    uint32 PMPROTSET0;
    uint32 PMPROTSET1;
    uint32 PPROTSET0;
    uint32 PPROTSET1;
    uint32 PPROTSET2;
    uint32 PPROTSET3;
    uint32 PCSPWRDWNSET0;
    uint32 PCSPWRDWNSET1;
    uint32 PSPWRDWNSET0;
    uint32 PSPWRDWNSET1;
    uint32 PSPWRDWNSET2;
    uint32 PSPWRDWNSET3;
    uint32 PSPWRDWNCLR0;
    uint32 PSPWRDWNCLR1;
    uint32 PSPWRDWNCLR2;
    uint32 PSPWRDWNCLR3;
} pcrREG_in;

// выходные данные
// curr_config

static void set_test_in_data();
static void set_test_out_data();

void put_config_values
{
    pcrREG_in.PMPROTSET0 = pcrREG->PMPROTSET0;
    pcrREG_in.PMPROTSET1 = pcrREG->PMPROTSET1;
    pcrREG_in.PPROTSET0 = pcrREG->PPROTSET0;
    pcrREG_in.PPROTSET1 = pcrREG->PPROTSET1;
    pcrREG_in.PPROTSET2 = pcrREG->PPROTSET2;
    pcrREG_in.PPROTSET3 = pcrREG->PPROTSET3;
    pcrREG_in.PCSPWRDWNSET0 = pcrREG->PCSPWRDWNSET0;
    pcrREG_in.PCSPWRDWNSET1 = pcrREG->PCSPWRDWNSET1;
    pcrREG_in.PSPWRDWNSET0 = pcrREG->PSPWRDWNSET0;
    pcrREG_in.PSPWRDWNSET1 = pcrREG->PSPWRDWNSET1;
    pcrREG_in.PSPWRDWNSET2 = pcrREG->PSPWRDWNSET2;
    pcrREG_in.PSPWRDWNSET3 = pcrREG->PSPWRDWNSET3;
    pcrREG_in.PSPWRDWNCLR0 = pcrREG->PSPWRDWNCLR0;
    pcrREG_in.PSPWRDWNCLR1 = pcrREG->PSPWRDWNCLR1;
    pcrREG_in.PSPWRDWNCLR2 = pcrREG->PSPWRDWNCLR2;
    pcrREG_in.PSPWRDWNCLR3 = pcrREG->PSPWRDWNCLR3;
}

void get_config_values
{
    pcrREG->PMPROTSET0 = pcrREG_in.PMPROTSET0;
    pcrREG->PMPROTSET1 = pcrREG_in.PMPROTSET1;
    pcrREG->PPROTSET0 = pcrREG_in.PPROTSET0;
    pcrREG->PPROTSET1 = pcrREG_in.PPROTSET1;
    pcrREG->PPROTSET2 = pcrREG_in.PPROTSET2;
    pcrREG->PPROTSET3 = pcrREG_in.PPROTSET3;
    pcrREG->PCSPWRDWNSET0 = pcrREG_in.PCSPWRDWNSET0;
    pcrREG->PCSPWRDWNSET1 = pcrREG_in.PCSPWRDWNSET1;
    pcrREG->PSPWRDWNSET0 = pcrREG_in.PSPWRDWNSET0;
    pcrREG->PSPWRDWNSET1 = pcrREG_in.PSPWRDWNSET1;
    pcrREG->PSPWRDWNSET2 = pcrREG_in.PSPWRDWNSET2;
    pcrREG->PSPWRDWNSET3 = pcrREG_in.PSPWRDWNSET3;
    pcrREG->PSPWRDWNCLR0 = pcrREG_in.PSPWRDWNCLR0;
    pcrREG->PSPWRDWNCLR1 = pcrREG_in.PSPWRDWNCLR1;
    pcrREG->PSPWRDWNCLR2 = pcrREG_in.PSPWRDWNCLR2;
    pcrREG->PSPWRDWNCLR3 = pcrREG_in.PSPWRDWNCLR3;
}


//--------------------------------------------------------------------
//      Основная функция
//--------------------------------------------------------------------
void main_test(void)
{
    InitDevice();

    //---------------------------------------------------------------------
    // Бесконечный цикл работы
    //---------------------------------------------------------------------
    while(1) 
    {
        // ожидание запроса от тестового окружения на проведения теста
        RequestRx();
        // записать входные глобальные данные и аргументы функции
        set_test_in_data();
        // выполнить функцию
        switch(test_number){
            case 1: //pcrInit 
                pcrInit();
            break;
        }
        // записать выходные глобальные данные
        set_test_out_data();
        // передача выходных данных функции в тестовое окружение
        ResponseTx(); 
    }  
}
//-------------------------------------------------------------
//       Запись входных данных
//-------------------------------------------------------------
static void set_test_in_data()
{
    SET_IN_DATA(&curr_config);
    SET_IN_DATA(&test_number);
    put_config_values();
}
//-------------------------------------------------------------
//             Запись выходных данных
//-------------------------------------------------------------
static void set_test_out_data()
{
    get_config_values();
    SET_OUT_DATA(&curr_config);
}
