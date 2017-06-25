# coding: utf8

from Common import *


class Home:

    form = web.form.Form(
        web.form.Textbox('log', description='Логин'), web.form.Password('pas', description='Пароль')
    )


    def GET(self):
        form = self.form

        reg = 0



        return render.Home(form, reg)


    def POST(self):

        form = self.form()
        if not form.validates():
            raise web.seeother('/home/', True)
        people = db.query('Select * from people')
        for p in people:
            if form.d.log == p['login']:
                if form.d.pas == p['password']:
                    print "AUTH!"

                    raise web.seeother('/renters/', True)
#
#
#
        # $s = file_get_contents('http://ulogin.ru/token.php?token='. $_POST['token'].
        # '&host='. $_SERVER['HTTP_HOST']);
        # $user = json_decode($s, true);
# #
# #
# #         # // $user['network'] - google or google+
# #         # // $user['identity'] - id iser in google
# #         # // $user['first_name'] - name
# #         # // $user['last_name'] - family
# #
# #         s = ('http://ulogin.ru/token.php?token=', _POST['token'], '&host=', _SERVER['HTTP_HOST'])
# #
# #
# #
