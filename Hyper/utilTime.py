from datetime import datetime
import time 
BASE_DATETIME_DATE   = "2000-01-01T" # NO CAMBIAR

def getSecondsToNextTarget(target_datetime_time):
    """
    Funcion que devuelve los segundos que faltan 
    para llegar a la hora target del dia. Si se ha pasado 
    la hora target, indica los segundos hasta la siguiente hora target.
    """
    current_time_iso = datetime.now().time().isoformat()
    current_compare_datetime = datetime.fromisoformat(BASE_DATETIME_DATE + current_time_iso)

    target_compare_datetime = datetime.fromisoformat(BASE_DATETIME_DATE + target_datetime_time)

    delta_time = target_compare_datetime - current_compare_datetime

    return delta_time.seconds

def waitTillTargetTime(target_datetime_time):
    """
    Funcion que duerme el proceso hasta que llega la hora target.
    """

    STT = getSecondsToNextTarget(target_datetime_time)

    # Dormimos lo que queda
    time.sleep(STT)
