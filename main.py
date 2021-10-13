
import utils

comcon = utils.ComConnector()
if comcon is not None:
    onec = utils.OneC(comcon, "77dln-s-a01.1plt.ru:1540")
    iBases = onec.getIB()
    print(f'Обнаружены информационные базы:')
    for ib in iBases:
        print(f'    {ib.name}')
else:
    print("Не смогли создать COM-соединение")
