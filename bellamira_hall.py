# encoding=utf8
import sys

# coding: utf8

from db_controller import *

reload(sys)
sys.setdefaultencoding('utf8')




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
    '/deltimezone/(\\d+)/(\\d+)?', 'DelTimezone'
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


class Hall:
    form = web.form.Form(
        web.form.Textbox('days', description='день недели'), web.form.Textbox('startTime', description='время начала'),
        web.form.Textbox('endTime', description='время окончания'),
        web.form.Textbox('cost', description='общая стоимость')
    )
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
    form = web.form.Form(web.form.Textbox('name', description='наименование'),
                         web.form.Textbox('square', description='площадь'))

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

    form = web.form.Form(web.form.Dropdown('drop', [], description='выберите руководителя'), web.form.Textbox('FIO', description='ФИО руководителя'),
                         web.form.Textbox('phone', description='телефон'), web.form.Textbox('link', description='ссылка'))

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
        web.form.Textbox('name', description='название организации'), web.form.Dropdown('drop', [], description='выберите руководителя'),
        web.form.Checkbox('other', description='другое'), web.form.Textbox('FIO', description='ФИО руководителя'),
        web.form.Textbox('phone', description='телефон'), web.form.Textbox('link', description='ссылка')
    )

    form2 = web.form.Form(web.form.Textbox("date", description='дата'), web.form.Textbox('sum', description='общая стоимость'))

    form3 = web.form.Form(web.form.Textbox('name', description='название мероприятия'), web.form.Textbox('startDate', description='дата начала'),
                          web.form.Textbox('startTime', description='время начала'), web.form.Textbox('duration', description='продолжительность'),
                          web.form.Textbox('endDate', description='дата окончания'), web.form.Textbox('endTime', description='время окончания'))

    def GET(self, renter_id):
        groups = db.select("renters_group", order='name', where='renter_id = $renter_id', vars=locals())
        people = db.query('Select * from people where id in (SELECT people_id FROM group_people WHERE renter_id = '
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
        db.insert('group_people', renter_id = renter_id, group_id=ids, people_id=people_id)
        raise web.seeother('/renter/' + str(renter_id) + "/", True)


class Renters:
    form = web.form.Form(
        web.form.Textbox('name', description='наименование'),
        web.form.Textbox('renter_link', description='ссылка на организацию'),
        web.form.Textbox('renter_phone', description='телефон организации'),
        web.form.Dropdown('drop', [(-1, "Add")], description='руководитель'),
        web.form.Checkbox('other', description='другое'), web.form.Textbox('FIO', description='ФИО руководителя'),
        web.form.Textbox('phone', description='телефон руководителя'),
        web.form.Textbox('link', description='ссылка на руководителя')
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
