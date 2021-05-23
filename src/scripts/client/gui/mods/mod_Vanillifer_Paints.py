import logging
import BigWorld

import string

def rgbToColorInt(rgbString):
  if not rgbString or str.isspace(rgbString):
    return None
  rgb = rgbString.split()
  if not len(rgb) == 4:
    return None
  rgb = map(int, rgb)
  #TODO switch to Math.Vector4 ?
  color = (rgb[3] << 24) + (rgb[2] << 16) + (rgb[1] << 8) + rgb[0]
  return color

def getPaintOverride(config, paintId, defaultPaint):
    paintId = str(paintId)
    return rgbToColorInt(config.tryGetValue('paintOverrides', paintId) or defaultPaint)

def OverridePaints(_logger, config):

    try:

        from items import vehicles
    
        defaultPaint = config.tryGetValue('paintOverrides', 'default', default = ';If specified its applied to all paints without specified override', saveDefault = True)

        #iterate paint dictionary
        for key, value in vehicles.g_cache.customization20().paints.iteritems():
  
            paintOverride = getPaintOverride(config, key, defaultPaint)
  
            #TODO switch to Math.Vector4 ?
            originalColorStr = [value.color & 255, value.color >> 8 & 255, value.color >> 16 & 255, value.color >> 24 & 255]
            originalColorStr = ' '.join(str(n) for n in originalColorStr)

            #store original values in config as a reference for user
            config.setValue('originalPaints', str(key), str(originalColorStr) + ';' +value.userString)
  
            #override paint
            if not paintOverride == None:
                value.color = paintOverride

        _logger.info('Paints have been overriden succesfully')
    except Exception as e:
        _logger.error('Failed to override paints')
        _logger.error(str(e))
