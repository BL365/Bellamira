# coding: utf8

from Common import *

from datetime import *

import time


class Hall():

    form = web.form.Form(
        web.form.Dropdown('drop', [], description='День'), web.form.Textbox('startTime', description='Время начала', pattern="\\d{1,2}:\\d{1,2}", size="5", maxlength="5"),
        web.form.Textbox('endTime', description='Время окончания', pattern="\\d{1,2}:\\d{1,2}", size="5", maxlength="5"), web.form.Textbox('cost', description='Стоимость', maxlength="5", size="5")
    )

    form2 = web.form.Form(
        web.form.Textbox('name', description='Название'), web.form.Dropdown('drop', [], description='Группа'),
        web.form.Textbox('start_time', pattern="\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2}", size="16", maxlength="16", id="st_t", description='Время начала'),
        web.form.Textbox('end_time', pattern="\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2}", size="16", maxlength="16", id="end_t", description='Время окончания')
    )

    def GET(self, hall_id):
        hall = db.select('hall', where='id=$hall_id', vars=locals())[0]
        zones = db.select('time_zone', where='hall_id=$hall_id', vars=locals())
        rate = db.select('rate_renter', order='days_of_week', where='hall_id=$hall_id', vars=locals())
        events = db.select('using_hall', order='start_time', where='hall_id=$hall_id', vars=locals())
        days = db.select('days_of_week', vars=locals())
        form = self.form()
        form2 = self.form2()
        temp = getdropValues2()
        form2.drop.args = temp
        drop_days = getdropValues4()
        form.drop.args = drop_days

        zones = list(zones)
        updeted_zones = []
        for t in zones:
            hours = t['start_time'] / 3600
            minutes = t['start_time'] % 3600 / 60
            t['start_time'] = "%02d:%02d" % (hours, minutes)

            hours = t['end_time'] / 3600
            minutes = t['end_time'] % 3600 / 60
            t['end_time'] = "%02d:%02d" % (hours, minutes)
            updeted_zones.append(t)

        event = db.select('using_hall', order='start_time', where='hall_id=$hall_id', vars=locals())

        # cost_table = db.query('SELECT using_hall.[hall_id], using_hall.[group_id], using_hall.[start_time], using_hall.[end_time], renters_group.[renter_id] AS RENTER, rate_renter.[days_of_week] AS DAYS_IND_RATE, rate_renter.[start_time] AS ST_T_IND_RATE, rate_renter.[end_time] AS EN_T_IND_RATE, rate_renter.[cost] AS IND_COST, time_zone.[days_of_week] AS DAYS_ST_RATE, time_zone.[start_time] AS ST_T_ST_RATE, time_zone.[end_time] AS EN_T_ST_RATE, time_zone.[cost] AS STAND_COST FROM using_hall INNER JOIN renters_group ON using_hall.[group_id] = renters_group.[id] INNER JOIN rate_renter ON renters_group.[renter_id] = rate_renter.[renter_id] INNER JOIN time_zone ON using_hall.[hall_id] = time_zone.[hall_id]')
        # hall_cost_table = []        #sdelat sopostavlenie vremeni zaniatia i tarifa, raschet stoimosti
        # for c in cost_table:
        #     if c['hall_id'] == hall_id:
        #         hall_cost_table.append(c)
        event = list(event)
        # for ev in event:
        #     # print "HEEEERREEEEEE в родительском цикле|", ev
        #     ev['start_time'] = datetime.fromtimestamp(ev['start_time'])
        #     ev['end_time'] = datetime.fromtimestamp(ev['end_time'])

        comb_rate = db.query('SELECT rate_renter.[id], rate_renter.[renter_id], rate_renter.[hall_id], rate_renter.[days_of_week], rate_renter.[start_time], rate_renter.[end_time], rate_renter.[cost], renters_group.[renter_id], renters_group.[id] AS group_id FROM rate_renter INNER JOIN renters_group ON rate_renter.[renter_id] = renters_group.[renter_id]')
        # print event
        comb_rate = list(comb_rate)
        event_ex = []
        delta = 0
        ind_rate_sum = 0
        rate_sum = 0
        updeted_zones1 = db.select('time_zone', where='hall_id=$hall_id', vars=locals())
        updeted_zones1 = list(updeted_zones1)
        event_lite = []
        while len(event)> 0:
            ev1 = event.pop()
            for r in (comb_rate + updeted_zones1):
                # print "родительский"
                if 'renter_id' in r:
                    if r['group_id'] == ev1['group_id']:
                        # print "вложенный", type(r['hall_id']), r['hall_id'], type(hall_id), hall_id
                        if r['hall_id'] == int(hall_id):
                            # print "совпал зал"
                            if r['group_id'] == ev1['group_id']:
                                # print "совпали  зал и группа",type(r['days_of_week'])
                                if type(r['days_of_week']) != type(delta):
                                    r['days_of_week'] = int(r['days_of_week'])
                                # print "ПРОВЕРКА ДНЯ!!!!!!!!!!!", ev1['name'], str(r['days_of_week'])
                                if ev1['name'] != str(r['days_of_week']):

                                    if datetime.fromtimestamp(ev1['start_time']).weekday() == r['days_of_week']:  # проверка дня
                                        print "совпал день"
                                        a = ev1['start_time']
                                        b = ev1['end_time']
                                        a = (a + 10800) % 86400 # смещение на 3 часа, необходимо, причина существования не понятна, возможно что-то с часовыми поясами
                                        b = (b + 10800) % 86400
                                        ev1['name'] = str(r['days_of_week'])
                                        if not b <= r['start_time']:
                                            if not a >= r['end_time']:
                                                print "HEEEERREEEEEE есть пересечение", a, b, r['start_time'], r['end_time'], r['cost'], r['id'], ev1['id']
                                                if a >= r['start_time'] and b <= r['end_time']:  # если соблюдается - сложить все часы этого тарифа и умножить на cost
                                                    print "время внутри", a, b, r['start_time'], r['end_time']
                                                    delta = r['end_time'] - r['start_time']
                                                    ev1['start_time'] = a
                                                    ev1['end_time'] = r['start_time']
                                                    event.append(ev1)
                                                    ev1['start_time'] = r['end_time']
                                                    ev1['end_time'] = b
                                                    cost = r['cost'] / 3600
                                                    cost = delta * cost
                                                    ind_rate_sum = ind_rate_sum + cost
                                                    print "сумма", cost, "|delta|", delta
                                                    print "сумма за время арендованное по индив тарифам", ind_rate_sum
                                                    event.append(ev1)
                            #                         print "продолжительность|добавлено в искл", delta
                                                elif a >= r['start_time']:
                                                    delta = r['end_time'] - a
                                                    a = int(r['end_time'])
                                                    ev1['start_time'] = a
                                                    ev1['end_time'] = b
                                                    print "добавление в event_lite 1|", ev1['id'], ev1['start_time'], ev1['end_time'], r['start_time'], r['end_time'], r['cost'], delta, a, b
                                                    cost = r['cost'] / 3600
                                                    cost = delta * cost
                                                    ind_rate_sum = ind_rate_sum + cost
                                                    print "сумма", cost, "|delta|", delta
                                                    print "сумма за время арендованное по индив тарифам", ind_rate_sum
                                                    event.append(ev1)
                                                elif b <= r['end_time']:
                                                    delta = b - r['start_time']
                                                    ev1['start_time'] = a
                                                    ev1['end_time'] = b
                                                    print "добавление в event_lite 2|", ev1['id'], ev1['start_time'], ev1['end_time'], r['start_time'], r['end_time'], r['cost'], delta

                                                    ev1['end_time'] = int(r['start_time'])
                                                    event.append(ev1)

                                                    cost = r['cost'] / 3600
                                                    print "cost for ind_rate|", r['cost']
                                                    cost = delta * cost

                                                    ind_rate_sum = ind_rate_sum + cost  # здесь скопится сумма по всем задействованным индивидуальным тарифам
                                                    print "сумма", cost, "|delta|", delta
                                                    print "сумма за время арендованное по индив тарифам", ind_rate_sum

                                elif ev1['name'] == str(r['days_of_week']):
                                    # print "ДЕНЬ  !!!!!!!! СОВПАЛ"
                                    if not ev1['end_time'] <= r['start_time']:
                                        if not ev1['start_time'] >= r['end_time']:
                                            print "пересечение В ОБРЕЗКАХ", ev1['start_time'], ev1['end_time'], r['start_time'], r['end_time'], r['cost'], r['id'], ev1['id']
                                            if ev1['start_time'] >= r['start_time'] and ev1['end_time'] <= r[
                                                'end_time']:  # если соблюдается - сложить все часы этого тарифа и умножить на cost
                                                print "время внутри", ev1['start_time'], ev1['end_time'], r['start_time'], r['end_time']
                                                delta = r['end_time'] - r['start_time']
                                                ev1['end_time'] = r['start_time']
                                                event.append(ev1)
                                                ev1['start_time'] = r['end_time']
                                                cost = r['cost'] / 3600
                                                cost = delta * cost
                                                ind_rate_sum = ind_rate_sum + cost
                                                print "сумма", cost, "|delta|", delta
                                                print "сумма за время арендованное по индив тарифам", ind_rate_sum
                                                event.append(ev1)
                                                #                         print "продолжительность|добавлено в искл", delta
                                            elif ev1['start_time'] >= r['start_time']:
                                                delta = r['end_time'] - ev1['start_time']
                                                ev1['end_time'] = ev1['end_time']
                                                print "добавление в event_lite 111|", ev1['id'], ev1[
                                                    'start_time'], ev1['end_time'], r['start_time'], r[
                                                    'end_time'], r['cost'], delta
                                                cost = r['cost'] / 3600
                                                cost = delta * cost
                                                ind_rate_sum = ind_rate_sum + cost
                                                print "сумма", cost, "|delta|", delta
                                                print "сумма за время арендованное по ВТОРИЧНЫМ индив тарифам", ind_rate_sum
                                                event.append(ev1)
                                            elif ev1['end_time'] <= r['end_time']:
                                                delta = ev1['start_time'] - r['start_time']
                                                print "добавление в event_lite 222|", ev1['id'], ev1['start_time'], ev1['end_time'], r['start_time'], r[
                                                    'end_time'], r['cost'], delta
                                                ev1['end_time'] = int(r['start_time'])
                                                event.append(ev1)

                                                print "cost for ind_rate|", r['cost']
                                                cost = r['cost'] / 3600
                                                cost = delta * cost
                                                ind_rate_sum = ind_rate_sum + cost
                                                print "сумма", cost, "|delta|", delta
                                                print "сумма за время арендованное по ВТОРИЧНЫМ индив тарифам", ind_rate_sum
                                              # здесь скопится сумма по всем задействованным индивидуальным тарифам
        print "сумма за время арендованное по ВТОРИЧНЫМ индив тарифам", ind_rate_sum




        updeted_events = []
        for e in events:
            e['start_time'] = datetime.fromtimestamp(e['start_time']).strftime("%d/%m/%Y (%a) %H:%M")
            e['end_time'] = datetime.fromtimestamp(e['end_time']).strftime("%d/%m/%Y (%a) %H:%M")
            for t in temp:
                if t[0] == e['group_id']:
                    e['group_id'] = t[1]
                    updeted_events.append(e)

        return render.prices(hall, updeted_zones, form, form2, updeted_events, ind_rate_sum)

    def POST(self, hall_id):
        form = self.form()
        form2 = self.form2()
        if not form.validates():
            raise web.seeother('/hall/' + str(hall_id) + "/", True)
        if not form2.validates():
            raise web.seeother('/hall/' + str(hall_id) + "/", True)

        if form.d.startTime and form.d.endTime != None:
            stT = form.d.startTime
            enT = form.d.endTime
            print "here          here            here         69     |", stT, "|", enT
            stSec = int(stT[0:2]) * 3600 + int(stT[3:5]) * 60
            enSec = int(enT[0:2]) * 3600 + int(enT[3:5]) * 60

            days_of_week = getdropValues4()
            day_name = "Вт"
            print type(days_of_week)
            # for d in days_of_week:
                # print "here  ", type(d['no']), d['no'], type(form.d.drop), form.d.drop
                # if d['no'] == int(form.d.drop):
                #     day_name = d['name']
            if form.d.drop != "-1":
                element = {"id": getNextId("time_zone"),
                           "hall_id": hall_id,
                           "days_of_week": form.d.drop,
                           "start_time": stSec,
                           "end_time": enSec,
                           "cost": form.d.cost}
                db.multiple_insert('time_zone', values=[element])
            raise web.seeother('/hall/' + str(hall_id) + "/", True)

        if form2.d.start_time and form2.d.end_time != None:
            if form2.d.drop != "-1":
                start_dt_string2 = datetime.strptime(form2.d.start_time, "%d/%m/%Y %H:%M")
                start_dt_unix2 = time.mktime(start_dt_string2.timetuple())
                end_dt_string2 = datetime.strptime(form2.d.end_time, "%d/%m/%Y %H:%M")
                end_dt_unix2 = time.mktime(end_dt_string2.timetuple())
                element2 = {"id": getNextId("using_hall"),
                           "name": form2.d.name,
                           "group_id": form2.d.drop,
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
    form = web.form.Form(web.form.Textbox('name', description='Зал'), web.form.Textbox('square', description='Площаль'))

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