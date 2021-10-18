
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
        self.__agent = OneC.connector.ConnectAgent(server)
        print(f'Подключились к агенту - {self.__agent.ConnectionString}')

        self.__clusters = self.__agent.getclusters()
        for cluster in self.__clusters:
            print(f'Получили кластер - {cluster.HostName}:{cluster.MainPort}')
            # Если в кластере есть Администраторы кластера, нужно передавать логин и пароль для авторизации
            self.__agent.Authenticate(cluster, "", "")
            self.__workingProcesses = self.__agent.GetWorkingProcesses(cluster)
            print(f'Получили рабочие процессы кластера:')
            for workingProcess in self.__workingProcesses:
                print(f'    {workingProcess.HostName + ":" + str(workingProcess.MainPort)}')

    def getIB(self):
        for cluster in self.__clusters:
            infoBases = self.__agent.getInfoBases(cluster)
        return infoBases

def main():
    com_connector = ComConnector()
    onec = OneC(com_connector, "77dln-s-a01.1plt.ru:1540")


if __name__ == "__main__":
    main()
