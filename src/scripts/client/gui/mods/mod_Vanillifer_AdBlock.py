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

			#from gui.Scaleform.daapi.view.lobby.hangar.craftmachine_entry_point import CraftMachineEntryPoint
			#from gui.impl.lobby.craft_machine.craftmachine_entry_point_view import CraftmachineEntryPointView
			#from gui.impl.gen.view_models.views.lobby.craft_machine.craftmachine_entry_point_view_model import CraftmachineEntryPointViewModel
			
			#def disabled_makeInjectView(self):
			#	_logger.info('Preventing Thunderstorm advert from being shown')
			#	self.__view = CraftmachineEntryPointView(0)
			#	return self.__view

			#CraftMachineEntryPoint._makeInjectView = disabled_makeInjectView

			_logger.info('Craftmachine promo have been disabled succesfully')
		except:
			_logger.error('Failed to disable Craftmachine')