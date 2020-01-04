FROM python
RUN pip install python-telegram-bot
ADD /src /
CMD ["python", "alfred_bot.py"]