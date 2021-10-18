
import draw_window
import utils


def update_infobases():
    comcon = utils.ComConnector()
    if comcon is not None:
        onec = utils.OneC(comcon, "77dln-s-a01.1plt.ru:1540")
        iBases = onec.getIB()
        print(f'Обнаружены информационные базы:')
        for ib in iBases:
            print(f'    {ib.name}')
    else:
        print("Не смогли создать COM-соединение")


if __name__ == "__main__":
    draw_window.draw_window()
