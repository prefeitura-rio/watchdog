# Build arguments
ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}

# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# ensures that the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output of your application (e.g. django logs)
# in real time. Equivalent to python -u: https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1

# Install dependencies
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir poetry && \
    poetry install

# Run main.py
STOPSIGNAL SIGKILL
CMD ["poetry", "run", "python", "main.py"]
