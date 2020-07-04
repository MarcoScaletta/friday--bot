FROM python
RUN pip install python-telegram-bot requests pymongo
ADD /src /
CMD ["python", "alfred_bot.py"]
