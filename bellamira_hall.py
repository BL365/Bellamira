from db_controller import *

from datetime import *

import time

import json


google_reg = {"web": {"client_id":"890621792831-7gh2uv62k8rpovqs3lrh5bc5q90unh8f.apps.googleusercontent.com",
                      "project_id":"bellamira-146516","auth_uri":"https://accounts.google.com/o/oauth2/auth",
                      "token_uri":"https://accounts.google.com/o/oauth2/token",
                      "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                      "client_secret":"dcpF93fM7ktZzoXRsX5aUykR"}}

urls = (
    '/', 'Index',
    '/renters/', 'Renters',
    '/renter/(\\d+)/', 'Renter',
    '/renter/(\\d+)/(\\d+)/', 'Group',
    '/deletePeopleFromGroup/(\\d+)/(\\d+)/(\\d+)?', 'DeletePeopleFromGroup',
    '/halls/', 'Halls',
    '/hall/(\\d+)/', 'Hall',
    '/hall/(\\d+)/(\\d+)/', 'Timezone',
    '/rentTimezone/', 'RentTimezone',
    '/delhall/(\\d+)?', 'DelHall',
    '/deltimezone/(\\d+)/(\\d+)?', 'DelTimezone',
    '/prices/(\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2})/(\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2})/(\\d+)/','CheckTime'
)

dbCreator().execute()

render = web.template.render('templates', base='base')

class Index:
    form = web.form.Form(
        web.form.Textbox('number', web.form.notnull, description="")
    )

    def GET(self):
        return render.index()

    def POST(self):
        raise web.seeother('/', True)


class Hall():

    form = web.form.Form(
        web.form.Textbox('days'), web.form.Textbox('startTime'), web.form.Textbox('endTime'),
                         web.form.Textbox('cost')
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

        form2 = self.form2()
        tempo = getdropValues2()
        form2.drop.args = tempo
        events = db.select('using_hall', where='hall_id=$hall_id', vars=locals())
        updeted_events = []

        for e in events:
            e['start_time'] = datetime.fromtimestamp(e['start_time']).strftime("%d/%m/%Y (%a) %H:%M")
            e['end_time'] = datetime.fromtimestamp(e['end_time']).strftime("%d/%m/%Y (%a) %H:%M")
            for t in tempo:
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

        start_dt_string = datetime.strptime(form2.d.start_time, "%d/%m/%Y %H:%M")
        start_dt_unix = time.mktime(start_dt_string.timetuple())
        end_dt_string = datetime.strptime(form2.d.end_time, "%d/%m/%Y %H:%M")
        end_dt_unix = time.mktime(end_dt_string.timetuple())

        if group_id != "-1":
            element = {"id": getNextId("using_hall"),
                       "name": form2.d.name,
                       "group_id": group_id,
                       "hall_id": hall_id,
                       "start_time": start_dt_unix,
                       "end_time": end_dt_unix}
            db.multiple_insert('using_hall', values=[element])
        raise web.seeother('/hall/' + str(hall_id) + "/", True)

class CheckTime():

    def GET(self, st_new, en_new, hall_id):

        start_old = db.query('SELECT start_time FROM using_hall where hall_id=' + str(hall_id))
        end_old = db.query('SELECT end_time FROM using_hall where hall_id=' + str(hall_id))

        st_new = datetime.strptime(st_new, "%d/%m/%Y %H:%M")
        st_new = time.mktime(st_new.timetuple())
        en_new = datetime.strptime(en_new, "%d/%m/%Y %H:%M")
        en_new = time.mktime(en_new.timetuple())

        dif_eN_sO = []
        start_times_old = []
        for a in start_old:
            z = en_new - a['start_time']
            start_times_old.append(a['start_time'])
            dif_eN_sO.append(z)

        dif_eO_sN = []
        end_times_old = []
        for a in end_old:
            z = a['end_time'] - st_new
            dif_eO_sN.append(z)
            end_times_old.append(a['end_time'])

        res = "Time "

        if max(end_times_old) < st_new:
            ST = 1
            if st_new < en_new:
                EN = 1
            else:
                res = res + "end - incorrectly "
                EN = 0
        else:
            if en_new < min(start_times_old):
                EN = 1
                if st_new < en_new:
                    ST = 1
                else:
                    res = res + "start - incorrectly "
                    ST = 0
                if min(dif_eO_sN) <= 0:
                    ST = 1
                else:
                    res = res + "start - incorrectly "
                    ST = 0
                if min(dif_eN_sO) <= 0:
                     EN = 1
                else:
                    res = res + "end - incorrectly "
                    EN = 0


        result = ST == 0 and EN == 0
        print result

        return (json.dumps({'result': result}))

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

class DeletePeopleFromGroup:


    def GET(self, renter_id, group_id, people_id):
        db.query('delete from group_people where group_id=' + str(group_id) + ' and people_id = ' + str(people_id))
        raise web.seeother('/renter/' + str(renter_id) + "/" + str(group_id) + "/", True)

class Group:

    form = web.form.Form(web.form.Dropdown('drop', []), web.form.Textbox('FIO'), web.form.Textbox('phone'),
                         web.form.Textbox('link')
                         )

    def GET(self, renter_id, group_id):
        people = db.query('Select * from people where id in (select people_id from group_people where group_id='
                          + str(group_id)+' or (group_id is null and renter_id = ' + str(renter_id) + '))');
        group = db.select("renters_group", where='id = $group_id', vars=locals())[0]
        renter = db.select("renters", where="id=$renter_id", vars=locals())[0]
        renter_man = db.select("people", where="id = $renter.people_id", vars=locals())[0]
        form = self.form()
        form.drop.args = getdropValues();
        return render.group(renter, renter_man, group, people, form)

    def POST(self, renter_id, group_id):
        form = self.form()
        if not form.validates() or (form.d.drop == '-1' and form.d.FIO == ""):
            raise web.seeother('/renter/' + str(renter_id) + "/" + str(group_id) + "/", True)
        people_id = form.d.drop
        if people_id == "-1" and form.d.FIO!="":
            people_id = getNextId('people')
            element = {"FIO": form.d.FIO,
                       "phone": form.d.phone,
                       "link": form.d.link,
                       "id": people_id}
            db.multiple_insert('people', values=[element])
        db.insert('group_people', renter_id=renter_id, group_id=group_id, people_id=people_id)
        raise web.seeother('/renter/' + str(renter_id) + "/" + str(group_id) + "/", True)

class Renter:

    form = web.form.Form(
        web.form.Textbox('name'), web.form.Dropdown('drop', []),
        web.form.Checkbox('other'), web.form.Textbox('FIO'),
        web.form.Textbox('phone'), web.form.Textbox('link')
    )

    form2 = web.form.Form(web.form.Textbox("date"), web.form.Textbox('sum'))

    form3 = web.form.Form(web.form.Textbox('name'), web.form.Textbox('startDate'), web.form.Textbox('startTime'),
                          web.form.Textbox('duration'), web.form.Textbox('endDate'), web.form.Textbox('endTime'))

    def GET(self, renter_id):
        groups = db.select("renters_group", order='name', where='renter_id = $renter_id', vars=locals())
        people = db.query('Select * from people where id in (select people_id from group_people where renter_id = '
                                   + str(renter_id) + ')');
        renter = db.select("renters", where="id=$renter_id", vars=locals())[0]
        renter_man = db.select("people", where="id = $renter.people_id", vars=locals())[0]
        form = self.form()
        form.drop.args = getdropValues()
        form2 = self.form2()
        form3 = self.form3()
        return render.renter(renter, renter_man, groups, people, form, form2, form3)

    def POST(self, renter_id):
        form = self.form()
        if not form.validates():
            raise web.seeother('/renter/'+str(renter_id)+"/", True)
        if form.d.FIO == "" and form.d.name == "":
            raise web.seeother('/renter/' + str(renter_id) + "/", True)
        people_id = form.d.drop
        if people_id == "-1" and form.d.FIO != "":
            people_id = getNextId('people')
            element = {"FIO": form.d.FIO,
                       "phone": form.d.phone,
                       "link": form.d.link,
                       "id": people_id}
            db.multiple_insert('people', values=[element])
        ids = getNextId('renters_group')
        element = {"name": form.d.name,
                   "people_id": people_id,
                   "renter_id": renter_id,
                   "id": ids}
        db.multiple_insert("renters_group", values=[element])
        db.insert('group_people', renter_id=renter_id, group_id=ids, people_id=people_id)
        raise web.seeother('/renter/' + str(renter_id) + "/", True)


class Renters:

    form = web.form.Form(
        web.form.Textbox('name'), web.form.Textbox('renter_link'),
        web.form.Textbox('renter_phone'), web.form.Dropdown('drop', [(-1, "Add")]),
        web.form.Checkbox('other'), web.form.Textbox('FIO'),
        web.form.Textbox('phone'), web.form.Textbox('link')
    )

    def GET(self):
        based = db.select("renters", order='id')
        form = self.form()
        form.drop.args = getdropValues();
        return render.renters(form, based, db)

    def POST(self):
        form = self.form()
        if not form.validates():
            raise web.seeother('/renters/', True)
        if form.d.FIO == "" and form.d.name=="":
            raise web.seeother('/renters/', True)
        people_id = form.d.drop
        if people_id == "-1" and form.d.FIO != "":
            people_id = getNextId('people')
            element = {"FIO": form.d.FIO,
                   "phone": form.d.phone,
                   "link": form.d.link,
                   "id": people_id}
            db.multiple_insert('people', values=[element])
        ids = getNextId('renters')
        element = {"name": form.d.name,
                   "phone": form.d.renter_phone,
                   "link": form.d.renter_link,
                   "people_id": people_id,
                   "id": ids}
        db.multiple_insert("renters", values=[element])
        db.insert('group_people', renter_id=ids, people_id=people_id)
        raise web.seeother('/renters/', True)

app = web.application(urls, globals())

if __name__ == '__main__':
    print "http://localhost:8080/renters/"
    print "http://localhost:8080/halls/"
    app.run()
