import win32com.client as win32


class ComConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = win32.Dispatch("V83.COMConnector")  # 8.3.21.1302
            print(f'Создали COM-объект - {cls._instance}')
        return cls._instance


class OneC:
    connector = None

    def __init__(self, comConnector):
        if OneC.connector is None:
            OneC.connector = comConnector
        self.agent = None
        self.clusters = None
        self.workingProcesses = None
        self.infoBases = None

    def getAgent(self, server):
        self.agent = OneC.connector.ConnectAgent(server)
        return self.agent

    def getClusters(self):
        self.clusters = self.agent.getclusters()
        return self.clusters

    def getWorkingProcesses(self, cluster, clusterLogin, clusterPass):
        # Если в кластере есть Администраторы кластера, нужно передавать логин и пароль для авторизации
        self.agent.Authenticate(cluster, clusterLogin, clusterPass)
        self.workingProcesses = self.agent.GetWorkingProcesses(cluster)
        return self.workingProcesses

    def getInfoBases(self, cluster, clusterLogin, clusterPass):
        # Если в кластере есть Администраторы кластера, нужно передавать логин и пароль для авторизации
        self.agent.Authenticate(cluster, clusterLogin, clusterPass)
        for cluster in self.clusters:
            self.infoBases = self.agent.getInfoBases(cluster)
        return self.infoBases


def main():
    com_connector = ComConnector()
    onec = OneC(com_connector)
    onec_agent = onec.getAgent("a00-77dln-a30.1plt.ru:1540")
    print(f'Подключились к агенту - {onec_agent.ConnectionString}')
    onec_clusters = onec.getClusters()
    print(f'Получили кластеры сервера:')
    for onec_cluster in onec_clusters:
        print(f'    {onec_cluster.HostName}:{onec_cluster.MainPort}')
        onec_workingProcesses = onec.getWorkingProcesses(onec_cluster, "Yurij.Malyutin", "pass")
        print(f'Получили рабочие процессы кластера:')
        for onec_workingProcess in onec_workingProcesses:
            print(f'    {onec_workingProcess.HostName + ":" + str(onec_workingProcess.MainPort)}')
        onec_infoBases = onec.getInfoBases(onec_cluster, "Yurij.Malyutin", "pass")
        print(f'Получили список баз:')
        for onec_infoBase in onec_infoBases:
            print(f'    {onec_infoBase.Name}')


if __name__ == "__main__":
    main()
