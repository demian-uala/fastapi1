FROM python:3.12
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 APP_HOME=/microservice/ HOST=0.0.0.0 PORT=5000
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
COPY  requirements.txt /tmp/
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
ADD . $APP_HOME
EXPOSE $PORT

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser $APP_HOME
USER appuser

#CMD uvicorn main:app --host $HOST --port $PORT
