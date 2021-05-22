import logging
import BigWorld
import string
from ConfigParser import ConfigParser
import ResMgr
import os

from mod_Vanillifer_Config_Default import applyDefaultConfig

def GetModsDirectory():
  paths = '../paths.xml'
  paths = ResMgr.openSection(paths)
  moddir = os.path.join(os.getcwd(), paths['Paths'].values()[1].readString(''))
  moddir = moddir.replace('\\./','\\')
  return moddir

class VanilliferConfig():

    def __init__(self, _logger):

        self._logger = _logger

        self.configFile, localConfigFile = self.prepareFile()

        self.config = ConfigParser()
        self.config.optionxform = str

        self.readConfig(localConfigFile)

        self.prepareSections()

    def readConfig(self, localConfigFile):
        #prioritize config outside of versioned directory
        if os.path.isfile(self.configFile):
            self._logger.info('Reading Vanillifer config from ' + self.configFile)
            self.config.read(self.configFile)
        #try to load bundled config if no global present
        elif os.path.isfile(localConfigFile):
            self._logger.info('Reading Vanillifer config from ' + localConfigFile)
            self.config.read(localConfigFile)
        else:
            applyDefaultConfig(self._logger, self)

    def prepareFile(self):
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

        return configFile, localConfigFile

    def prepareSections(self):
        sections = self.config.sections()
        
        self.ensureSectionExists('silhouetteColors')

        self.ensureSectionExists('dogtags')
        self.ensureSectionExists('badges')
        self.ensureSectionExists('marathon')
        
        self.ensureSectionExists('modelOverrides')
        self.ensureSectionExists('camouflageOverrides')
        self.ensureSectionExists('styleOverrides')
        self.ensureSectionExists('paintOverrides')
        
        self.ensureSectionExists('originalModels')
        self.ensureSectionExists('originalCamouflages')
        self.ensureSectionExists('originalStyles')
        self.ensureSectionExists('originalPaints')

    def boolValue(self, section, field):
      return self.tryGetValue(section, field, default = 'false').lower() == "true"
    def tryGetValue(self, section, field, default = None, saveDefault = False):
        if self.config.has_option(section, field):
            result = self.config.get(section, field)
        else:
            if saveDefault:
                self.setValue(section, field, default)
            result = default

        #ignore nonstandard inline comment
        if result:
            result = result.split(';')[0].strip()

        return result

    def ensureSectionExists(self, section): 
        if not section in self.config.sections():
            self.config.add_section(section)

    def setValue(self, section, field, value):        
        self.ensureSectionExists(section)
        self.config.set(section, field, value)
      
    def disableMarathonAdvertBox(self):
        return self.boolValue('marathon', 'hideAdvert')
    def disableMarathonBackgroundMusic(self):
        return self.boolValue('marathon', 'disableMusic')

    def disableDogTags(self):
        return self.boolValue('dogtags', 'disable')
    def disableBadges(self):
        return self.boolValue('badges', 'disable')

    def saveConfig(self):
        with open(self.configFile, 'w') as updatedConfig:
            self._logger.info('Writing Vanillifer config to ' + self.configFile)
            self.config.write(updatedConfig)