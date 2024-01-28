FROM python:3.11

WORKDIR /usr/src/app


# Install Cron
RUN apt-get update && apt-get -y install cron

# Copy the requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the specific files
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
COPY config.py ./
COPY generate_title.py ./
COPY find_documents_with_tag_id.py ./

RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/crontab

# Executing crontab command
CMD ["cron", "-f"]



