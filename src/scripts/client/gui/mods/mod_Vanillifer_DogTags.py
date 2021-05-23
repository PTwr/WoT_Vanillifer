import logging
import BigWorld

def isDogTagEnabled_AlwaysDisabled(self):
    return False

def DisableDogTags(_logger, config):

	if not config.disableDogTags:
		return

	try:
	
		from helpers.server_settings import ServerSettings

		ServerSettings.isDogTagEnabled = isDogTagEnabled_AlwaysDisabled

		_logger.info('DogTags have been disabled succesfully')
	except:
		_logger.error('Failed to disable DogTags')
