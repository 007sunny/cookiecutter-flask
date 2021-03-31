# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template
from pythonjsonlogger import jsonlogger

from {{cookiecutter.app_name}} import commands, app1, logger
from {{cookiecutter.app_name}}.extensions import (
    bcrypt,
    cache,
    db,
    debug_toolbar,
    flask_static_digest,
    migrate,
)
from opentelemetry import trace
from opentelemetry.exporter.datadog import (
    DatadogExportSpanProcessor,
    DatadogSpanExporter,
)
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    DatadogExportSpanProcessor(
        DatadogSpanExporter(
            agent_url="http://127.0.0.1:8126/", service="dd_tracing_example"
        )
    )
)
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("span_1"):
    with tracer.start_as_current_span("span_2"):
        with tracer.start_as_current_span("span_3"):
            print("Hello world from {{cookiecutter.app_name}}!")


def create_app(config_object="{{cookiecutter.app_name}}.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(app1.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.FileHandler(filename='<LOG_FILE_PATH>')
    formatter = logger.formatter
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

