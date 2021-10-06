import sys
import win32com.client as win32

from au_mainForm import Ui_MainWindow
from PyQt5 import QtWidgets


def create_com_connector():
    _com_connector = win32.Dispatch("V83.COMConnector")
    if _com_connector is not None:
        print("Создали COM-объект...")
        return _com_connector
    else:
        print("Возникли проблемы при создании COM-объекта...")


def connect_agent(_com_connector):
    _agent = _com_connector.ConnectAgent("77dln-s-a01.1plt.ru:1540")
    if _agent is not None:
        print("Подключились к агенту...")
        return _agent
    else:
        print("Возникли проблемы при подключении к агенту...")


def get_clusters(_agent):
    _clusters = _agent.getclusters()
    if _clusters is not None:
        print("Получили список кластеров...")
        return _clusters
    else:
        print("Возникли проблемы при получении списка кластеров...")


def get_working_processes(_agent, _cluster):
    _working_processes = _agent.GetWorkingProcesses(_cluster)
    if _working_processes is not None:
        print("Получили рабочие процессы...")
        return _working_processes
    else:
        print("Возникли проблемы при получении рабочих процессов...")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def main():
    com_connector = create_com_connector()
    agent = connect_agent(com_connector)
    clusters = get_clusters(agent)
    for cluster in clusters:
        agent.Authenticate(cluster, "", "")
        working_processes = get_working_processes(agent, cluster)

        for working_process in working_processes:
            connect_string = working_process.HostName + ":" + str(working_process.MainPort)
            print('     ' + connect_string)

    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
