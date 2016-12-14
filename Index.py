from Common import *


class Index:
    form = web.form.Form(
        web.form.Textbox('number', web.form.notnull, description="")
    )

    def GET(self):
        return render.index()

    def POST(self):
        raise web.seeother('/', True)
