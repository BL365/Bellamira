# coding: utf8

from Common import *

from datetime import *

import time


class Renter:
    form = web.form.Form(
        web.form.Textbox('name', description='Название группы'), web.form.Dropdown('drop8', [], description='Руководитель'),
        # web.form.Checkbox('other', description='Новый?'),
        web.form.Textbox('FIO', description='ФИО нового руководителя'),
        web.form.Textbox('phone', description='Телефон'), web.form.Textbox('link', description='Ссылка в соц. сетях')
    )

    form2 = web.form.Form(web.form.Textbox('date', description='Дата', pattern="\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2}", size="16", maxlength="16"),
                          web.form.Textbox('sum', description='Сумма'))

    form3 = web.form.Form(web.form.Dropdown('drop', [], description='Группа'), web.form.Dropdown('drop2', [], description='Зал'),
                          web.form.Textbox('name', description='Название'),
                          web.form.Textbox('start_time', pattern="\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2}",
                                           size="16", maxlength="16", id="st_t", description='Время начала'),
                          web.form.Textbox('end_time', pattern="\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2}",
                                           size="16", maxlength="16", id="end_t", description='Время окончания'))

    form4 = web.form.Form(web.form.Dropdown('drop', [], description='Зал'),
                          web.form.Dropdown('drop2', [], description='День недели'),
                          web.form.Textbox('start_time', description='Время начала', pattern="\\d{1,2}:\\d{1,2}",
                                           size="5", maxlength="5"),
                          web.form.Textbox('end_time', description='Время окончания', pattern="\\d{1,2}:\\d{1,2}",
                                           size="5", maxlength="5"),
                          web.form.Textbox('cost', description='Стоимость часа'))

    def GET(self, renter_id):
        groups = db.select("renters_group", where='renter_id = $renter_id', vars=locals())
        people = db.query('Select * from people where id in (select people_id from group_people where renter_id = '
                          + str(renter_id) + ')');
        renter = db.select("renters", where="id=$renter_id", vars=locals())[0]
        renter_man = db.select("people", where="id = $renter.people_id", vars=locals())[0]
        pays = db.select("pays", where='renter_id = $renter_id', vars=locals())
        rate = db.select('rate_renter', where='renter_id=$renter_id', vars=locals())
        events_groups = db.query('SELECT  using_hall.[id], using_hall.[name], using_hall.[hall_id], using_hall.[group_id], using_hall.[start_time], using_hall.[end_time], renters_group.[renter_id] AS renter, renters_group.[name] AS group_name, hall.[name] AS hall_name FROM renters_group INNER JOIN using_hall ON renters_group.[id] = using_hall.[group_id] INNER JOIN hall ON using_hall.[hall_id] = hall.[id]')
        cost_table = db.query('SELECT using_hall.[hall_id], using_hall.[group_id], using_hall.[start_time], using_hall.[end_time], renters_group.[renter_id] AS RENTER, rate_renter.[days_of_week] AS DAYS_IND_RATE, rate_renter.[start_time] AS ST_T_IND_RATE, rate_renter.[end_time] AS EN_T_IND_RATE, rate_renter.[cost] AS IND_COST, time_zone.[days_of_week] AS DAYS_ST_RATE, time_zone.[start_time] AS ST_T_ST_RATE, time_zone.[end_time] AS EN_T_ST_RATE, time_zone.[cost] AS STAND_COST FROM using_hall INNER JOIN renters_group ON using_hall.[group_id] = renters_group.[id] INNER JOIN rate_renter ON renters_group.[renter_id] = rate_renter.[renter_id] INNER JOIN time_zone ON using_hall.[hall_id] = time_zone.[hall_id]')
        days = db.query('SELECT * FROM days_of_week')
        form = self.form()
        form.drop8.args = getdropValues()
        form2 = self.form2()
        form3 = self.form3()
        drop_hall = getdropValues3()
        form3.drop2.args = drop_hall
        form3.drop.args = getdropValues2()
        form4 = self.form4()
        form4.drop.args = drop_hall
        drop_days = getdropValues4()
        form4.drop2.args = drop_days

        if events_groups != None:
            uppd_ev_groups = []
            for e in events_groups:
                e['start_time'] = datetime.fromtimestamp(e['start_time']).strftime("%d/%m/%Y (%a) %H:%M")
                e['end_time'] = datetime.fromtimestamp(e['end_time']).strftime("%d/%m/%Y (%a) %H:%M")
                if e['renter'] == int(renter_id):
                    uppd_ev_groups.append(e)
            print "HERREEE ИТератор прошел цикл|"

        if pays != None:
            updeted_pays = []
            print "HEEEERREEEEEE ИТератор перед pays|"
            for p in pays:
                p['date'] = datetime.fromtimestamp(p['date']).strftime("%d/%m/%Y (%a) %H:%M")
                updeted_pays.append(p)


        updated_rate = []
        for i in rate:
            # print "начало  in rate|", type(i['days_of_week']), i['days_of_week']
            i['days_of_week'] = str(i['days_of_week'])
            # print "после преобразования|", type(i['days_of_week']), i['days_of_week']
            hours = i['start_time'] / 3600
            minutes = i['start_time'] % 3600 / 60  # здесь время переводится в часы и минуты
            i['start_time'] = "%02d:%02d" % (hours, minutes)
            hours = i['end_time'] / 3600
            minutes = i['end_time'] % 3600 / 60
            i['end_time'] = "%02d:%02d" % (hours, minutes)
            for d in drop_hall:# здесь id заменяется названием
                # print "цикл дроп-зал", type(d[0]), d[0], type(i['hall_id']), i['hall_id']
                if d[0] == i['hall_id']:
                    i['hall_id'] = d[1]
                    updated_rate.append(i)# здесь формируется список тарифов, без замены дня недели с номера на сокращенное название
        updated_rate1 = list(updated_rate)
        updated_rate2 = []
        days = list(days)
        for up in updated_rate1:
            print type(days)
            for dn in days:  # здесь номер дня недели тарифа заменяется названием. В этот цикл итератор заходит только 1 раз
                # print "начало итерации дней"
                # up['days_of_week'] = str(up['days_of_week'])
                # dn['no'] = str(dn['no'])
                # print "HEEEEREEEEEEEEE  дни перед сравнением", type(up['days_of_week']), up['days_of_week'], "|", type(dn['no']), dn['no']
                if type(dn['no']) != type(up['days_of_week']):
                    dn['no'] = str(dn['no'])
                    # print "HEEEEREEEEEEEEE  после", type(up['days_of_week']), up[
                    #     'days_of_week'], "|", type(dn['no']), dn['no']
                if up['days_of_week'] == dn['no']:
                    up['days_of_week'] = dn['name']
                    updated_rate2.append(up)

        ind_rate_sum = 0
        events = db.query('SELECT using_hall.[id], using_hall.[group_id], using_hall.[hall_id], using_hall.[name], using_hall.[start_time], using_hall.[end_time], renters_group.[renter_id], renters_group.[id] AS group_id FROM using_hall INNER JOIN renters_group ON using_hall.[group_id] = renters_group.[id]')
        comb_rate = db.query('SELECT rate_renter.[id], rate_renter.[renter_id], rate_renter.[hall_id], rate_renter.[days_of_week], rate_renter.[start_time], rate_renter.[end_time], rate_renter.[cost], renters_group.[renter_id], renters_group.[id] AS group_id FROM rate_renter INNER JOIN renters_group ON rate_renter.[renter_id] = renters_group.[renter_id]')
        comb_rate = list(comb_rate)
        if comb_rate != None:
            events = list(events)
            delta = 0
            cost = 0
            while len(events) > 0:
                c = events.pop()
                # c['start_time'] = datetime.fromtimestamp(c['start_time'])
                # c['end_time'] = datetime.fromtimestamp(c['end_time'])
                # print "c ReNTER", type(c['RENTER']), c['RENTER'], type(rate2), rate2
                # print "в цикле", type(rate2), type(comb_rate), rate2
                for r in comb_rate:
                    # print "in rate", type(c['renter_id']), type(renter_id)
                    if c['renter_id'] == int(renter_id) and c['renter_id'] == r['renter_id']:
                        # print "совпал арендатор", c['renter_id'], int(renter_id), r['renter_id']
                        if c['group_id'] == r['group_id']:
                            if c['hall_id'] == r['hall_id']:#тот ли зал
                                # print "HEEREE совпал зал|",  c['hall_id'], "|", r['hall_id']
                                r['days_of_week'] = int(r['days_of_week'])
                                # print "HEEEERREEEEEE день|", type(r['days_of_week']), r['days_of_week']
                                if c['name'] != str(r['days_of_week']):
                                    if datetime.fromtimestamp(c['start_time']).weekday() == r['days_of_week']:#тот ли день, если тот, то сначала преобразование в один тип исчисления с тарифами
                                        # print "HEEEERREEEEEE совпали группа, зал, день|", r['id'], c['id'], c['group_id'], r['group_id'], c['hall_id'], r['hall_id']
                                        # print "!", r['days_of_week'], r['days_of_week']
                                        a = (c['start_time'] + 10800) % 86400
                                        b = (c['end_time'] + 10800) % 86400
                                        print "DAY!!!!!!",  r['days_of_week'], datetime.fromtimestamp(c['start_time']).weekday()
                                        c['name'] = str(datetime.fromtimestamp(c['start_time']).weekday())
                                        if not b <= r['start_time']:
                                            if not a >= r['end_time']:
                                                print "HEEREEE пересечение", a, b, r['start_time'], r['end_time'], r['cost'], r['id'], c['id']
                                                if a >= r['start_time'] and b <= r['end_time']:# если соблюдается - сложить все часы этого тарифа и умножить на cost, если соблюдается - искать пересекающиеся и считать
                                                    print "HERE all in", a, b, r['start_time'], r['end_time'], r['id'], c['id'], ":id|days:", str(r['days_of_week']), datetime.fromtimestamp(c['start_time']).weekday()
                                                    delta = c['end_time'] - c['start_time']
                                                    print "сумма|", r['cost'], "delta|", delta
                        #                             print "HEEEERREEEEEE стоимость использованного времени тарифа|"

                                                elif a < r['start_time'] and b > r['end_time']:
                                                    print "HERE where big", a, b, r['start_time'], r['end_time'], r['id'], c[
                                                        'id']
                                                    delta = r['end_time'] - r['start_time']
                                                    print "сумма|", r['cost'], "delta|", delta
                                                    c['start_time'] = a
                                                    c['end_time'] = r['start_time']
                                                    events.append(c)
                                                    c['start_time'] = r['end_time']
                                                    c['end_time'] = b
                                                    events.append(c)

                                                elif a >= r['start_time']:
                                                    print "HERE старт занятия в тарифе", a, b, r['start_time'], r['end_time'], r['id'], c['id']
                                                    delta = r['end_time'] - a
                                                    a = int(r['end_time'])
                                                    c['start_time'] = r['end_time']
                                                    c['end_time'] = b
                                                    events.append(c)
                                                    print "HERE доб-е обрезка", c['start_time'], c['end_time']
                                                    print "сумма|", r['cost'], "delta|", delta
                                                elif b <= r['end_time']:
                                                    delta = b - r['start_time']
                                                    print "HERE end занятия в тарифе", a, b, r['start_time'], r['end_time'], r['id'], c['id']
                                                    print "сумма|", r['cost'], "delta|", delta
                                                    c['end_time'] = r['start_time']
                                                    c['start_time'] = a
                                                    events.append(c)
                                                    print "HERE доб-е обрезка", c['start_time'], c['end_time']
                                                    print "сумма|", r['cost'], "delta|", delta
                                                cost = r['cost'] / 3600
                                                cost = delta * cost
                                                print "сумма", cost, "|delta|", delta
                                                ind_rate_sum = ind_rate_sum + cost#здесь скопится сумма по всем задействованным индивидуальным тарифам
                                                print "сумма за время арендованное по индивидуальным тарифам", ind_rate_sum
                                elif c['name'] == str(r['days_of_week']):
                                    print "day 111111111111111111111111", c['name'],  str(r['days_of_week'])
                                    if not c['end_time'] <= r['start_time']:
                                        if not c['start_time'] >= r['end_time']:
                                            print "HEEREEE пересечение", c['start_time'], c['end_time'], r['start_time'], r['end_time'], r[
                                                'cost'], r['id'], c['id']
                                            if c['start_time'] >= r['start_time'] and c['end_time'] <= r[
                                                'end_time']:  # если соблюдается - сложить все часы этого тарифа и умножить на cost, если соблюдается - искать пересекающиеся и считать
                                                print "HERE all in обр", c['start_time'], c['end_time'], r['start_time'], r['end_time'], r['id'], c['id'], ":id|days:", str(r['days_of_week']), c['name']
                                                delta = c['end_time'] - c['start_time']
                                                print "сумма|", r['cost'], "delta|", delta
                                                #                             print "HEEEERREEEEEE стоимость использованного времени тарифа|"

                                            elif c['start_time'] < r['start_time'] and c['end_time'] > r['end_time']:
                                                print "HERE where big", c['start_time'], c['end_time'], r['start_time'], r['end_time'], r['id'], c['id']
                                                delta = r['end_time'] - r['start_time']
                                                print "сумма|", r['cost'], "delta|", delta

                                                c['end_time'] = r['start_time']
                                                events.append(c)
                                                c['start_time'] = r['end_time']

                                                events.append(c)

                                            elif c['start_time'] >= r['start_time']:
                                                print "HERE старт занятия в тарифе", c['start_time'], c['end_time'], r['start_time'], r[
                                                    'end_time'], r['id'], c['id']
                                                delta = r['end_time'] - c['start_time']
                                                c['start_time'] = int(r['end_time'])


                                                events.append(c)
                                                print "HERE доб-е обрезка", c['start_time'], c['end_time']
                                                print "сумма|", r['cost'], "delta|", delta
                                            elif c['end_time'] <= r['end_time']:
                                                delta = c['end_time'] - r['start_time']
                                                print "HERE end занятия в тарифе", c['start_time'], c['end_time'], r['start_time'], r['end_time'], \
                                                r['id'], c['id']
                                                print "сумма|", r['cost'], "delta|", delta
                                                c['end_time'] = r['start_time']

                                                events.append(c)
                                                print "HERE доб-е обрезка", c['start_time'], c['end_time']
                                                print "сумма|", r['cost'], "delta|", delta
                                            cost = r['cost'] / 3600
                                            cost = delta * cost
                                            print "сумма", cost, "|delta|", delta
                                            ind_rate_sum = ind_rate_sum + cost  # здесь скопится сумма по всем задействованным индивидуальным тарифам
                                            print "сумма за время арендованное по индивидуальным тарифам c обрезками", ind_rate_sum

        print "HEEEERRREEE ИТератор перед return|"
        # updated_rate3 = []
        # for s in updated_rate2:
        #     if s['days_of_week'] == "Пн":
        #         updated_rate3.append(s)
        #     if s['days_of_week'] == "Вт":
        #         updated_rate3.append(s)
        #     if s['days_of_week'] == "Ср":
        #         updated_rate3.append(s)
        #     if s['days_of_week'] == "Чт":
        #         updated_rate3.append(s)
        #     if s['days_of_week'] == "Пт":
        #         updated_rate3.append(s)
        #     if s['days_of_week'] == "Сб":
        #         updated_rate3.append(s)
        #     if s['days_of_week'] == "Вс":
        #         updated_rate3.append(s)
        return render.renter(renter, renter_man, groups, people, updated_rate2, updeted_pays, uppd_ev_groups, form, form2, form3, form4)

    def POST(self, renter_id):
        print "ИТЕРАТОР В КЛАССЕ РЕНТЕР _ ПОСТ   "
        form = self.form()
        form2 = self.form2()
        form3 = self.form3()
        form4 = self.form4()
        if not form.validates():
            raise web.seeother('/renter/' + str(renter_id) + "/", True)
        if not form2.validates():
            raise web.seeother('/renter/' + str(renter_id) + "/", True)
        if not form3.validates():
            raise web.seeother('/renter/' + str(renter_id) + "/", True)
        if not form4.validates():
            raise web.seeother('/renter/' + str(renter_id) + "/", True)


        if form.d.name != "занятие" and form.d.drop8 != "-1" and form.d.drop8 != -1 and form.d.name != "занятие":
            print "HEEEEEEEEEEEEEEEEEERRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEE FORM1111111 !!!!!!!!!", form.d.name, form.d.drop8
            people_id = getNextId('people')
            # print "HERE!!!", type(form.d.other), form.d.other
            print "HERE!!!", type(form.d.drop8), form.d.drop8
            group_id = getNextId('renters_group')
            print form, "here form1"
            form.d.drop8 = int(form.d.drop8)
            renter_id = int(renter_id)
            if form.d.drop8 != "-1":

                element = {"id": group_id,
                           "people_id": form.d.drop8,
                           "name": form.d.name,
                           "renter_id": renter_id}
                print "True ", type(group_id), group_id, type(people_id), people_id, type(form.d.name), form.d.name, type(renter_id), renter_id, type(form.d.drop8), form.d.drop8
                db.multiple_insert("renters_group", values=[element])
                db.insert("group_people", renter_id=renter_id, group_id=group_id, people_id=form.d.drop8)
            elif form.d.drop8 == "-1":
                print form.d.FIO, form.d.phone
                if form.d.FIO != "" and form.d.phone != "":
                    element = {"FIO": form.d.FIO,
                               "phone": form.d.phone,
                               "link": form.d.link,
                               "id": people_id}
                    print "False ", form.d.FIO, form.d.phone, form.d.link, people_id
                    db.multiple_insert('people', values=[element])
                    element = {"id": group_id,
                               "people_id": people_id,
                               "name": form.d.name,
                               "renter_id": renter_id
                               }
                    print "false ", type(group_id), group_id, type(people_id), people_id, type(form.d.name), form.d.name, type(renter_id), renter_id

                    db.multiple_insert("renters_group", values=[element])
                    db.insert("group_people", renter_id=renter_id, group_id=group_id, people_id=people_id)
            raise web.seeother('/renter/' + str(renter_id) + "/", True)


        if form2.d.sum != None:
            print "HEEEEEEEEEEEEEEEEEERRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEE FORM2222222 !!!!!!!!!",  form2.d.date, form2.d.sum
            dt_pays = datetime.now()
            dt = datetime.strptime(form2.d.date, "%d/%m/%Y %H:%M")
            print dt
            dt2 = time.mktime(dt.timetuple())
            print dt2
            element = {"id": getNextId("pays"),
                       "date": dt2,
                       "renter_id": renter_id,
                       "sum": form2.d.sum}
            db.multiple_insert('pays', values=[element])
            raise web.seeother('/renter/' + str(renter_id) + "/", True)
            # if form2.d.date == None:
            #     print "HERE    HERE HERE |", dt_pays
            #     dt_p = time.mktime(dt_pays.timetuple())
            #     print "HERE    HERE HERE |", dt_p
            #     element = {"id": getNextId("pays"),
            #                "date": dt_p,
            #                "renter_id": renter_id,
            #                "sum": form2.d.sum}
            #     db.multiple_insert('pays', values=[element])
            #     raise web.seeother('/renter/' + str(renter_id) + "/", True)
            # elif form2.d.date != None:
                # # dt_pays = datetime.now() = datetime.datetime(2017, 6, 20, 12, 17, 17, 146000)
                #
                # month = int(form2.d.date[3:5])
                # day = int(form2.d.date[0:2])
                # print type(month), month, type(day), day
                # datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0,
                # print dt_pays.year
                # dt = []
                # dt = day, "/", month, "/", dt_pays.year, "00:00"
                # print dt, "dt"
                # dt = str(dt)
                # print dt, "dt"
                # dt = datetime.strptime(form2.d.date, "%d/%m/%Y %H:%M")
                # print dt
                # dt2 = time.mktime(dt.timetuple())
                # print dt2
                # element = {"id": getNextId("pays"),
                #            "date": dt2,
                #            "renter_id": renter_id,
                #            "sum": form2.d.sum}
                # db.multiple_insert('pays', values=[element])
                # raise web.seeother('/renter/' + str(renter_id) + "/", True)

        # print form3.d.drop
        # print form3.d.drop2
        # print form3.d.start_time
        # print form3.d.end_time
        # print form3.d.name


        if form3.d.start_time != None and form3.d.end_time != None and form3.d.name != None:
            if form3.d.drop != "-1" and form3.d.drop2 != "-1":
                start_dt_string2 = datetime.strptime(form3.d.start_time, "%d/%m/%Y %H:%M")
                start_dt_unix2 = time.mktime(start_dt_string2.timetuple())
                end_dt_string2 = datetime.strptime(form3.d.end_time, "%d/%m/%Y %H:%M")
                end_dt_unix2 = time.mktime(end_dt_string2.timetuple())

                element2 = {"id": getNextId("using_hall"),
                           "name": form3.d.name,
                           "group_id": form3.d.drop,
                           "hall_id": form3.d.drop2,
                           "start_time": start_dt_unix2,
                           "end_time": end_dt_unix2}
                db.multiple_insert("using_hall", values=[element2])



        if form4.d.drop != "-1" and renter_id != "-1" and form4.d.cost != None and form4.d.drop2 != "-1":
            print "HEEEEEEEEEEEEEEEEEERRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEE FORM444444444 !!!!!!!!!"
            HALL_ID = form4.d.drop
            rate_id = getNextId('rate_renter')

            stT = form4.d.start_time
            enT = form4.d.end_time
            stSec = int(stT[0:2]) * 3600 + int(stT[3:5]) * 60
            enSec = int(enT[0:2]) * 3600 + int(enT[3:5]) * 60
            element2 = {"hall_id": HALL_ID,
                        "renter_id": renter_id,
                        "days_of_week": form4.d.drop2,
                        "start_time": stSec,
                        "end_time": enSec,
                        "cost": form4.d.cost,
                        "id": rate_id
                        }
            db.multiple_insert('rate_renter', values=[element2])
        raise web.seeother('/renter/' + str(renter_id) + "/", True)

class Renters:

    form = web.form.Form(
        web.form.Textbox('name', description='Название организации'), web.form.Textbox('renter_link', description='Ссылка'),
        web.form.Textbox('renter_phone', description='Телефон'), web.form.Dropdown('drop', [(-1, "Add")], description='Выберите руководителя'),
        web.form.Checkbox('other', description='Новый руководитель'),
        web.form.Textbox('FIO', description='ФИО руководителя'),
        web.form.Textbox('phone', description='Телефон'), web.form.Textbox('link', description='Ссылка в соц. сетях')
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


class DelRenter:

    def GET(self, renter_id):
        print "                   HEREEEEEEEEEEEEEE          |",  renter_id
        db.delete('renters', where='id=$renter_id', vars=locals())
        raise web.seeother('/renters/', True)
