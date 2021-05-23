import logging
import BigWorld

import string


def SwitchModel(models, current, replacement):
    from items.components.shared_components import ModelStatesPaths

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
  
def ApplyModelOverrides(_logger, config):

    try:
        import nations
        from items import vehicles

        for nationName in nations.NAMES:
            nationId = nations.NAMES.index(nationName)
            for vehicleId in vehicles.g_list.getList(nationId):
                vehicle = vehicles.g_cache.vehicle(nationId, vehicleId)
                vehicleName = vehicle.name.replace(' = ', ':').split(':')[1]
                config.setValue('originalModels', vehicleName, vehicle.userString)
    
                replacement = config.tryGetValue('modelOverrides', vehicleName)
                if replacement:
                    _logger.info('Replacing '+vehicleName+' with '+ replacement)
                    _logger.info('vehicleId: '+str(vehicleId)+' nationId: '+str(nationId))
                    SwitchTankModels(vehicle, vehicleName, replacement)

        _logger.info('Applied model overrides succesfully')
    except:
        _logger.error('Failed to apply model overrides')