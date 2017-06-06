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
    '/deltimezone/(\\d+)/(\\d+)?', 'DelTimezone',
    '/prices/(\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2})/(\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2})/(\\d+)/', 'CheckTime'
    '/delrenter/(\\d+)?', 'DelRenter', #url for new class delRenter
    '/home/(\\d+)?', 'Home'#url for new page Home

)

render = web.template.render('templates', base='base')