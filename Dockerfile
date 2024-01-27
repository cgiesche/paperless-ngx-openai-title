FROM python:3.11

WORKDIR /usr/src/app

# Copy the requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the specific files
COPY config.py ./
COPY generate_title.py ./
COPY run.py ./

# Check if config.py exists
RUN if [ ! -f config.py ]; then echo "config.py not found" && exit 1; fi

CMD [ "python", "./run.py" ]
