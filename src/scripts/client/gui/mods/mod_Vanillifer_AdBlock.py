import logging
import BigWorld

def AdBlock(_logger, config):

	if config.adblockWhitelistEnabled():
		try:			
			from gui.Scaleform.daapi.view.lobby.hangar import event_entry_points_container

			_logger.info("Applying AdBlock whitelist")

			whitelist = config.adblockWhitelist()
			newDict = dict()
			_logger.info(whitelist)

			for (key, value) in event_entry_points_container._ENTRY_POINT_ENABLED_VALIDATOR.iteritems():
				if key in whitelist:
					_logger.info("Allowing entry point for " + key)
					newDict[key] = value
				else:
					_logger.info("Removing entry point for " + key)

			event_entry_points_container._ENTRY_POINT_ENABLED_VALIDATOR = newDict
			
		except Exception as e:
			_logger.error('Failed to apply whitelist')
			_logger.error(e)

	if config.disableGoldfish():
		try:
	
			from gui import gold_fish

			def isTimeToShowGoldFishPromo_AlwaysDisabled(self):
				return False

			gold_fish.isTimeToShowGoldFishPromo = isTimeToShowGoldFishPromo_AlwaysDisabled

			_logger.info('GoldFish promo have been disabled succesfully')
		except:
			_logger.error('Failed to disable GoldFish')

	if config.disableCraftmachine():
		try:
	
			from gui.game_control import craftmachine_controller

			def getCraftMachineEntryPointIsActive_alwaysDisabled(craftMachineController=None):
				return False

			craftmachine_controller.getCraftMachineEntryPointIsActive = getCraftMachineEntryPointIsActive_alwaysDisabled

			_logger.info('Craftmachine promo have been disabled succesfully')
		except:
			_logger.error('Failed to disable Craftmachine')

	if config.disableMapBox():
		try:
	
			from gui.impl.lobby.mapbox import mapbox_entry_point_view 

			def mapBoxEntryPointIsActive_alwaysDisabled(craftMachineController=None):
				return False

			mapbox_entry_point_view.isMapboxEntryPointAvailable = mapBoxEntryPointIsActive_alwaysDisabled

			_logger.info('MapBox promo have been disabled succesfully')
		except:
			_logger.error('Failed to disable MapBox')