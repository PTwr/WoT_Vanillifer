import logging
import BigWorld

import string

def ApplyStyleOverrides(_logger, config):

    try:

        from items import vehicles

        defaultStyle = config.tryGetValue('styleOverrides', 'default')
        if defaultStyle:
            try:
                defaultStyle = int(defaultStyle)
            except:
                _logger.error('Default for styleOverrides must be integer value')
                defaultStyle = None
                        
        for value in vehicles.g_cache.customization20().styles.itervalues():
            config.setValue('originalStyles', str(value.id), value.userString)
  
            override = config.tryGetValue('styleOverrides', str(value.id))
            if override:
                try:
                    if override.lower() == 'allow':
                        continue
                    override = int(override)
                except:
                    _logger.error('styleOverrides for #' + str(value.id) + ' must be integer value')
                    override = None
            override = override or defaultStyle
  
            if override:
                try:
                    #remove modelSet
                    value.modelsSet = ''
                    #remove style
                    for outfitid in value.outfits:
                        outift = value.outfits[outfitid]
                        for camo in outift.camouflages:
                            camo.id = override
                        outift.paints = []
                        outift.decals = []
                        outift.projection_decals = []
                        outift.personal_numbers = []
                except Exception as e:
                    _logger.error('Failed to apply style override for #' + str(key))
                    _logger.error(str(e))

        _logger.info('Style overrides have been succesfully')
    except Exception as e:
        _logger.error('Failed apply style overrides')
        _logger.error(str(e))
