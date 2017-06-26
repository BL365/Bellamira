# coding: utf8

from Common import *

isAuthSuccess = False

class Home:

    form = web.form.Form(
        web.form.Textbox('log', description='Логин'), web.form.Password('pas', description='Пароль')
    )


    def GET(self):
        form = self.form
        return render.Home(form, isAuthSuccess)


    def POST(self):
        global isAuthSuccess
        print "post enter"
        form = self.form()
        if not form.validates() or not form.d.log:
            isAuthSuccess = False
            raise web.seeother('/home/', True)
        auth = db.query('Select * from auth where login ="' + form.d.log+'"')
        auth = list(auth)
        print len(auth), auth
        for a in auth:
            if form.d.pas == a['password']:
                print "AUTH!"
                isAuthSuccess = True

                raise web.seeother('/home/', True)
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
# #        все заливай и обновляем на сервере

