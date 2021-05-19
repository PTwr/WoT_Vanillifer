import logging
from items import vehicles, tankmen, EQUIPMENT_TYPES, ItemsPrices
import os
from ConfigParser import ConfigParser
import BigWorld
from helpers import getFullClientVersion, getShortClientVersion, getClientVersion

import importlib
import ResMgr
import string
from items.components.shared_components import ModelStatesPaths

import nations
from items.components import path_builder

from helpers.server_settings import ServerSettings

from gui.doc_loaders import badges_loader

from helpers import EdgeDetectColorController
import Math

_logger = logging.getLogger(__name__)
_logger.info('Vanilifer v1.2.0')

def TryGetConfigValue(section, field):
  if config.has_option(section, field):
    return config.get(section, field)
  return None

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
  mode = (TryGetConfigValue(silhouetteColors, 'mode') or '').lower()

  Self, Enemy, Friend, Flag, Hangar = TryGetConfigValue(silhouetteColors, 'self'),TryGetConfigValue(silhouetteColors, 'enemy'),TryGetConfigValue(silhouetteColors, 'friend'),TryGetConfigValue(silhouetteColors, 'flag'),TryGetConfigValue(silhouetteColors, 'hangar'),

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
  result = dict((k, v) for (k, v) in result.iteritems() if v['name'] == 'ai_bot')
  return result

def isDogTagEnabled_AlwaysDisabled(self):
    return False
def GetModsDirectory():
  paths = '../paths.xml'
  paths = ResMgr.openSection(paths)
  moddir = os.path.join(os.getcwd(), paths['Paths'].values()[1].readString(''))
  moddir = moddir.replace('\\./','\\')
  return moddir
  
def rgbToColorInt(rgbString):
  if rgbString == None or str.isspace(rgbString):
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
  if config.has_option('paintOverrides', paintId):
    return rgbToColorInt(config.get('paintOverrides', paintId))
  else:
    return rgbToColorInt(defaultPaint)

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

cwd = os.getcwd()

configFileName = 'Vanillifer.ini'
configDirectory = os.path.join(cwd, 'mods', 'config')
configFile = os.path.join(configDirectory, configFileName)
localConfigFile = os.path.join(GetModsDirectory(), configFileName)
try: 
    os.makedirs(configDirectory)
except OSError:
    if not os.path.isdir(configDirectory):
        raise

config = ConfigParser()
config.optionxform=str

#prioritize config outside of versioned directory
if os.path.isfile(configFile):
  _logger.info('Reading Vanillifer config from '+configFile)
  config.read(configFile)
#try to load bundled config if no global present
elif os.path.isfile(localConfigFile):
  _logger.info('Reading Vanillifer config from '+localConfigFile)
  config.read(localConfigFile)

sections = config.sections()
if not 'silhouetteColors' in sections:
  config.add_section('silhouetteColors')
if not 'dogtags' in sections:
  config.add_section('dogtags')
if not 'badges' in sections:
  config.add_section('badges')
if not 'modelOverrides' in sections:
  config.add_section('modelOverrides')
if not 'camouflageOverrides' in sections:
  config.add_section('camouflageOverrides')
if not 'styleOverrides' in sections:
  config.add_section('styleOverrides')
if not 'paintOverrides' in sections:
  config.add_section('paintOverrides')
  
if not 'originalModels' in sections:
  config.add_section('originalModels')
if not 'originalCamouflages' in sections:
  config.add_section('originalCamouflages')
if not 'originalStyles' in sections:
  config.add_section('originalStyles')
if not 'originalPaints' in sections:
  config.add_section('originalPaints')
  
if config.has_option('dogtags', 'disable') and config.get('dogtags', 'disable').lower() == "true":
  _logger.info('Disabling dogtags')
  ServerSettings.isDogTagEnabled = isDogTagEnabled_AlwaysDisabled
  
if config.has_option('badges', 'disable') and config.get('badges', 'disable').lower() == "true":
  _logger.info('Disabling badges')
  badges_loader._readBadges = _readBadges_disabled

if config.has_option('paintOverrides', 'default'):
  defaultPaint = config.get('paintOverrides', 'default') 
else:
  config.set('paintOverrides', 'default', ';If specified its applied to all paints without specified override')
  defaultPaint = None

for nationName in nations.NAMES:
  nationId = nations.NAMES.index(nationName)
  for vehicleId in vehicles.g_list.getList(nationId):
    vehicle = vehicles.g_cache.vehicle(nationId, vehicleId)
    vehicleName = vehicle.name.replace(' = ', ':').split(':')[1]
    config.set('originalModels', vehicleName, vehicle.userString)
    
    if config.has_option('modelOverrides', vehicleName):
      replacement = config.get('modelOverrides', vehicleName)
      replacement = replacement.split(';')[0].strip() #ignore inline comment
      replacement = replacement.strip() #trim whitespace
      _logger.info('Replacing '+vehicleName+' with '+ replacement)
      _logger.info('vehicleId: '+str(vehicleId)+' nationId: '+str(nationId))
      SwitchTankModels(vehicle, vehicleName, replacement)
  
defaultCamo = None
if config.has_option('camouflageOverrides', 'default'):
  try:
    defaultCamo = int(config.get('camouflageOverrides', 'default'))
  except:
    _logger.error('Default for camouflageOverrides must be integer value')
    defaultCamo = None
    
defaultStyle = None
if config.has_option('styleOverrides', 'default'):
  try:
    defaultStyle = int(config.get('styleOverrides', 'default'))
  except:
    _logger.error('Default for styleOverrides must be integer value')
    defaultStyle = None
    
##nocamo
transparentCamouflage = vehicles.g_cache.customization20().camouflages[1]
camoKeys = vehicles.g_cache.customization20().camouflages.keys()
for key in camoKeys:
  config.set('originalCamouflages', str(key), vehicles.g_cache.customization20().camouflages[key].userString)
  
  override = None
  if config.has_option('camouflageOverrides', str(key)):
    try:
      s = config.get('camouflageOverrides', str(key))
      s = s.split(';')[0].strip()
      if s.lower() == 'allow':
        continue
      override = int(s)
      override = int(config.get('camouflageOverrides', str(key)))
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
  config.set('originalStyles', str(value.id), value.userString)
  
  override = None
  if config.has_option('styleOverrides', str(value.id)):
    try:
      s = config.get('styleOverrides', str(value.id))
      s = s.split(';')[0].strip()
      if s.lower() == 'allow':
        continue
      override = int(s)
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
  config.set('originalPaints', str(key), str(originalColorStr) + ';' +value.userString)
  
  if not paintOverride == None:
    value.color = paintOverride

OverrideSilhouetteColors()

with open(configFile, 'w') as updatedConfig:
  _logger.info('Writing Vanillifer config to '+configFile)
  config.write(updatedConfig)