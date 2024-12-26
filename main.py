import utils
import yaml
import datetime


def getSettings(filename):
    settings = None
    with open(filename) as stream:
        try:
            settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.exception(f'Не смогли прочитать настройки из файла, по причине: {exc}')
            return settings
        else:
            logger.info(f'Прочитали настройки')
            logger.debug(f'Прочитанные настройки:')
            logger.debug(f'{settings}')
            return settings


# Подключим логирование
logger = utils.getLogger("main", "w")

# Получим COM-коннектор
connector = utils.ComConnector()

# Прочитаем настройки из updater_settings.yaml
settings = getSettings("updater_settings.yaml")

clusters = settings.get('Clusters')
for cluster in clusters:    
    # Получим объект для работы с кластером 1С
    onec = utils.OneC_Server(cluster, connector)
    
    # Получим агента сервера 1С
    onec_agent = onec.getAgent()
    
    # Получим кластеры 
    onec_clusters = onec.getAllClusters()
    
    # Получим кластер с нужным нам портом
    onec_workCluster = onec.getClusterWithPort(cluster.get('ClusterPort'))
    
    # Получим рабочие процессы сервера
    if onec_workCluster is not None:
        onec_workingProcesses = onec.getWorkingProcesses()
        
    # Получим центральный сервер кластера
    onec_centralServer = onec.getCentralServer()
        
    # Сформируем строку подключения к рабочему процессу, обслуживающему базы.
    # Это будет процесс с HostName, равным HostName центрального кластера, 
    # и портом, равным MainPort этого рабочего процесса
    for wp in onec_workingProcesses:
        if wp.HostName == onec_centralServer.HostName:
            workingAddress = wp.HostName + ':' + str(wp.MainPort)
            break

    # Подключимся к рабочему процессц, обслуживающему соединения с базами.
    workingProcessConnect = connector.ConnectWorkingProcess(workingAddress)
    
    # Получим список информационных баз кластера
    onec_infoBases = onec.getInfoBases()
    
    # Обойдём базы, и найдём с которыми будем работать
    infobases = cluster.get('Infobases')
    for infobase in infobases:
        ib = workingProcessConnect.CreateInfoBaseInfo()
        ib.name = infobase.get('InfobaseName')
        ib.DeniedFrom = datetime.datetime.now()
        lockTime = int(infobase.get('LockTime'))
        ib.DeniedTo = ib.DeniedFrom + datetime.timedelta(minutes = lockTime)
        ib.PermissionCode = "123456"
        ib.SessionsDenied = True
        workingProcessConnect.UpdateInfoBase(ib)
        
    #for IBSettings in infobases:
        

    # if onec_infoBases is not None:
    #     onec_infoBase = onec.getInfoBase()