import logging
import BigWorld

from items import vehicles, tankmen, EQUIPMENT_TYPES, ItemsPrices
import os
from ConfigParser import ConfigParser
from helpers import getFullClientVersion, getShortClientVersion, getClientVersion

import importlib
import string
from items.components.shared_components import ModelStatesPaths

import nations


_logger = logging.getLogger(__name__)
_logger.info('Vanillifer v1.2.3 - "Simplicity"')

from mod_Vanillifer_Config import VanilliferConfig
from mod_Vanillifer_Marathon import VanillifyMarathon
from mod_Vanillifer_Silhuette import OverrideSilhouetteColors
from mod_Vanillifer_Badges import DisableBadges
from mod_Vanillifer_DogTags import DisableDogTags
from mod_Vanillifer_Paints import OverridePaints
from mod_Vanillifer_ProgressiveDecals import DisableProgressiveDecalPopups
from mod_Vanillifer_Camouflage import ApplyCamouflageOverrides
from mod_Vanillifer_Styles import ApplyStyleOverrides
from mod_Vanillifer_Models import ApplyModelOverrides

config = VanilliferConfig(_logger)

VanillifyMarathon(_logger, config.disableMarathonAdvertBox(), config.disableMarathonBackgroundMusic())

OverrideSilhouetteColors(_logger, config)

DisableBadges(_logger, config)

OverridePaints(_logger, config)

DisableProgressiveDecalPopups(_logger, config)

ApplyCamouflageOverrides(_logger, config)

ApplyStyleOverrides(_logger, config)

ApplyModelOverrides(_logger, config)

DisableDogTags(_logger, config)

config.saveConfig()