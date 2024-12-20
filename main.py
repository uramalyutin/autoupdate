import utils
import yaml


def getSettings(filename):
    with open(filename) as stream:
        try:
            settings = yaml.safe_load(stream)
            logger.info(f'Прочитали настройки')
            logger.debug(f'Прочитанные настройки:')
            logger.debug(f'{settings}')
        except yaml.YAMLError as exc:
            logger.exception(f'Не смогли прочитать настройки из файла {exc}')
    return settings


#Подключим логирование
logger = utils.getLogger("main", "w")

#Прочитаем настройки из updater_settings.yaml
settings = getSettings("updater_settings.yaml")

#Создадим COM-коннектор
com_connector = utils.ComConnector()

if com_connector is not None:
    #Обойдём базы, с которыми будем работать
    infobases = settings.get('Infobases')
    for infobase in infobases:
        #Получим объект для работы с кластером
        onec = utils.OneC_Cluster(com_connector, infobase)
        onec_agent = onec.getAgent()
        onec_clusters = onec.getClusters()
        onec_workCluster = onec.getClusterWithPort(infobase.get('ServerPort'))
        if onec_workCluster is not None:
            onec_workingProcesses = onec.getWorkingProcesses()
            onec_infoBases = onec.getInfoBases()
        if onec_infoBases is not None:
            onec_infoBase = onec.getInfoBase()