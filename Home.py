# coding: utf8

from Common import *


class Home:

    form = web.form.Form(
        web.form.Textbox('log', description='Логин'), web.form.Textbox('pas', description='Пароль')
    )


    def GET(self, auth):
        form = self.form



        render.Home(form)


    def POST(self, log, pas):

        form = self.form()
        if not form.validates():
            raise web.seeother('/home/', True)

        print "token"


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
