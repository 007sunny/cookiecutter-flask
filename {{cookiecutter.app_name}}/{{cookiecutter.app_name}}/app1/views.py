# -*- coding: utf-8 -*-
import logging

import requests

from flask import Blueprint, request, current_app
from opentelemetry import trace

blueprint = Blueprint('app1_blueprint', __name__)

@blueprint.route("/hello")
def hello():
    param = request.args.get("param")
    current_app.logger.info('testing #####################')
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("server-inner"):
        if param == "error":
            current_app.logger.info('encountered error')
            raise ValueError("forced server error")
        return "served: {}".format(param)

