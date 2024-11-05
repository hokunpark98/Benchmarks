FROM php:5-apache
ADD index.php /var/www/html/index.php
RUN chmod a+rx /var/www/html/index.php

# Apache 포트를 12002로 변경하고 ServerName을 설정
RUN sed -i 's/Listen 80/Listen 12002/' /etc/apache2/ports.conf && \
    sed -i 's/:80/:12002/g' /etc/apache2/sites-available/000-default.conf && \
    echo "ServerName localhost" >> /etc/apache2/apache2.conf
