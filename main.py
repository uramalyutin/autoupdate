
import utils

comcon = utils.ComConnector()
if comcon is not None:
    onec = utils.OneC(comcon, "77dln-s-a01.1plt.ru:1540")
else:
    print("Не смогли создать COM-соединение")
