# -*- coding: utf-8 -*-
"""

    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""

from flask import request
from flask_restful import Resource

from walle.common.controller import Controller
from walle.form.server import ServerForm
from walle.model.deploy import ServerModel


class ServerAPI(Resource):
    def get(self, id=None):
        """
        fetch environment list or one item
        /environment/<int:env_id>

        :return:
        """
        return self.item(id) if id else self.list()

    def list(self):
        """
        fetch environment list

        :return:
        """
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        server_model = ServerModel()
        server_list, count = server_model.list(page=page, size=size, kw=kw)
        return Controller.list_json(list=server_list, count=count)

    def item(self, id):
        """
        获取某个用户组

        :param id:
        :return:
        """

        server_model = ServerModel(id=id)
        server_info = server_model.item()
        if not server_info:
            return Controller.render_json(code=-1)
        return Controller.render_json(data=server_info)

    def post(self):
        """
        create a environment
        /environment/

        :return:
        """

        form = ServerForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            server_new = ServerModel()
            id = server_new.add(name=form.name.data, host=form.host.data)
            if not id:
                return Controller.render_json(code=-1)

            return Controller.render_json(data=server_new.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def put(self, id):
        """
        update environment
        /environment/<int:id>

        :return:
        """

        form = ServerForm(request.form, csrf_enabled=False)
        form.set_id(id)
        if form.validate_on_submit():
            server = ServerModel(id=id)
            ret = server.update(name=form.name.data, host=form.host.data)
            return Controller.render_json(data=server.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def delete(self, id):
        """
        remove an environment
        /environment/<int:id>

        :return:
        """
        server_model = ServerModel(id=id)
        server_model.remove(id)

        return Controller.render_json(message='')
