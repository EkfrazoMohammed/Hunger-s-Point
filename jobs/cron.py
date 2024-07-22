from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
from HungerPointApp.views import *


def start():
    print("IN cron.py")
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(SendSavedEmail, 'cron',second=2)
    scheduler.add_job(OrderUpdate, 'cron',second=2)
    scheduler.start()
