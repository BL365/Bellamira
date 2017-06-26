# coding: utf8

from Common import *

class DelEvent():

    def GET(self, renter_id, event_id):
        db.delete('using_hall', where='id=$event_id', vars=locals())
        raise web.seeother('/renter/' + str(renter_id) + "/", True)


class DelPay():

    def GET(self, renter_id, pay_id):
        db.delete('pays', where='id=$pay_id', vars=locals())
        raise web.seeother('/renter/' + str(renter_id) + "/", True)


class DelTimezone():

    def GET(self, hall_id, zone_id):
        db.delete('time_zone', where='id=$zone_id', vars=locals())
        raise web.seeother('/hall/' + str(hall_id) + "/", True)


class DelIndRate():

    def GET(self, renter_id, rate_id):
        db.delete('rate_renter', where='id=$rate_id', vars=locals())
        raise web.seeother('/renter/' + str(renter_id) + "/", True)

class DelGroup():

    def GET(self, renter_id, group_id):
        db.delete('renters_group', where='id=$group_id', vars=locals())
        raise web.seeother('/renter/' + str(renter_id) + "/", True)

class DelPeople():

    def GET(self, renter_id, people_id ):
        db.delete('people', where='id=$people_id', vars=locals())
        raise web.seeother('/renter/' + str(renter_id) + "/", True)
