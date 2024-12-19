import win32com.client as win32
import logging


class ComConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = win32.Dispatch("V83.COMConnector")  # 8.3.23.2040
        logger.info(f'Создали COM-объект - {cls._instance}')
        return cls._instance


class OneC:
    comConnector = None
    
    def __init__(self, comConnector, onecServer, mainPort, clusterLogin, clusterPass):
        try:
            logger.info(f'Начало инициализации кластера {onecServer}')
            if OneC.comConnector is None:
                OneC.comConnector = comConnector
            self.agent = OneC.comConnector.ConnectAgent(onecServer)
            logger.info(f'Подключились к агенту - {self.agent.ConnectionString}')
            self.clusters = self.agent.getclusters()
            logger.info(f'Получили кластеры сервера')
            if logger.level == logging.DEBUG:
                for cluster in self.clusters:
                    logger.debug(f'    {cluster.HostName + ":" + str(cluster.MainPort)}')
            # На одном сервере может быть несколько кластеров, поэтому нужно найти нужный нам кластер
            workCluster = None
            for cluster in self.clusters:
                logger.debug(f'Ищем кластер с портом {cluster.MainPort}')
                if cluster.MainPort == int(mainPort):
                    workCluster = cluster
                    logger.debug(f'Получили кластер {cluster.HostName}:{cluster.MainPort}')
                    break
            if workCluster is not None:
                # Если в кластере есть Администраторы кластера, нужно авторизоваться как Администратор кластера,
                # чтобы получить рабочие процессы и информационные базы
                self.agent.Authenticate(workCluster, clusterLogin, clusterPass)
                logger.info(f"Выполнили аутентификацию на кластере")
                self.workingProcesses = self.agent.GetWorkingProcesses(workCluster)
                logger.info(f'Получили рабочие процессы на кластера')
                if logger.level == logging.DEBUG:
                    for workingProcess in self.workingProcesses:
                        logger.debug(f'    {workingProcess.HostName + ":" + str(workingProcess.MainPort)}')
                self.infoBases = self.agent.getInfoBases(workCluster)
                logger.info(f'Получили список баз на кластере')
                if logger.level == logging.DEBUG:
                    for infoBase in self.infoBases:
                        logger.debug(f'    {infoBase.Name}')

            else:
                self.workingProcesses = None
                self.infoBases = None
        except:
            logger.exception('В процессе инициализации кластера произошла ошибка')
        logger.info(f'Завершение инициализации кластера {onecServer}')

    def getAgent(self):
        return self.agent

    def getClusters(self):
        return self.clusters

    def getWorkingProcesses(self):
        return self.workingProcesses

    def getInfoBases(self):
        return self.infoBases


def main():
    com_connector = ComConnector()
    onec = OneC(com_connector, "a00-77dln-a30.1plt.ru:1540", "1541", "Yurij.Malyutin", "pass")
    onec_agent = onec.getAgent()
    onec_clusters = onec.getClusters()
    for onec_cluster in onec_clusters:
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
