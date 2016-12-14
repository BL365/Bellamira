from Common import *


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
                          + str(group_id) + ' or (group_id is null and renter_id = ' + str(renter_id) + '))');
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
        if people_id == "-1" and form.d.FIO != "":
            people_id = getNextId('people')
            element = {"FIO": form.d.FIO,
                       "phone": form.d.phone,
                       "link": form.d.link,
                       "id": people_id}
            db.multiple_insert('people', values=[element])
        db.insert('group_people', renter_id=renter_id, group_id=group_id, people_id=people_id)
        raise web.seeother('/renter/' + str(renter_id) + "/" + str(group_id) + "/", True)
