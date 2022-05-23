import win32com.client as win32


class ComConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = win32.Dispatch("V83.COMConnector")  # 8.3.21.1302
        return cls._instance


class OneC:
    comConnector = None

    def __init__(self, comConnector, onecServer, mainPort, clusterLogin, clusterPass):
        if OneC.comConnector is None:
            OneC.comConnector = comConnector
        self.agent = OneC.comConnector.ConnectAgent(onecServer)
        self.clusters = self.agent.getclusters()
        # На одном сервере может быть несколько кластеров, поэтому нужно найти нужный нам кластер
        workCluster = None
        for cluster in self.clusters:
            if cluster.MainPort == int(mainPort):
                workCluster = cluster
                break
        if workCluster is not None:
            # Если в кластере есть Администраторы кластера, нужно авторизоваться как Администратор кластера,
            # чтобы получить рабочие процессы и информационные базы
            self.agent.Authenticate(workCluster, clusterLogin, clusterPass)
            self.workingProcesses = self.agent.GetWorkingProcesses(workCluster)
            self.infoBases = self.agent.getInfoBases(workCluster)
        else:
            self.workingProcesses = None
            self.infoBases = None

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
    print(f'Создали COM-объект - {com_connector}')
    onec = OneC(com_connector, "a00-77dln-a30.1plt.ru:1540", "1541", "Yurij.Malyutin", "pass")
    onec_agent = onec.getAgent()
    print(f'Подключились к агенту - {onec_agent.ConnectionString}')
    onec_clusters = onec.getClusters()
    print(f'Получили кластеры сервера:')
    for onec_cluster in onec_clusters:
        print(f'    {onec_cluster.HostName}:{onec_cluster.MainPort}')
        onec_workingProcesses = onec.getWorkingProcesses()
        print(f'Получили рабочие процессы кластера:')
        for onec_workingProcess in onec_workingProcesses:
            print(f'    {onec_workingProcess.HostName + ":" + str(onec_workingProcess.MainPort)}')
        onec_infoBases = onec.getInfoBases()
        print(f'Получили список баз:')
        for onec_infoBase in onec_infoBases:
            print(f'    {onec_infoBase.Name}')


if __name__ == "__main__":
    main()
