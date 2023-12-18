import speedtest
import threading
import time
from collections import deque
import time
import datetime
try:
    from dashboard.database.database import db_session, init_db, engine
    from dashboard.database.models import SP_CON
except:
    import sys
    sys.path.insert(1, r'D:\Learn\Python\repos\DASHBOARD_HOME')
    from dashboard.database.database import db_session, init_db, engine
    from dashboard.database.models import SP_CON

def calc_ul_dl(rate, dt=3):
    while True:
        try:
            st = speedtest.Speedtest()
            ul, dl = st.upload()/1024/1024, st.download()/1024/1024
            now = datetime.datetime.now()
            timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
            sp_con = SP_CON(round(ul, 2), round(dl, 2))
            db_session.add(sp_con)
            db_session.commit()
        except Exception as error:
            print(error)
            ul, dl = "-", "-"
        rate.append((ul, dl))
        

        time.sleep(dt)



def print_rate(rate):
    try:
        print("UL: "+str(round(rate[-1][0], 1))+" MB/s / DL: "+str(round(rate[-1][1], 1))+" MB/s")
    except IndexError:
        "UL: - kB/s/ DL: - kB/s"

def run_test(dt=3):
    transfer_rate = deque(maxlen=1)
    t = threading.Thread(target=calc_ul_dl, args=(transfer_rate, dt))

    # The program will exit if there are only daemonic threads left.
    t.daemon = True
    t.start()

if __name__ == "__main__":


    # Create the ul/dl thread and a deque of length 1 to hold the ul/dl- values
    transfer_rate = deque(maxlen=1)
    t = threading.Thread(target=calc_ul_dl, args=(transfer_rate,))

    # The program will exit if there are only daemonic threads left.
    t.daemon = True
    t.start()

    # The rest of your program, emulated by me using a while True loop
    while True:
        print_rate(transfer_rate)
        time.sleep(5)


