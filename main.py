import utils
import yaml


#Прочитаем настройки из updater_settings.yaml

com_connector = utils.ComConnector()
if com_connector is not None:
    onec = utils.OneC_Cluster(com_connector, "a00-77dln-a30.1plt.ru:1540", "Yurij.Malyutin", "pass")
    onec_agent = onec.getAgent()
    onec_clusters = onec.getClusters()
    onec_workCluster = onec.getClusterWithPort("1541")
    if onec_workCluster is not None:
        onec_workingProcesses = onec.getWorkingProcesses()
        onec_infoBases = onec.getInfoBases()
    if onec_infoBases is not None:
        onec_infoBase = onec.getInfoBase()
