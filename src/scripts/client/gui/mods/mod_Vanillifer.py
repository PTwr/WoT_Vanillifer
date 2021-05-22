import logging
from items import vehicles, tankmen, EQUIPMENT_TYPES, ItemsPrices
import os
from ConfigParser import ConfigParser
import BigWorld
from helpers import getFullClientVersion, getShortClientVersion, getClientVersion

import importlib
import string
from items.components.shared_components import ModelStatesPaths

import nations
from items.components import path_builder

from helpers.server_settings import ServerSettings

from gui.doc_loaders import badges_loader

from helpers import EdgeDetectColorController
import Math

_logger = logging.getLogger(__name__)
_logger.info('Vanillifer v1.2.2')

from mod_Vanillifer_Config import VanilliferConfig
from mod_Vanillifer_Marathon import VanillifyMarathon

config = VanilliferConfig(_logger)

VanillifyMarathon(_logger, config.disableMarathonAdvertBox(), config.disableMarathonBackgroundMusic())

from gui.shared import event_dispatcher 

def showProgressiveRewardAwardWindow_disabled(bonuses, specialRewardType, currentStep, notificationMgr=None):
  _logger.info('showProgressiveRewardAwardWindow_disabled')
  pass
def showProgressiveRewardWindow_disabled(bonuses, specialRewardType, currentStep, notificationMgr=None):
  _logger.info('showProgressiveRewardWindow_disabled')
  pass

#not working
#event_dispatcher.showProgressiveRewardAwardWindow = showProgressiveRewardAwardWindow_disabled
#event_dispatcher.showProgressiveRewardWindow = showProgressiveRewardWindow_disabled

def SetSilhuetteColor(mode, category, value):
  if value == None or value == '':
    return
  color = value.split()
  #color = map(str.strip(), color)
  color = map(float, color)
  color = Math.Vector4(color[0], color[1], color[2], color[3])
  EdgeDetectColorController.g_instance._EdgeDetectColorController__colors[mode][category] = color

def OverrideSilhouetteColors():
  silhouetteColors = 'silhouetteColors'
  mode = (config.tryGetValue(silhouetteColors, 'mode') or '').lower()

  Self, Enemy, Friend, Flag, Hangar = config.tryGetValue(silhouetteColors, 'self'),config.tryGetValue(silhouetteColors, 'enemy'),config.tryGetValue(silhouetteColors, 'friend'),config.tryGetValue(silhouetteColors, 'flag'),config.tryGetValue(silhouetteColors, 'hangar'),

  if mode == 'common' or mode == 'colorBlind':
    SetSilhuetteColor(mode, 'self', Self)
    SetSilhuetteColor(mode, 'enemy', Enemy)
    SetSilhuetteColor(mode, 'friend', Friend)
    SetSilhuetteColor(mode, 'flag', Flag)
    SetSilhuetteColor(mode, 'hangar', Hangar)

  EdgeDetectColorController.g_instance.updateColors()

_readBadges_disabled_original = badges_loader._readBadges
def _readBadges_disabled():
  result = _readBadges_disabled_original()
  # allow bot badge
  result = dict((k, v) for (k, v) in result.iteritems() if config.tryGetValue('badges', v['name'], default = '').lower() == 'allow')
  return result

def isDogTagEnabled_AlwaysDisabled(self):
    return False
  
def rgbToColorInt(rgbString):
  if not rgbString or str.isspace(rgbString):
    return None    
  rgb = rgbString.split(';')[0] #ignore inline comment
  rgb = rgb.strip()
  rgb = rgb.split()
  if not len(rgb) == 4:
    return None
  rgb = map(int, rgb)
  color = (rgb[3] << 24) + (rgb[2] << 16) + (rgb[1] << 8) + rgb[0]
  return color

def getPaintOverride(config, paintId):
    paintId = str(paintId)
    return rgbToColorInt(config.tryGetValue('paintOverrides', paintId) or defaultPaint)

def SwitchModel(models, current, replacement):
  undamaged = models.undamaged.replace(current, replacement)
  destroyed = models.destroyed.replace(current, replacement)
  exploded = models.exploded.replace(current, replacement)
  return ModelStatesPaths(undamaged, destroyed, exploded)

def SwitchTankModels(models, current, replacement):
  for hull in models.hulls:
    hull.models = SwitchModel(hull.models, current, replacement)
  for chassis in models.chassis:
    chassis.models = SwitchModel(chassis.models, current, replacement)
  for turrets in models.turrets:
    for turret in turrets:
      turret.models = SwitchModel(turret.models, current, replacement)
      for gun in turret.guns:
        gun.models = SwitchModel(gun.models, current, replacement)
  
if config.disableDogTags:
  _logger.info('Disabling dogtags')
  ServerSettings.isDogTagEnabled = isDogTagEnabled_AlwaysDisabled
  
if config.disableBadges:
  _logger.info('Disabling badges')
  badges_loader._readBadges = _readBadges_disabled

defaultPaint = config.tryGetValue('paintOverrides', 'default', default = ';If specified its applied to all paints without specified override', saveDefault = True)

for nationName in nations.NAMES:
  nationId = nations.NAMES.index(nationName)
  for vehicleId in vehicles.g_list.getList(nationId):
    vehicle = vehicles.g_cache.vehicle(nationId, vehicleId)
    vehicleName = vehicle.name.replace(' = ', ':').split(':')[1]
    config.setValue('originalModels', vehicleName, vehicle.userString)
    
    replacement = config.tryGetValue('modelOverrides', vehicleName)
    if replacement:
      _logger.info('Replacing '+vehicleName+' with '+ replacement)
      _logger.info('vehicleId: '+str(vehicleId)+' nationId: '+str(nationId))
      SwitchTankModels(vehicle, vehicleName, replacement)
  
defaultCamo = config.tryGetValue('camouflageOverrides', 'default')
if defaultCamo:
  try:
    defaultCamo = int(defaultCamo)
  except:
    _logger.error('Default for camouflageOverrides must be integer value')
    defaultCamo = None
    
defaultStyle = config.tryGetValue('styleOverrides', 'default')
if defaultStyle:
  try:
    defaultStyle = int(defaultStyle)
  except:
    _logger.error('Default for styleOverrides must be integer value')
    defaultStyle = None
    
##nocamo
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
  
_logger.info('styles')
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

_logger.info('paints')
for key, value in vehicles.g_cache.customization20().paints.iteritems():
  
  paintOverride = getPaintOverride(config, key)
  
  originalColorStr = [value.color & 255, value.color >> 8 & 255, value.color >> 16 & 255, value.color >> 24 & 255]
  originalColorStr = ' '.join(str(n) for n in originalColorStr)
  config.setValue('originalPaints', str(key), str(originalColorStr) + ';' +value.userString)
  
  if not paintOverride == None:
    value.color = paintOverride

OverrideSilhouetteColors()

config.saveConfig()