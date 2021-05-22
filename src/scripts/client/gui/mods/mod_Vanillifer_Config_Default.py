import logging
import BigWorld
import string
from ConfigParser import ConfigParser
import ResMgr
import os

def applyDefaultConfig(_logger, config):
    _logger.info('Setting default values')

    config.setValue('marathon', 'hideAdvert', 'true')
    config.setValue('marathon', 'disableMusic', 'true')

    config.setValue('dogtags', 'disable', 'true')

    config.setValue('badges', 'disable', 'true')
    config.setValue('badges', 'ai_bot', 'allow')
    
    config.setValue('modelOverrides', 'A117_T26E5_Patriot', 'A117_T26E5')
    config.setValue('modelOverrides', 'Ch01_Type59_Gold', 'Ch01_Type59')
    config.setValue('modelOverrides', 'Ch41_WZ_111_QL', 'Ch41_WZ_111_5A')
    config.setValue('modelOverrides', 'F74_AMX_M4_1949_Liberte', 'F74_AMX_M4_1949')

    config.setValue('paintOverrides', 'default', '79 73 52 255; Applied to all paints without specified override')