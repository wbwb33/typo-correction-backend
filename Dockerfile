# Here is the build image, probably ~500MB, this image will NOT go to deployment
# START of builder
# to target this stage $ docker build --target builder -t builder .
FROM python:3.8-slim as builder

# copy required library list to install folder, auto create install folder if not exist
COPY requirements.txt /install/requirements.txt

# set workdir and install dependency
WORKDIR /install
RUN pip install --no-cache-dir --user -r requirements.txt
# END of builder


# Here is the production image, probably ~50MB, this image WILL go to deployment
# START of app
# to target this stage $ docker build --target app -t wbwb33/voicebot-rasa-logger .
FROM python:3.8-slim as app

# copy installed library from builder image
COPY --from=builder /root/.local /root/.local

# copy all project files into app, auto create app folder if not exist
COPY . /app

# set workdir to app
WORKDIR app

# set env for python lib
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

# execute main py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
# END of app(base)
