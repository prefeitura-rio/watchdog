FROM python:3.9

# Setup virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir poetry && \
    poetry install

# Run main.py
CMD ["poetry", "run", "python", "main.py"]
