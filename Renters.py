from Common import *


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

