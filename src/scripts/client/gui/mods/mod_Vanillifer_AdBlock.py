import logging
import BigWorld

def isTimeToShowGoldFishPromo_AlwaysDisabled(self):
    return False

def AdBlock(_logger, config):

	if config.disableGoldfish():
		try:
	
			from gui import gold_fish

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