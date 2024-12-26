import win32com.client as win32
import logging


class ComConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is not None:
            return cls._instance
        
        try:
            cls._instance = win32.Dispatch("V83.COMConnector")  # 8.3.23.2040
            #logger.info(f'Создали COM-объект - {cls._instance}')
        except:
            logger.exception('В процессе создания COM-объекта произошла ошибка')
            return cls._instance
        else:
            logger.info(f'Создали COM-объект - {cls._instance}')
            return cls._instance


class OneC_Server:
    _comConnector = None

    def __new__(cls, settings, comConnector):
        # В общем случае COM-коннектор может быть только одной версии, поэтому сохраним его для всего класса
        if cls._comConnector is None:
            # Добавим COM-коннектор
            cls._comConnector = comConnector
        return super().__new__(cls)
    
    def __init__(self, settings, comConnector):
        self.serverName = settings.get('ServerName')
        self.serverPort = settings.get('ServerPort')
        self.clusterPort = settings.get('ClusterPort')
        self.clusterLogin = settings.get('ClusterLogin')
        self.clusterPassword = settings.get('ClusterPassword')
        self.IBName = settings.get('InfoBaseName')
        self.IBLogin = settings.get('InfobaseLogin')
        self.IBPass = settings.get('InfobasePassword')
 
        self.agent = None
        self.clusters = None
        self.workCluster = None
        self.workingProcesses = None
        self.workingServers = None
        self.centralServer = None
        self.infoBases = None
 
        logger.info(f'Проинициализировали объект для работы с кластером')

    def getAgent(self): 
        '''Подключаеся к агенту'''
        try:
            self.agent = OneC_Server._comConnector.ConnectAgent(self.serverName)
        except:
            logger.exception('В процессе подключения к агенту произошла ошибка')        
        else:
            logger.info(f'Подключились к агенту - {self.serverName}')
        return self.agent

    def getAllClusters(self):
        '''Получаем кластеры сервера'''
        try:
            self.clusters = self.agent.getclusters()
        except:
            logger.exception('В процессе получения кластеров произошла ошибка')
        else:
            logger.info(f'Получили кластеры сервера')
            if logger.level == logging.DEBUG:
                for cluster in self.clusters:
                    logger.debug(f'    {cluster.HostName + ":" + str(cluster.MainPort)}')
        return self.clusters
    
    def getClusterWithPort(self, port):
        '''На одном сервере может быть несколько кластеров, поэтому нужно найти кластер с нужным портом'''
        try:
            for cluster in self.clusters:
                if cluster.MainPort == int(port):
                    self.workCluster = cluster
                    break
        except:
            logger.exception(f'В процессе поиска кластера с портом {port} произошла ошибка')
        else:
            logger.info(f'Получили кластер {cluster.HostName}:{cluster.MainPort}')
    
        # Если в кластере есть Администраторы кластера, нужно авторизоваться как Администратор кластера,
        # чтобы получить рабочие процессы и информационные базы
        try:
            self.agent.Authenticate(self.workCluster, self.clusterLogin, self.clusterPassword)
        except:
            logger.exception(f'В процессе аутентификации на кластере произошла ошибка')
        else:
            logger.info(f"Выполнили аутентификацию на кластере")
        return self.workCluster

    def getWorkingProcesses(self):
        #Получим рабочие процессы кластера
        try:
            self.workingProcesses = self.agent.GetWorkingProcesses(self.workCluster)
        except:
            logger.exception(f'В процессе получения рабочих процессов на кластере произошла ошибка')
        else:
            logger.info(f'Получили рабочие процессы на кластере')
            if logger.level == logging.DEBUG:
                for workingProcess in self.workingProcesses:
                    logger.debug(f'    {workingProcess.HostName + ":" + str(workingProcess.MainPort)}')
        return self.workingProcesses

    def getWorkingServers(self):
        #Получим рабочие серверы кластера
        try:
            self.workingServers = self.agent.GetWorkingServers(self.workCluster)
        except:
            logger.exception(f'В процессе получения рабочих серверов на кластере произошла ошибка')
        else:
            logger.info(f'Получили рабочие серверы на кластере')
            if logger.level == logging.DEBUG:
                for workingServers in self.workingServers:
                    logger.debug(f'    {workingServers.HostName + ":" + str(workingServers.MainPort)}')
        return self.workingServers

    def getCentralServer(self):
        #Получим центральный сервер кластера
        if self.workingServers is None:
            self.getWorkingServers()
        try:
            for ws in self.workingServers:
                if ws.Name == 'Центральный сервер':
                    self.centralServer = ws
                    break
        except:
            logger.exception(f'В процессе получения центрального сервера кластера произошла ошибка')
        else:
            logger.info(f'Получили центральный сервер кластера')
            if logger.level == logging.DEBUG:
                logger.debug(f'    {self.centralServer.HostName + ":" + str(self.centralServer.MainPort)}')
        return self.centralServer

    def getInfoBases(self):
        #Получим информационные базы кластера
        try:
            self.infoBases = self.agent.getInfoBases(self.workCluster)
        except:
            logger.exception(f'В процессе получения информационных баз на кластере произошла ошибка')
        else:
            logger.info(f'Получли список информационных баз на кластере')
            if logger.level == logging.DEBUG:
                for infoBase in self.infoBases:
                    logger.debug(f'    {infoBase.Name}')
        return self.infoBases

    def getInfoBase(self, IBName):
        for ib in self.infoBases:
            if IBName == ib.Name:
                logger.info(f'Нашли базу {ib.Name}')
                return ib
            else:
                continue
        return None


def getLogger(loggerName, loggerMode):
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(
        filename = "updater_log.log", mode=loggerMode, encoding = 'utf-8'
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
    return logger


def main():
    pass


logger = getLogger("utils", "a")
if __name__ == "__main__":
    main()
