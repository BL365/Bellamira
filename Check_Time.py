from Common import *

from datetime import *

import time

import json

class CheckTime():

    def GET(self, st_new, en_new, hall_id):

        print st_new, en_new
        TIME_old = db.query('SELECT start_time, end_time FROM using_hall where hall_id=' + str(hall_id))

        st_new = datetime.strptime(st_new, "%d/%m/%Y %H:%M")
        st_new = time.mktime(st_new.timetuple())
        en_new = datetime.strptime(en_new, "%d/%m/%Y %H:%M")
        en_new = time.mktime(en_new.timetuple())

        result = True

        for t in TIME_old:
            print t["start_time"], ">=", en_new,"(", t["start_time"] >= en_new,") or", t["end_time"], "<=", st_new, "(",t["end_time"] <= st_new,")"
            if not (t["start_time"] >= en_new or t["end_time"] <= st_new):

                result = False
                print "        time is busy:         ", t["start_time"],">", en_new," or",  t["end_time"], "<", st_new
                break

        print result

        return (json.dumps({'result': result}))