import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from mailstream.models import Stream, Log
from django.core.management import BaseCommand
from mailstream.services import (NULLABLE,
                                 DAILY, WEEKLY, MONTHLY, REGULARITY_VALUES,
                                 CREATED, STARTED, ENDED, STATUS_VALUES,
                                 SUCCESS_ATTEMPT, ERROR_ATTEMPT, ATTEMPT_VALUES)
from datetime import datetime, timezone, timedelta
from users.services import send_email_by_django

logger = logging.getLogger(__name__)


def mailstrem_job():
    # Your job processing logic here...
    # print('--- sending email ---')
    # текущее время
    current_datetime = datetime.now(tz=timezone.utc)
    # текущая дата и время
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    # разброс по времени
    from_time = current_datetime - timedelta(minutes=5)
    till_time = current_datetime + timedelta(minutes=5)

    # get all streams
    streams = Stream.objects.all()
    # print('datatime', current_datetime)
    for stream in streams:
        # print(f'Рассылка {stream.name}:')
        start_date = stream.started_at
        end_date = stream.ended_at
        # print(f'from {from_date} till {till_date} time {stream.start_time} period {stream.regularity}')
        if stream.is_active:
            # check start and end time
            in_date = start_date <= current_date <= end_date
            in_time = from_time.time() <= stream.start_time <= till_time.time()
            if in_date:
                # print('in_date')
                duration = abs(end_date - start_date).days
                step = 1
                if stream.regularity == DAILY:
                    step = 1
                elif stream.regularity == WEEKLY:
                    step = 7
                elif stream.regularity == MONTHLY:
                    step = 30
                in_shedule = False
                for day in range(0, duration, step):
                    range_date = datetime.combine(start_date, datetime.min.time()) + timedelta(days=day)
                    print(f'range date {range_date.date()}')
                    if range_date.date() == current_date:
                        print(f'in range {range_date}')
                        in_shedule = True
                        break
                if in_shedule and in_time:
                    # print(f'in_time time: {current_time}')
                    if bool(Log.objects.filter(stream=stream, attempt_date=current_date).count()):
                        # print('stream', stream.name, ' - already executed')
                        continue
                else:
                    # not a correct time to execute
                    # print('stream', stream.name, ' - not correct time, skip')
                    continue
            else:
                if current_date < stream.started_at:
                    # stream too early for execution
                    # print('stream', stream.name, ' - too early')
                    continue
                else:
                    # stream is ended
                    # print('stream', stream.name, ' - not in date')
                    stream.status = ENDED
                    stream.is_active = False
                    stream.save()
                    # print('stream', stream.name, ' - ended')
                    continue
        else:
            # set status ended
            stream.status = ENDED
            stream.save()
            # print('stream', stream.name, ' - not active, ended')
            continue
        # выполнение рассылки
        recipients = []
        logs = []
        for client in stream.client.all():
            recipients.append(client.email)
            attempt_status = SUCCESS_ATTEMPT
            log = Log.objects.create(stream=stream, client=client, attempt_status=attempt_status,
                                     attempt_date=current_date, attempt_time=current_time)
            log.save()
            logs.append(log)
        stream.status = STARTED
        stream.save()
        # send_email
        # print(recipients)
        response = send_email_by_django(stream.message.subject, stream.message.body, recipients)
        # print('Итог: ',stream.name, stream.message.subject, stream.message.body, recipients, f' ответ: {response}')
        # response = f'text {stream.regularity}'
        for log in logs:
            log.response = response
            log.save()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        # scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            mailstrem_job,
            trigger=CronTrigger(minute="*/1"),  # Every 10 seconds
            id="mailstrem_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'mailstrem_job'.")

        # scheduler.add_job(
        #     delete_old_job_executions,
        #     trigger=CronTrigger(
        #         day_of_week="mon", hour="00", minute="00"
        #     ),  # Midnight on Monday, before start of the next work week.
        #     id="delete_old_job_executions",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info(
        #     "Added weekly job: 'delete_old_job_executions'."
        # )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
