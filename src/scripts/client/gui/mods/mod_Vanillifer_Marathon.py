import logging
import BigWorld

def VanillifyMarathon(_logger, advert, music):
	_logger.info('Vanillifying Marathon')

	if advert:
		try:

			from gui.Scaleform.daapi.view.lobby.marathon.marathon_entry_point import MarathonEntryPointWrapper
  
			#from frameworks.wulf import ViewFlags #parameter for MarathonEntryPoint flags
			def disabled_makeInjectView(self):
				_logger.info('Preventing marathon advert from being shown')
				self._MarathonEntryPointWrapper__view = MarathonEntryPoint(flags=0)
				return self._MarathonEntryPointWrapper__view

			MarathonEntryPointWrapper._makeInjectView = disabled_makeInjectView

			_logger.info('Vanillified Marathon advert')

		except:
			_logger.error('Failed to vanillify marathon advert')

	if music:
		try:

			from gui.sounds.filters import WWISEMarathonPageFilter

			def start_empty(self):
				_logger.info('Preventing marathon background music from being played')
				pass

			WWISEMarathonPageFilter.start = start_empty

			_logger.info('Vanillified Marathon background music')
		except:
			_logger.error('Failed to vanillify marathon background music')