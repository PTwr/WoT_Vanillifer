import logging
import BigWorld


def DisableBadges(_logger, config):

	if not config.disableBadges:
		return

	try:

		from gui.doc_loaders import badges_loader

		_readBadges_disabled_original = badges_loader._readBadges
		def _readBadges_disabled():
			result = _readBadges_disabled_original()
			# allow bot badge
			result = dict((k, v) for (k, v) in result.iteritems() if config.tryGetValue('badges', v['name'], default = '').lower() == 'allow')
			return result

		badges_loader._readBadges = _readBadges_disabled

		_logger.info('Badges have been disabled succesfully')
	except:
		_logger.error('Failed to disable badges')
