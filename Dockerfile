FROM python
RUN pip install python-telegram-bot
ADD /src/dumb_bot.py /
CMD ["python", "alfred_bot.py"]