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
        for t in zones:#создание списка общих тарифов в "человеческом" формате времени
            hours = t['start_time'] / 3600
            minutes = t['start_time'] % 3600 / 60
            t['start_time'] = "%02d:%02d" % (hours, minutes)
            hours = t['end_time'] / 3600
            minutes = t['end_time'] % 3600 / 60
            t['end_time'] = "%02d:%02d" % (hours, minutes)
            updeted_zones.append(t)

        event = db.select('using_hall', order='start_time', where='hall_id=$hall_id', vars=locals())
        event = list(event)
        comb_rate = db.query('SELECT rate_renter.[id], rate_renter.[renter_id], rate_renter.[hall_id], rate_renter.[days_of_week], rate_renter.[start_time], rate_renter.[end_time], rate_renter.[cost], renters_group.[id] AS group_id FROM rate_renter INNER JOIN renters_group ON rate_renter.[renter_id] = renters_group.[renter_id]')
        # comb_rate создано для возможности сопоставления группы и индивидуального тарифа
        comb_rate = list(comb_rate)
        ind_rate_sum = 0

        # event_lite = []
        up_ev = []
        for l1 in event:
            if l1['start_time'] > 86400 and l1['end_time'] > 86400:
                # if l1['hall_id'] == int(hall_id):
                l1['name'] = str(datetime.fromtimestamp(l1['start_time']).weekday())
                l1['start_time'] = (l1['start_time'] + 10800) % 86400 # смещение на 3 часа, необходимо, причина существования не ясна, возможно что-то с часовыми поясами                                                    #
                l1['end_time'] = (l1['end_time'] + 10800) % 86400 #перевод времени из unix в секунды от начала суток
                up_ev.append(l1)#сюда попадают занятия, с измененным временем, и с номером дня недели в названии
        #del event[:]

        up_ev1 = []
        while len(up_ev) > 0:  # перевод занятий-подсписков в формат кортежа из формата списка
            e1 = up_ev.pop()
            e1 = (e1['id'], e1['name'], e1['group_id'], e1['hall_id'], e1['start_time'], e1['end_time'])
            up_ev1.append(e1)
        print "up_ev1 LEN", len(up_ev1)
        del up_ev[:]
        event_lite = []
        ex_ev = []
        while len(up_ev1) > 0: #пока занятия в списке
            print "весь up_ev1", up_ev1
            ev1 = up_ev1.pop() #взятие последнего элемента списка

            print "up_ev1 LEN", len(up_ev1), ev1[0], ev1[4], ev1[5]

            for r in comb_rate:#здесь по совпадающему залу, группе, дню недели, времени занятия и времени тарифа высчитывается стоимость
                # if int(ev1[0]) == 13:
                    # print "ИНДИВИДЫ второго порядка", ev1[4], ev1[5]
                if r['group_id'] == ev1[2] and int(r['hall_id']) == int(ev1[3]):
                    if int(ev1[1]) == int(r['days_of_week']):
                        a = ev1[4]
                        b = ev1[5]
                        if not b <= r['start_time'] and not a >= r['end_time']:
                            # print "занятие, расчет индивидуальных", ev1
                            ex_ev.append(ev1)
                            if a >= r['start_time'] and b <= r['end_time']:  # время внутри тарифа
                                cost = delta(ev1[5], ev1[4], r['cost'])
                                print "блок 1"
                            elif a < r['start_time'] and b > r['end_time']:
                                print "блок2"
                                if int(ev1[0]) == 13:
                                    print "13ое занятие, расчет индивидуальных блок2", ev1
                                cost = delta(r['end_time'], r['start_time'], r['cost'])

                                tz2 = (ev1[0], ev1[1], ev1[2], ev1[3], ev1[4], r['start_time'])
                                up_ev1.append(tz2)

                                if int(ev1[0]) == 13:
                                    print "отправка tz2", tz2
                                del tz2
                                tz = (ev1[0], ev1[1], ev1[2], ev1[3], r['end_time'], ev1[5])
                                up_ev1.append(tz)
                                if int(ev1[0]) == 13:
                                    print "отправка tz", tz
                                del tz
                            elif a >= r['start_time']:
                                cost = delta(r['end_time'], a, r['cost'])
                                tz = (ev1[0], ev1[1], ev1[2], ev1[3], r['end_time'], ev1[5])
                                # print "отправка обрезков", ev1[4], ev1[5]
                                up_ev1.append(tz)
                                del tz
                                print "блок 3"
                            else: #b <= r['end_time']
                                cost = delta(b, r['start_time'], r['cost'])
                                tz = (ev1[0], ev1[1], ev1[2], ev1[3], ev1[4], r['start_time'])
                                # print "отправка обрезков", ev1['start_time'], ev1['end_time']
                                up_ev1.append(tz)
                                del tz
                                print "блок 4"
                            ind_rate_sum = ind_rate_sum + cost
                            print cost
                            break
                        else:
                            event_lite.append(ev1)
                    else:
                        event_lite.append(ev1)
                else:
                    event_lite.append(ev1)

        event_lite = set(event_lite)#создание множества из списка занятий, для удаления дубликатов занятий

        ex_ev1 = []
        if len(ex_ev) > 0:
            # while ex_ev:# перевод занятий-подсписков в формат кортежа из формата списка
            #     a1 = ex_ev.pop()
            #     a1 = (a1['id'], a1['name'], a1['group_id'], a1['hall_id'], a1['start_time'], a1['end_time'])
            #     ex_ev1.append(a1)
            ex_ev = set(ex_ev)
            event_lite = event_lite - ex_ev
        for i1111 in event_lite:
            if i1111[0] == 13:
                print "13ый кортеж в event_lite", i1111[0], i1111[4], i1111[5]
        event_lite = list(event_lite)#перевод списка занятий из формата множества в список
        event_lite1 = []
        for e2 in event_lite:#перевод занятий из кортежа в список
            e2 = list(e2)
            event_lite1.append(e2)
        # del event_lite[:]
        zones1 = db.select('time_zone', where='hall_id=$hall_id', vars=locals())
        zones1 = list(zones1)
        pub_sum = 0
        # del event_lite1[:]
        # event_lite1 = []
        # event_lite1 = lite_ev
        while len(event_lite1) > 0:
            av = event_lite1.pop()
            for z1 in zones1:
                if int(av[1]) == int(z1['days_of_week']) and int(av[3]) == int(z1['hall_id']):
                    if not av[5] <= z1['start_time'] and not av[4] >= z1['end_time']:
                        if av[0] == 13:
                            print "13ое занятие подсчет в общих----------------------------------------"
                        a = av[4]
                        b = av[5]
                        if a >= z1['start_time'] and b <= z1['end_time']:
                            cost = delta(b, a, z1['cost'])
                        elif a < z1['start_time'] and b > z1['end_time']:
                            cost = delta(z1['end_time'], z1['start_time'], z1['cost'])
                            av[5] = z1['end_time']
                            event_lite1.append(av)
                            av[4] = z1['end_time']
                            av[5] = b
                            event_lite1.append(av)
                        elif a >= z1['start_time']:
                            cost = delta(z1['end_time'], a, z1['cost'])
                            av[4] = z1['end_time']
                            event_lite1.append(av)
                        else:  # av[5] <= z1['end_time']
                            cost = delta(b, z1['start_time'], z1['cost'])
                            av[5] = z1['start_time']
                            event_lite1.append(av)
                        pub_sum = pub_sum + cost
                        print "cost", cost
                        print "pub_sum", pub_sum
        sum = ind_rate_sum + pub_sum

        updeted_events = []
        for e in events:
            e['start_time'] = datetime.fromtimestamp(e['start_time']).strftime("%d/%m/%Y (%a) %H:%M")
            e['end_time'] = datetime.fromtimestamp(e['end_time']).strftime("%d/%m/%Y (%a) %H:%M")
            for t in temp:
                if t[0] == e['group_id']:
                    e['group_id'] = t[1]
                    updeted_events.append(e)

        return render.prices(hall, updeted_zones, form, form2, updeted_events, ind_rate_sum, pub_sum, sum)

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