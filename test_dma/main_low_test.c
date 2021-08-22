//==============================================================================
// (C) Copyright 2021 ��� "��� "������", ����������� ��� ����ѻ.
// �. ������, ������
//
// ����:       ��� ����
// �����������:A
// ���������:  ������� ����� test_
// ����:       main_low_test.c
// ����������: ����� �������
//
// ������:     main, 
//             set_test_out_data,
//             set_test_in_data,
//
// ����������: ���
//------------------------------------------------------------------------------
// ������� ���������:
// �����  ����      �����       CR       ��������
//------------------------------------------------------------------------------
//   1    01/01/70  ������ �.   N/A      ��������� ����������
//==============================================================================

//------------------------------------------------------------------------------
// ���������� �����
//------------------------------------------------------------------------------
#include "low_test_drv.h"
#include "main.h"


//------------------------------------------------------------------------------
// ���������� � ����������� ����������
//------------------------------------------------------------------------------

// ������� ������
uint32 test_number;

typedef static struct PCP_in_ {
    uint32 ISADDR;
    uint32 IDADDR;
    uint32 ITCOUNT;
    uint32 CHCTRL;
    uint32 EIOFF;
    uint32 FIOFF;
} PCP_in;

typedef static struct dmaRAMREG_in_ {
    struct PCP[32]_in;
} dmaRAMREG_in;

typedef static struct dmaREG_in_ {
    uint32 GCTRL;
    uint32 SWCHENAS;
    uint32 CHPRIOS;
    uint32 GCHIENAS;
    uint32 DREQASI[8];
    uint32 PAR[4];
    uint32 FTCINTENAS;
    uint32 LFSINTENAS;
    uint32 HBCINTENAS;
    uint32 BTCINTENAS;
    uint32 DMAPCR;
    uint32 DMAMPCTRL;
} dmaREG_in;

// �������� ������
// curr_config

static void set_test_in_data();
static void set_test_out_data();

void put_config_values
{
    PCP.ISADDR = PCP->ISADDR;
    PCP.IDADDR = PCP->IDADDR;
    PCP.ITCOUNT = PCP->ITCOUNT;
    PCP.CHCTRL = PCP->CHCTRL;
    PCP.EIOFF = PCP->EIOFF;
    PCP.FIOFF = PCP->FIOFF;
    dmaRAMREG_in.PCP[32] = dmaRAMREG->PCP[32]_in;
    dmaREG_in.GCTRL = dmaREG->GCTRL;
    dmaREG_in.SWCHENAS = dmaREG->SWCHENAS;
    dmaREG_in.CHPRIOS = dmaREG->CHPRIOS;
    dmaREG_in.GCHIENAS = dmaREG->GCHIENAS;
    dmaREG_in.DREQASI[8] = dmaREG->DREQASI[8];
    dmaREG_in.PAR[4] = dmaREG->PAR[4];
    dmaREG_in.FTCINTENAS = dmaREG->FTCINTENAS;
    dmaREG_in.LFSINTENAS = dmaREG->LFSINTENAS;
    dmaREG_in.HBCINTENAS = dmaREG->HBCINTENAS;
    dmaREG_in.BTCINTENAS = dmaREG->BTCINTENAS;
    dmaREG_in.DMAPCR = dmaREG->DMAPCR;
    dmaREG_in.DMAMPCTRL = dmaREG->DMAMPCTRL;
}

void get_config_values
{
    PCP->ISADDR = PCP.ISADDR;
    PCP->IDADDR = PCP.IDADDR;
    PCP->ITCOUNT = PCP.ITCOUNT;
    PCP->CHCTRL = PCP.CHCTRL;
    PCP->EIOFF = PCP.EIOFF;
    PCP->FIOFF = PCP.FIOFF;
    dmaRAMREG->PCP[32] = dmaRAMREG_in.PCP[32];
    dmaREG->GCTRL = dmaREG_in.GCTRL;
    dmaREG->SWCHENAS = dmaREG_in.SWCHENAS;
    dmaREG->CHPRIOS = dmaREG_in.CHPRIOS;
    dmaREG->GCHIENAS = dmaREG_in.GCHIENAS;
    dmaREG->DREQASI[8] = dmaREG_in.DREQASI[8];
    dmaREG->PAR[4] = dmaREG_in.PAR[4];
    dmaREG->FTCINTENAS = dmaREG_in.FTCINTENAS;
    dmaREG->LFSINTENAS = dmaREG_in.LFSINTENAS;
    dmaREG->HBCINTENAS = dmaREG_in.HBCINTENAS;
    dmaREG->BTCINTENAS = dmaREG_in.BTCINTENAS;
    dmaREG->DMAPCR = dmaREG_in.DMAPCR;
    dmaREG->DMAMPCTRL = dmaREG_in.DMAMPCTRL;
}


//--------------------------------------------------------------------
//      �������� �������
//--------------------------------------------------------------------
void main_test(void)
{
    InitDevice();

    //---------------------------------------------------------------------
    // ����������� ���� ������
    //---------------------------------------------------------------------
    while(1) 
    {
        // �������� ������� �� ��������� ��������� �� ���������� �����
        RequestRx();
        // �������� ������� ���������� ������ � ��������� �������
        set_test_in_data();
        // ��������� �������
        switch(test_number){
            case 1: //dmaEnable 
                dmaEnable();
            break;
            case 2: //dmaSetCtrlPacket 
                dmaSetCtrlPacket();
            break;
            case 3: //dmaSetSWChEnable 
                dmaSetSWChEnable();
            break;
        }
        // �������� �������� ���������� ������
        set_test_out_data();
        // �������� �������� ������ ������� � �������� ���������
        ResponseTx(); 
    }  
}
//-------------------------------------------------------------
//       ������ ������� ������
//-------------------------------------------------------------
static void set_test_in_data()
{
    SET_IN_DATA(&curr_config);
    SET_IN_DATA(&test_number);
    put_config_values();
}
//-------------------------------------------------------------
//             ������ �������� ������
//-------------------------------------------------------------
static void set_test_out_data()
{
    get_config_values();
    SET_OUT_DATA(&curr_config);
}
