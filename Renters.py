# coding: utf8

from Common import *

from datetime import *

import time


class Renter:
    form = web.form.Form(
        web.form.Textbox('name', description='Название группы'), web.form.Dropdown('drop', [], description='Руководитель'),
        web.form.Checkbox('other', description='Новый?'), web.form.Textbox('FIO', description='ФИО нового руководителя'),
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
        events_groups = db.query('SELECT using_hall.[name], using_hall.[hall_id], using_hall.[group_id], using_hall.[start_time], using_hall.[end_time], renters_group.[renter_id] AS renter, renters_group.[name] AS group_name, hall.[name] AS hall_name FROM renters_group INNER JOIN using_hall ON renters_group.[id] = using_hall.[group_id] INNER JOIN hall ON using_hall.[hall_id] = hall.[id]')
        cost_table = db.query('SELECT using_hall.[hall_id], using_hall.[group_id], using_hall.[start_time], using_hall.[end_time], renters_group.[renter_id] AS RENTER, rate_renter.[days_of_week] AS DAYS_IND_RATE, rate_renter.[start_time] AS ST_T_IND_RATE, rate_renter.[end_time] AS EN_T_IND_RATE, rate_renter.[cost] AS IND_COST, time_zone.[days_of_week] AS DAYS_ST_RATE, time_zone.[start_time] AS ST_T_ST_RATE, time_zone.[end_time] AS EN_T_ST_RATE, time_zone.[cost] AS STAND_COST FROM using_hall INNER JOIN renters_group ON using_hall.[group_id] = renters_group.[id] INNER JOIN rate_renter ON renters_group.[renter_id] = rate_renter.[renter_id] INNER JOIN time_zone ON using_hall.[hall_id] = time_zone.[hall_id]')
        days = db.query('SELECT * FROM days_of_week')
        form = self.form()
        form.drop.args = getdropValues()
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

        ind_rate_sum = 0
        rate2 = rate
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
        # updated_rate1 = []
        # for up in updated_rate:
        #     print type(days)
        #     for dn in days:  # здесь номер дня недели тарифа заменяется названием. В этот цикл итератор заходит только 1 раз
        #         # print "начало итерации дней"
        #         # up['days_of_week'] = str(up['days_of_week'])
        #         dn['no'] = str(dn['no'])
        #         print "HEEEEREEEEEEEEE  ДНИ перед сравнением", type(up['days_of_week']), up['days_of_week'], "|", type(
        #             dn['no']), dn['no']
        #         if up['days_of_week'] == dn['no']:
        #             up['days_of_week'] = str(dn['name'])
        #             updated_rate1.append(up)  # здесь, по идее, это должно изменяться
        #             print "произведена замена|", type(up['days_of_week']), up['days_of_week'], "|", type(dn['no']), dn[
        #                 'no']
        #         print "выход из days", type(up['days_of_week']), up['days_of_week'], "|", type(dn['no']), dn['no']
        #     print "end step updRate", type(up['days_of_week']), up['days_of_week'], type(up['id']), up['id']
        if cost_table and rate2 != None:
            delta = 0
            cost = 0
            rent_cost= []
            print "HEEEERREEEEEE ИТератор вошел в таблицу"
            for c in cost_table:#этот цикл принципиально не заходит ни в if ни в for
                c['start_time'] = datetime.fromtimestamp(c['start_time'])
                c['end_time'] = datetime.fromtimestamp(c['end_time'])
                # print "c ReNTER", type(c['RENTER']), c['RENTER'], type(rate2), rate2
                if c['RENTER'] == renter_id:
                    rent_cost.append(c)
        print "rent.cost", rent_cost
            #     for r in rate2:
            #         print "in rate", type(c['RENTER']), c['RENTER'], type(r['renter_id']), r['renter_id']
            #         if c['RENTER'] == r['renter_id']:
            #             if c['hall_id'] == r['hall_id']:#тот ли зал
            #                 print "HEEREE совпал зал|",  c['hall_id'], "|", r['hall_id']
            #                 r['days_of_week'] = int(r['days_of_week'])
            #                 print "HEEEERREEEEEE день|", type(c['start_time'].weekday()), c['start_time'].weekday(), type(r['days_of_week']), r['days_of_week']
            #                 if c['start_time'].weekday() == r['days_of_week']:#тот ли день, если тот, то сначала преобразование в один тип исчисления с тарифами
            #                     print "HEEEERREEEEEE совпал день|"
            #                     c['start_time'] = time.mktime(c['start_time'].timetuple())
            #                     c['start_time'] = c['start_time'] % 86400
            #                     c['end_time'] = time.mktime(c['end_time'].timetuple())
            #                     c['end_time'] = c['end_time'] % 86400
            #                     if not c['start_time'] <= r['end_time'] or c['end_time'] >= r['start_time']:
            #                         print "HEEEERREEEEEE нет пересечения"
            #                         if c['start_time'] >= r['start_time'] and c['end_time'] <= r['end_time']:# если не соблюдается - сложить все часы этого тарифа и умножить на cost, если соблюдается - искать пересекающиеся и считать
            #                             print "HERE !!! |", a, "|искать часы"
            #                             delta = c['end_time'] - c['start_time']
            #                             print "HEEEERREEEEEE стоимость использованного времени тарифа|"
            #                         elif c['start_time'] > r['start_time'] and c['end_time'] <= r['end_time']:
            #                             delta = c['end_time'] - r['start_time']
            #                             print "HEEEERREEEEEE стоимость задействованного времени тарифа|"
            #                         elif c['start_time'] < r['start_time'] and c['end_time'] >= r['end_time']:
            #                             delta = r['end_time'] - c['start_time']
            #                             print "HEEEERREEEEEE стоимость задействованного времени тарифа|", cost
            #                         cost = r['cost'] / 3600
            #                         cost = delta * cost
            #                         ind_rate_sum = ind_rate_sum + cost#здесь скопится сумма по всем задействованным индивидуальным тарифам
            # print "сумма за время арендованное по индивидуальным тарифам", ind_rate_sum
        print "HEEEERRREEE ИТератор перед return|"
        return render.renter(renter, renter_man, groups, people, updated_rate, updeted_pays, uppd_ev_groups, form, form2, form3, form4)

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


        if form.d.name != None:
            print "HEEEEEEEEEEEEEEEEEERRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEE FORM1111111 !!!!!!!!!"
            people_id = getNextId('people')
            # print "HERE!!!", type(form.d.other), form.d.other
            print "HERE!!!", type(form.d.drop), form.d.drop
            group_id = getNextId('renters_group')
            print form, "here form1"
            form.d.drop = int(form.d.drop)
            renter_id = int(renter_id)
            if form.d.drop != "-1":

                element = {"id": group_id,
                           "people_id": form.d.drop,
                           "name": form.d.name,
                           "renter_id": renter_id}
                print "True ", type(group_id), group_id, type(people_id), people_id, type(form.d.name), form.d.name, type(renter_id), renter_id, type(form.d.drop), form.d.drop
                db.multiple_insert("renters_group", values=[element])
                db.insert("group_people", renter_id=renter_id, group_id=group_id, people_id=form.d.drop)
            elif form.d.drop == "-1":
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
        web.form.Checkbox('other', description='Новый руководитель'), web.form.Textbox('FIO', description='ФИО руководителя'),
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
