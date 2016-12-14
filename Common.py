from db_controller import *

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

render = web.template.render('templates', base='base')
