import logging
import BigWorld

import string

def ApplyCamouflageOverrides(_logger, config):

    try:
        from items import vehicles

        defaultCamo = config.tryGetValue('camouflageOverrides', 'default')
        if defaultCamo:
            try:
                defaultCamo = int(defaultCamo)
            except:
                _logger.error('Default for camouflageOverrides must be integer value')
                defaultCamo = None

        transparentCamouflage = vehicles.g_cache.customization20().camouflages[1]
        camoKeys = vehicles.g_cache.customization20().camouflages.keys()
        for key in camoKeys:
            config.setValue('originalCamouflages', str(key), vehicles.g_cache.customization20().camouflages[key].userString)
  
            override = config.tryGetValue('camouflageOverrides', str(key))
            if override:
                try:
                    if override.lower() == 'allow':
                        continue
                    override = int(override)
                except:
                    _logger.error('camouflageOverrides for #' + str(key) + ' must be integer value')
                    override = None
            override = override or defaultCamo
  
            if override:
                try:
                    vehicles.g_cache.customization20().camouflages[key] = vehicles.g_cache.customization20().camouflages[override]
                except Exception as e:
                    _logger.error('Failed to apply camouflage override for #' + str(key))
                    _logger.error(str(e))

        _logger.info('Camouflage overrides have been succesfully')
    except:
        _logger.error('Failed apply camouflage overrides')
