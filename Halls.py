from Common import *


class Hall:
    form = web.form.Form(web.form.Textbox('days'), web.form.Textbox('startTime'), web.form.Textbox('endTime'),
                         web.form.Textbox('cost'))

    def GET(self, hall_id):
        hall = db.select('hall', where='id=$hall_id', vars=locals())[0]
        zones = db.select('time_zone', where='hall_id=$hall_id', vars=locals())
        form = self.form()
        return render.prices(hall, zones, form)

    def POST(self, hall_id):
        raise web.seeother('/hall/' + str(hall_id) + "/", True)


class DelHall:
    def GET(self, hall_id):
        db.delete('hall', where='id=$hall_id', vars=locals())
        raise web.seeother('/halls/', True)


class Halls:
    form = web.form.Form(web.form.Textbox('name'),
                         web.form.Textbox('square'))

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
