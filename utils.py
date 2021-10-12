
import win32com.client as win32


class ComConnector:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = win32.Dispatch("V83.COMConnector")
        return cls._instance


class OneC:
    def __init__(self, comConnector, agent):
        self.agent = comConnector.ConnectAgent(agent)
        self.clusters = self.agent.getclusters()
        print(f'COM-объект - {comConnector}')
        print(f'Агент - {self.agent}')
        for cluster in self.clusters:
            print(f'Кластер - {cluster}')
            self.agent.Authenticate(cluster, "", "")
            self.workingProcesses = self.agent.GetWorkingProcesses(cluster)
            for workingProcess in self.workingProcesses:
                print(f'Рабочий процесс {workingProcess.HostName + ":" + str(workingProcess.MainPort)}')


def main():
    com_connector = ComConnector()
    onec = OneC(com_connector, "77dln-s-a01.1plt.ru:1540")


if __name__ == "__main__":
    main()
