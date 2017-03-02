from Common import *

from datetime import *

import time


class Hall():

    form = web.form.Form(
        web.form.Textbox('days'), web.form.Textbox('startTime'),
        web.form.Textbox('endTime'), web.form.Textbox('cost')
    )

    form2 = web.form.Form(
        web.form.Textbox('name'), web.form.Dropdown('drop', []),
        web.form.Textbox('start_time', pattern="\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2}", size="16", maxlength="16", id="st_t"),
        web.form.Textbox('end_time', pattern="\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2}", size="16", maxlength="16", id="end_t")
    )

    def GET(self, hall_id):
        hall = db.select('hall', where='id=$hall_id', vars=locals())[0]
        zones = db.select('time_zone', where='hall_id=$hall_id', vars=locals())
        form = self.form()

        # for t in zones:
        #     t['start_time'] = datetime.fromtimestamp(t['start_time']).strftime("%H:%M")
        #     t['end_time'] = datetime.fromtimestamp(t['end_time']).strftime("%H:%M")

        form2 = self.form2()
        temp = getdropValues2()
        form2.drop.args = temp
        events = db.select('using_hall', where='hall_id=$hall_id', vars=locals())
        updeted_events = []

        for e in events:
            e['start_time'] = datetime.fromtimestamp(e['start_time']).strftime("%d/%m/%Y (%a) %H:%M")
            e['end_time'] = datetime.fromtimestamp(e['end_time']).strftime("%d/%m/%Y (%a) %H:%M")
            for t in temp:
                if t[0] == e['group_id']:
                    e['group_id'] = t[1]
                    updeted_events.append(e)

        return render.prices(hall, zones, form, form2, updeted_events)



    def POST(self, hall_id):
        form = self.form()
        form2 = self.form2()
        if not form.validates():
            raise web.seeother('/hall/' + str(hall_id) + "/", True)
        if not form2.validates():
            raise web.seeother('/hall/' + str(hall_id) + "/", True)
        group_id = form2.d.drop

        # start_dt_string = datetime.strptime(form.d.startTime, "%%H:%M")
        # start_dt_unix = time.mktime(start_dt_string.timetuple())
        # end_dt_string = datetime.strptime(form.d.endTime, "%H:%M")
        # end_dt_unix = time.mktime(end_dt_string.timetuple())

        # if group_id != "-1":
        #     element = {"id": getNextId("time_zone"),
        #                "hall_id": hall_id,
        #                "days_of_week": form.d.days,
        #                "start_time": start_dt_unix,
        #                "end_time": end_dt_unix,
        #                "cost": form.d.cost}
        #     db.multiple_insert('time_zone', values=[element])
        # raise web.seeother('/hall/' + str(hall_id) + "/", True)

        if group_id != "-1":
            element = {"id": getNextId("time_zone"),
                       "hall_id": hall_id,
                       "days_of_week": form.d.days,
                       "start_time": form.d.startTime,
                       "end_time": form.d.endTime,
                       "cost": form.d.cost}
            db.multiple_insert('time_zone', values=[element])
        raise web.seeother('/hall/' + str(hall_id) + "/", True)


        start_dt_string2 = datetime.strptime(form2.d.start_time, "%d/%m/%Y %H:%M")
        start_dt_unix2 = time.mktime(start_dt_string2.timetuple())
        end_dt_string2 = datetime.strptime(form2.d.end_time, "%d/%m/%Y %H:%M")
        end_dt_unix2 = time.mktime(end_dt_string2.timetuple())

        if group_id != "-1":
            element2 = {"id": getNextId("using_hall"),
                       "name": form2.d.name,
                       "group_id": group_id,
                       "hall_id": hall_id,
                       "start_time": start_dt_unix2,
                       "end_time": end_dt_unix2}
            db.multiple_insert('using_hall', values=[element2])
        raise web.seeother('/hall/' + str(hall_id) + "/", True)

class DelHall:

    def GET(self, hall_id):
        db.delete('hall', where='id=$hall_id', vars=locals())
        raise web.seeother('/halls/', True)

class Halls:
    form = web.form.Form(web.form.Textbox('name'), web.form.Textbox('square'))

    def GET(self):
        halls = db.select('hall')
        form = self.form()
        return render.hall(halls, form)

    def POST(self):
        form = self.form()
        if not form.validates():
            raise web.seeother('/halls/', True)
        element = {"name": form.d.name,
                       "square": form.d.square,
                       "id": getNextId('hall')}
        db.multiple_insert('hall', values=[element])
        raise web.seeother('/halls/', True)
#
# class Timezone():
#
#     def GET(self, hall_id, cost):
#