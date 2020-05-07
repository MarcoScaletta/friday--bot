FROM python
RUN pip install python-telegram-bot requests pymongo && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install git
ADD /src /
CMD ["python", "alfred_bot.py"]