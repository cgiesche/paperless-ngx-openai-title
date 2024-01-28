FROM python:3.11

WORKDIR /usr/src/app

# Install Cron
RUN apt-get update && apt-get -y install cron

# Copy the requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the specific files
COPY docker_cron /etc/cron.d/docker_cron
COPY config.py ./
COPY generate_title.py ./
COPY find_documents_with_tag_id.py ./

COPY run.sh ./

RUN chmod +x run.sh

RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/docker_cron

CMD cron -f

# Check if config.py exists
RUN if [ ! -f config.py ]; then echo "config.py not found" && exit 1; fi

CMD [ "./run.sh" ]
