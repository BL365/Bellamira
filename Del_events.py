# coding: utf8

from Common import *

class DelEvent():


    def GET(self):
        db.delete('renters', where='id=$renter_id', vars=locals())
        raise web.seeother('/renters/', True)