FROM python

WORKDIR /app

# Copy and install dependencies
ADD . .
RUN make install 

# Setup crontab
RUN apt-get update
RUN apt-get -y install -qq --force-yes cron
ADD crontab /etc/cron.d/crawler
RUN chmod 0644 /etc/cron.d/crawler
RUN touch /var/log/cron.log

# Print log
CMD service cron start && tail -f /var/log/cron.log