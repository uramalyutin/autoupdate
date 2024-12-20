import win32com.client as win32
import logging


class ComConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = win32.Dispatch("V83.COMConnector")  # 8.3.23.2040
                logger.info(f'Создали COM-объект - {cls._instance}')
                return cls._instance
            except:
                logger.exception('В процессе создания COM-объекта произошла ошибка')
                return cls._instance


class OneC_Cluster:
    _comConnector = None
    
    def __init__(self, comConnector, onecServer, clusterLogin, clusterPass):
        logger.info(f'Начало инициализации кластера {onecServer}')
        
        #В общем случае COM-коннектор может быть только одной версии, поэтому сохраним его для всего класса
        if OneC_Cluster._comConnector is None:
            OneC_Cluster._comConnector = comConnector
        
        self.onecServer = onecServer
        self.clusterLogin = clusterLogin
        self.clusterPass = clusterPass
        self.agent = None
        self.clusters = None
        self.workCluster = None
        self.workingProcesses = None
        self.infoBases = None
 
        logger.info(f'Завершение инициализации кластера {onecServer}')

    def getAgent(self):
        if self.agent is None:
            #Подключаеся к агенту
            try:
                logger.debug(f'Подключаемся к агенту - {self.onecServer}')
                self.agent = OneC_Cluster._comConnector.ConnectAgent(self.onecServer)
            except:
                logger.exception('В процессе подключения к агенту произошла ошибка')        
        return self.agent

    def getClusters(self):
        if self.clusters is None:
            #Получаем кластеры сервера
            try:
                logger.debug(f'Получаем кластеры сервера')
                self.clusters = self.agent.getclusters()
                if logger.level == logging.DEBUG:
                    logger.debug(f'Получили кластеры:')
                    for cluster in self.clusters:
                        logger.debug(f'    {cluster.HostName + ":" + str(cluster.MainPort)}')
            except:
                logger.exception('В процессе получения кластеров произошла ошибка')
        return self.clusters

    def getClusterWithPort(self, port):
        if self.workCluster is None:
            # На одном сервере может быть несколько кластеров, поэтому нужно найти кластер с нужным портом
            try:
                logger.debug(f'Ищем кластер с портом {port}')
                for cluster in self.clusters:
                    if cluster.MainPort == int(port):
                        self.workCluster = cluster
                        logger.debug(f'Получили кластер {cluster.HostName}:{cluster.MainPort}')
                        break
            except:
                logger.exception(f'В процессе поиска кластера с портом {port} произошла ошибка')
            # Если в кластере есть Администраторы кластера, нужно авторизоваться как Администратор кластера,
            # чтобы получить рабочие процессы и информационные базы
            try:
                logger.debug(f"Выполняем аутентификацию на кластере")
                self.agent.Authenticate(self.workCluster, self.clusterLogin, self.clusterPass)
            except:
                logger.exception(f'В процессе аутентификации на кластере произошла ошибка')
        return self.workCluster

    def getWorkingProcesses(self):
        if self.workingProcesses is None:
            #Получим рабочие процессы кластера
            try:
                logger.debug(f'Получим рабочие процессы на кластере')
                self.workingProcesses = self.agent.GetWorkingProcesses(self.workCluster)
                if logger.level == logging.DEBUG:
                    logger.debug(f'Получиили рабочие процессы:')
                    for workingProcess in self.workingProcesses:
                        logger.debug(f'    {workingProcess.HostName + ":" + str(workingProcess.MainPort)}')
            except:
                logger.exception(f'В процессе получения рабочих процессов на кластере произошла ошибка')
        return self.workingProcesses

    def getInfoBases(self):
        if self.infoBases is None:
            #Получим информационные базы кластера
            try:
                logger.debug(f'Получим список информационных баз на кластере')
                self.infoBases = self.agent.getInfoBases(self.workCluster)
                if logger.level == logging.DEBUG:
                    logger.debug(f'Получиили информационные базы:')
                    for infoBase in self.infoBases:
                        logger.debug(f'    {infoBase.Name}')
            except:
                logger.exception(f'В процессе получения информационных баз на кластере произошла ошибка')        
        return self.infoBases


def main():
    com_connector = ComConnector()
    onec = OneC_Cluster(com_connector, "a00-77dln-a30.1plt.ru:1540", "Yurij.Malyutin", "pass")
    onec_agent = onec.getAgent()
    onec_clusters = onec.getClusters()
    onec_workCluster = onec.getClusterWithPort("1541")
    if onec_workCluster is not None:
        onec_workingProcesses = onec.getWorkingProcesses()
        onec_infoBases = onec.getInfoBases()


logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    filename = "updater_log.log", mode="w", encoding = 'utf-8'
)
console_handler = logging.StreamHandler()
file_format = logging.Formatter(
    '%(asctime)s;%(name)s;%(levelname)s;%(message)s'
)
console_format = logging.Formatter(
    "[%(asctime)s];%(name)s;%(levelname)s;%(message)s","%H:%M:%S"
)
file_handler.setFormatter(file_format)
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


if __name__ == "__main__":
    main()
