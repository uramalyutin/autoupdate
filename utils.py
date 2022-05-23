
import win32com.client as win32


class ComConnector:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = win32.Dispatch("V83.COMConnector")
            print(f'Создали COM-объект - {cls._instance}')
        return cls._instance


class OneC:
    connector = None
    def __init__(self, comConnector, server):
        if OneC.connector == None:
            OneC.connector = comConnector
        self.agent = OneC.connector.ConnectAgent(server)
        print(f'Подключились к агенту - {self.agent.ConnectionString}')

        self.clusters = self.agent.getclusters()
        for cluster in self.clusters:
            print(f'Получили кластер - {cluster.HostName}:{cluster.MainPort}')
            # Если в кластере есть Администраторы кластера, нужно передавать логин и пароль для авторизации
            self.agent.Authenticate(cluster, "", "")
            self.workingProcesses = self.agent.GetWorkingProcesses(cluster)
            print(f'Получили рабочие процессы кластера:')
            for workingProcess in self.workingProcesses:
                print(f'    {workingProcess.HostName + ":" + str(workingProcess.MainPort)}')


    def getIB(self):
        for cluster in self.clusters:
            infoBases = self.agent.getInfoBases(cluster)
        return infoBases


def main():
    com_connector = ComConnector()
    onec = OneC(com_connector, "77dln-s-a01.1plt.ru:1540")


if __name__ == "__main__":
    main()
