import logging
import BigWorld

from helpers import EdgeDetectColorController
import Math

def SetSilhuetteColor(_logger, mode, category, value):
  if not value:
    return
  color = value.split()
  color = map(float, color)
  color = Math.Vector4(color[0], color[1], color[2], color[3])
  EdgeDetectColorController.g_instance._EdgeDetectColorController__colors[mode][category] = color

def OverrideSilhouetteColors(_logger, config):
    try:
        silhouetteColors = 'silhouetteColors'
        mode = (config.tryGetValue(silhouetteColors, 'mode') or '').lower()

        Self, Enemy, Friend, Flag, Hangar = config.tryGetValue(silhouetteColors, 'self'),config.tryGetValue(silhouetteColors, 'enemy'),config.tryGetValue(silhouetteColors, 'friend'),config.tryGetValue(silhouetteColors, 'flag'),config.tryGetValue(silhouetteColors, 'hangar'),

        if mode == 'common' or mode == 'colorBlind':
            SetSilhuetteColor(_logger, mode, 'self', Self)
            SetSilhuetteColor(_logger, mode, 'enemy', Enemy)
            SetSilhuetteColor(_logger, mode, 'friend', Friend)
            SetSilhuetteColor(_logger, mode, 'flag', Flag)
            SetSilhuetteColor(_logger, mode, 'hangar', Hangar)
            EdgeDetectColorController.g_instance.updateColors()
            _logger.info('Silhuette color overrides applied for ' + mode + ' settings')

    except:
        _logger.error('Failed to apply silhuette color overrides')