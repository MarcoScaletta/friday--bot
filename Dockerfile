FROM python
RUN pip install python-telegram-bot requests
ADD /src /
CMD ["python", "alfred_bot.py"]