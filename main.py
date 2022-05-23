import utils


comcon = utils.ComConnector()
if comcon is not None:
    onec = utils.OneC(comcon)
else:
    print("Не смогли создать COM-соединение")
