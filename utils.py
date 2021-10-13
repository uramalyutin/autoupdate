
import win32com.client as win32


class ComConnector:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = win32.Dispatch("V83.COMConnector")
            print(f'Создали COM-объект - {cls._instance}')
        return cls._instance


class OneC:
    def __init__(self, comConnector, agent):

        self.agent = comConnector.ConnectAgent(agent)
        print(f'Подключились к агенту - {self.agent.ConnectionString}')

        self.clusters = self.agent.getclusters()
        for cluster in self.clusters:
            print(f'Получили кластер - {cluster.HostName}:{cluster.MainPort}')
            self.agent.Authenticate(cluster, "", "")
            self.workingProcesses = self.agent.GetWorkingProcesses(cluster)
            print(f'Получили рабочие процессы:')
            for workingProcess in self.workingProcesses:
                print(f'    {workingProcess.HostName + ":" + str(workingProcess.MainPort)}')


def main():
    com_connector = ComConnector()
    onec = OneC(com_connector, "77dln-s-a01.1plt.ru:1540")


if __name__ == "__main__":
    main()
