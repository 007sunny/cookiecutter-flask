# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-PYTHON_VERSION_NOT_SET}

FROM python:${INSTALL_PYTHON_VERSION}-slim-buster AS builder

WORKDIR /app

COPY ["Pipfile", "auto_pipenv.sh", "./"]
RUN pip install --no-cache pipenv
RUN pipenv install --pre

COPY {{cookiecutter.app_name}} {{cookiecutter.app_name}}
COPY .env.example .env

# ================================= PRODUCTION =================================
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster as production

WORKDIR /app

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid
ENV PATH="/home/sid/.local/bin:${PATH}"

COPY --from=builder --chown=sid:sid /app/{{ cookiecutter.app_name }}/static /app/{{ cookiecutter.app_name }}/static

COPY ["Pipfile", "auto_pipenv.sh", "./"]
RUN pip install --no-cache pipenv
RUN pipenv install --pre

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisord_programs /etc/supervisor/conf.d

COPY . .

EXPOSE 5000
ENTRYPOINT ["/bin/bash", "supervisord_entrypoint.sh"]
CMD ["-c", "/etc/supervisor/supervisord.conf"]


# ================================= DEVELOPMENT ================================
FROM builder AS development

RUN pipenv install --dev --pre
EXPOSE 2992
EXPOSE 5000
CMD ["pipenv", "run", "ddtrace-run", "flask", "run"]
