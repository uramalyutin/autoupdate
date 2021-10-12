
import win32com.client as win32


class ComConnector:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = win32.Dispatch("V83.COMConnector")
        return cls._instance


class OneC:
    def __init__(self, comConnector):
        self.comConnector = comConnector
        self.agent = self.comConnector.ConnectAgent("77dln-s-a01.1plt.ru:1540")
        self.clusters = self.agent.getclusters()
        print(f'COM-объект - {self.comConnector}')
        print(f'Агент - {self.agent}')
        for cluster in self.clusters:
            print(f'Кластер - {cluster}')
            self.agent.Authenticate(cluster, "", "")
            self.working_processes = self.agent.GetWorkingProcesses(cluster)
            for working_process in self.working_processes:
                print(f'Рабочий процесс {working_process.HostName + ":" + str(working_process.MainPort)}')

def main():
    com_connector = ComConnector()
    onec = OneC(com_connector)


if __name__ == "__main__":
    main()
