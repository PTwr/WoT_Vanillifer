import logging
import BigWorld

def DisableProgressiveDecalPopups(_logger, config):

    #if not config.disableProgressiveDecalPopups():
    #	return

    try:

        #from gui.shared import event_dispatcher 

        def showProgressiveRewardAwardWindow_disabled(bonuses, specialRewardType, currentStep, notificationMgr=None):
          _logger.info('showProgressiveRewardAwardWindow_disabled')
          pass
        def showProgressiveRewardWindow_disabled(bonuses, specialRewardType, currentStep, notificationMgr=None):
          _logger.info('showProgressiveRewardWindow_disabled')
          pass

        #not working
        #event_dispatcher.showProgressiveRewardAwardWindow = showProgressiveRewardAwardWindow_disabled
        #event_dispatcher.showProgressiveRewardWindow = showProgressiveRewardWindow_disabled

        #_logger.info('Progressive decal popups have been disabled succesfully')
    except:
        _logger.error('Failed to disable Progressive decal popups')
