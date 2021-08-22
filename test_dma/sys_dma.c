#include "sys_dma.h"
#include "sys_vim.h"

/** @fn void dmaEnable(void)
*   @brief enables DMA module
*
*   This function brings DMA out of reset
*/
/* SourceId : DMA_SourceId_001 */
/* DesignId : DMA_DesignId_001 */
/* Requirements: HL_SR167 */
void dmaEnable(void)
{
    dmaREG->GCTRL  = 0x00000001U; /* reset dma       */
    dmaREG->GCTRL |= 0x00010000U; /* enable dma      */
    dmaREG->GCTRL |= 0x00000300U; /* stop at suspend */
}


/** @fn void dmaSetCtrlPacket(uint32 channel)
*   @brief Set control packet
*
*   This function sets control packet
*/
/* SourceId : DMA_SourceId_005 */
/* DesignId : DMA_DesignId_003 */
/* Requirements: HL_SR171 */
void dmaSetCtrlPacket(uint32 channel, T_DMA_CTRL* g_dmaCTRLPKT)
{
    uint32 i = 0U;
    uint32 j = 0U;

    dmaRAMREG->PCP[channel].ISADDR  =  g_dmaCTRLPKT->SADD;
    dmaRAMREG->PCP[channel].IDADDR  =  g_dmaCTRLPKT->DADD;
    dmaRAMREG->PCP[channel].ITCOUNT = (g_dmaCTRLPKT->FRCNT << 16U) | g_dmaCTRLPKT->ELCNT;
    dmaRAMREG->PCP[channel].CHCTRL  = (g_dmaCTRLPKT->RDSIZE    << 14U) | (g_dmaCTRLPKT->WRSIZE    << 12U) | (g_dmaCTRLPKT->TTYPE << 8U)| \
                                      (g_dmaCTRLPKT->ADDMODERD << 3U ) | (g_dmaCTRLPKT->ADDMODEWR << 1U ) | (g_dmaCTRLPKT->AUTOINIT);
    dmaRAMREG->PCP[channel].CHCTRL |= (g_dmaCTRLPKT->CHCTRL << 16U);
    dmaRAMREG->PCP[channel].EIOFF   = (g_dmaCTRLPKT->ELDOFFSET << 16U) | (g_dmaCTRLPKT->ELSOFFSET);
    dmaRAMREG->PCP[channel].FIOFF   = (g_dmaCTRLPKT->FRDOFFSET << 16U) | (g_dmaCTRLPKT->FRSOFFSET);

    i = channel >> 3U;                /* Find the register to write                    */
    j = channel - (i << 3U);          /* Find the offset of the 4th bit                */
    j = 7U - j;                       /* Reverse the order of the 4th bit offset       */
    j = j << 2U;                      /* Find the bit location of the 4th bit to write */

    dmaREG->PAR[i] &= ~(uint32)((uint32)0xFU << j);
    dmaREG->PAR[i] |= (g_dmaCTRLPKT->PORTASGN << j);
}


/** @fn void dmaSetChEnable(uint32 channel,uint32 type)
*   @brief Enable channel
*   @param[in] channel DMA channel
*   @param[in] type Type of triggering
*                    - DMA_HW: Enables the selected DMA channel for hardware triggering
*                    - DMA_SW: Enables the selected DMA channel for software triggering
*
*   This function enables the DMA channel for hardware or software triggering
*/
/* SourceId : DMA_SourceId_006 */
/* DesignId : DMA_DesignId_004 */
/* Requirements: HL_SR172 */
void dmaSetSWChEnable(uint32 f_channel)
{
    dmaREG->SWCHENAS = (uint32)1U << f_channel;
}


/** @fn void dmaGetConfigValue(dma_config_reg_t *config_reg, config_value_type_t type)
*   @brief Get the initial or current values of the configuration registers
*
*   @param[in] *config_reg: pointer to the struct to which the initial or current
*                           value of the configuration registers need to be stored
*   @param[in] type:    whether initial or current value of the configuration registers need to be stored
*                       - InitialValue: initial value of the configuration registers will be stored
*                                       in the struct pointed by config_reg
*                       - CurrentValue: initial value of the configuration registers will be stored
*                                       in the struct pointed by config_reg
*
*   This function will copy the initial or current value (depending on the parameter 'type')
*   of the configuration registers to the struct pointed by config_reg
*
*/
/* SourceId : DMA_SourceId_015 */
/* DesignId : DMA_DesignId_015 */
/* Requirements: HL_SR183 */
void dmaGetConfigValue(dma_config_reg_t *config_reg, config_value_type_t type)
{
    if (type == InitialValue)
    {/* Do not pass Initial value as parameter as there is no DMA initialization API */
    }
    else
    {
        dmaREG_in->CONFIG_CHPRIOS     = dmaREG->CHPRIOS;
        dmaREG_in->CONFIG_GCHIENAS    = dmaREG->GCHIENAS;
        dmaREG_in->CONFIG_DREQASI[0U] = dmaREG->DREQASI[0U];
        dmaREG_in->CONFIG_DREQASI[1U] = dmaREG->DREQASI[1U];
        dmaREG_in->CONFIG_DREQASI[2U] = dmaREG->DREQASI[2U];
        dmaREG_in->CONFIG_DREQASI[3U] = dmaREG->DREQASI[3U];
        dmaREG_in->CONFIG_DREQASI[4U] = dmaREG->DREQASI[4U];
        dmaREG_in->CONFIG_DREQASI[5U] = dmaREG->DREQASI[5U];
        dmaREG_in->CONFIG_DREQASI[6U] = dmaREG->DREQASI[6U];
        dmaREG_in->CONFIG_DREQASI[7U] = dmaREG->DREQASI[7U];
        dmaREG_in->CONFIG_FTCINTENAS  = dmaREG->FTCINTENAS;
        dmaREG_in->CONFIG_LFSINTENAS  = dmaREG->LFSINTENAS;
        dmaREG_in->CONFIG_HBCINTENAS  = dmaREG->HBCINTENAS;
        dmaREG_in->CONFIG_BTCINTENAS  = dmaREG->BTCINTENAS;
        dmaREG_in->CONFIG_DMAPCR      = dmaREG->DMAPCR;
        dmaREG_in->CONFIG_DMAMPCTRL   = dmaREG->DMAMPCTRL;
    }
}

//--- end ---
