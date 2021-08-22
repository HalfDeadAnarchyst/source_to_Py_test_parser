/** @file sys_pcr.c
*   @brief PCR Driver Implementation File
*   @date 24.Feb.2014
*   @version 03.08.01
*
*/
/* (c) Texas Instruments 2009-2014, All rights reserved. */

#include "sys_pcr.h"
#include "control.h"
#include "error.h"

#define PCR_PMPROTSET0_CONFIGVALUE     0
#define PCR_PMPROTSET1_CONFIGVALUE     0
#define PCR_PPROTSET0_CONFIGVALUE      0
#define PCR_PPROTSET1_CONFIGVALUE      0
#define PCR_PPROTSET2_CONFIGVALUE      0
#define PCR_PPROTSET3_CONFIGVALUE      0
#define PCR_PCSPWRDWNSET0_CONFIGVALUE  0
#define PCR_PCSPWRDWNSET1_CONFIGVALUE  0
#define PCR_PSPWRDWNSET0_CONFIGVALUE   0
#define PCR_PSPWRDWNSET1_CONFIGVALUE   0
#define PCR_PSPWRDWNSET2_CONFIGVALUE   0
#define PCR_PSPWRDWNSET3_CONFIGVALUE   0

#define PCR_PSPWRDWNCLR0_CONFIGVALUE   0xFFFFFFFFU  // PS07,PS06,PS05,PS04,PS03,PS02,PS01,PS00
#define PCR_PSPWRDWNCLR1_CONFIGVALUE   0xFFFFFFFFU  // PS15,PS14,PS13,PS12,PS11,PS10,PS09,PS08
#define PCR_PSPWRDWNCLR2_CONFIGVALUE   0xFFFFFFFFU  // PS23,PS22,PS21,PS20,PS19,PS18,PS17,PS16
#define PCR_PSPWRDWNCLR3_CONFIGVALUE   0xFFFFFFFFU  // PS31,PS30,PS29,PS28,PS27,PS26,PS25,PS24

void pcrInit(void)
{
    pcrREG->PSPWRDWNCLR0 = PCR_PSPWRDWNCLR0_CONFIGVALUE;
    pcrREG->PSPWRDWNCLR1 = PCR_PSPWRDWNCLR1_CONFIGVALUE;
    pcrREG->PSPWRDWNCLR2 = PCR_PSPWRDWNCLR2_CONFIGVALUE;
    pcrREG->PSPWRDWNCLR3 = PCR_PSPWRDWNCLR3_CONFIGVALUE;
}


void pcrInitialization(void)
{
    pcrInit();
    pcrCheckConfig();
}



/** @fn void pcrGetConfigValue(pcr_config_reg_t *config_reg, config_value_type_t type)
*   @brief Get the initial or current values of the configuration registers
*
*	@param[in] *config_reg: pointer to the struct to which the initial or current 
*                           value of the configuration registers need to be stored
*	@param[in] type: 	whether initial or current value of the configuration registers need to be stored
*						- InitialValue: initial value of the configuration registers will be stored 
*                                       in the struct pointed by config_reg
*						- CurrentValue: initial value of the configuration registers will be stored 
*                                       in the struct pointed by config_reg
*
*   This function will copy the initial or current value (depending on the parameter 'type') 
*   of the configuration registers to the struct pointed by config_reg
*
*/
/* SourceId : PCR_SourceId_021 */
/* DesignId : PCR_DesignId_021 */
/* Requirements : HL_SR61 */
void pcrGetConfigValue(pcr_config_reg_t *config_reg, config_value_type_t type)
{
	if (type == InitialValue)
	{
        config_reg->CONFIG_PMPROTSET0    = PCR_PMPROTSET0_CONFIGVALUE;
        config_reg->CONFIG_PMPROTSET1    = PCR_PMPROTSET1_CONFIGVALUE;
        config_reg->CONFIG_PPROTSET0     = PCR_PPROTSET0_CONFIGVALUE;
        config_reg->CONFIG_PPROTSET1     = PCR_PPROTSET1_CONFIGVALUE;
        config_reg->CONFIG_PPROTSET2     = PCR_PPROTSET2_CONFIGVALUE;
        config_reg->CONFIG_PPROTSET3     = PCR_PPROTSET3_CONFIGVALUE;
        config_reg->CONFIG_PCSPWRDWNSET0 = PCR_PCSPWRDWNSET0_CONFIGVALUE;
        config_reg->CONFIG_PCSPWRDWNSET1 = PCR_PCSPWRDWNSET1_CONFIGVALUE;
        config_reg->CONFIG_PSPWRDWNSET0  = PCR_PSPWRDWNSET0_CONFIGVALUE;
        config_reg->CONFIG_PSPWRDWNSET1  = PCR_PSPWRDWNSET1_CONFIGVALUE;
        config_reg->CONFIG_PSPWRDWNSET2  = PCR_PSPWRDWNSET2_CONFIGVALUE;
        config_reg->CONFIG_PSPWRDWNSET3  = PCR_PSPWRDWNSET3_CONFIGVALUE;
	}
	else
	{
        config_reg->CONFIG_PMPROTSET0    = pcrREG->PMPROTSET0;
        config_reg->CONFIG_PMPROTSET1    = pcrREG->PMPROTSET1;
        config_reg->CONFIG_PPROTSET0     = pcrREG->PPROTSET0;
        config_reg->CONFIG_PPROTSET1     = pcrREG->PPROTSET1;
        config_reg->CONFIG_PPROTSET2     = pcrREG->PPROTSET2;
        config_reg->CONFIG_PPROTSET3     = pcrREG->PPROTSET3;
        config_reg->CONFIG_PCSPWRDWNSET0 = pcrREG->PCSPWRDWNSET0;
        config_reg->CONFIG_PCSPWRDWNSET1 = pcrREG->PCSPWRDWNSET1;
        config_reg->CONFIG_PSPWRDWNSET0  = pcrREG->PSPWRDWNSET0;
        config_reg->CONFIG_PSPWRDWNSET1  = pcrREG->PSPWRDWNSET1;
        config_reg->CONFIG_PSPWRDWNSET2  = pcrREG->PSPWRDWNSET2;
        config_reg->CONFIG_PSPWRDWNSET3  = pcrREG->PSPWRDWNSET3;
	}
}


/*==========================================================================*/
void pcrCheckConfig(void)
{
    pcr_config_reg_t aInitConfig;
    pcr_config_reg_t aCurrConfig;
    sint32 aCmpResult;

    /* get pointers to structures with config data */
    pcrGetConfigValue(&aInitConfig, InitialValue);
    pcrGetConfigValue(&aCurrConfig, CurrentValue);
    /* compare structures */
    aCmpResult = controlCompareStructs((uint8*)&aInitConfig, (uint8*)&aCurrConfig, sizeof(pcr_config_reg_t));
    if (aCmpResult != -1)
    {
        errorRespondToEvent(ERROR_CAUSE_CONFIG_PCR, SYS_FAULT_DIAGNOSTIC, 0, (uint8)aCmpResult);
    }
}
