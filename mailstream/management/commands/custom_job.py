from mailstream.models import Stream, Log
from django.core.management import BaseCommand
from mailstream.services import (NULLABLE,
                                 DAILY, WEEKLY, MONTHLY, REGULARITY_VALUES,
                                 CREATED, STARTED, ENDED, STATUS_VALUES,
                                 SUCCESS_ATTEMPT, ERROR_ATTEMPT, ATTEMPT_VALUES)
from django.conf import settings
from datetime import datetime, timezone, timedelta
from users.services import send_email_by_django

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('--- sending email ---')
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
        print('datatime', current_datetime)
        for stream in streams:
            print(f'Рассылка {stream.name}:')
            from_date = stream.started_at
            till_date = stream.ended_at
            print(f'from {from_date} till {till_date} time {stream.start_time} period {stream.regularity}')
            if stream.is_active:
                # check start and end time
                in_date = from_date <= current_date <= till_date
                in_time = from_time.time() <= stream.start_time <= till_time.time()
                if in_date:
                    print('in_date')
                    duration = abs(till_date - from_date).days
                    step = 1
                    if stream.regularity == DAILY:
                        step = 1
                    elif stream.regularity == WEEKLY:
                        step = 7
                    elif stream.regularity == MONTHLY:
                        step = 30
                    in_shedule = False
                    for day in range(0, duration, step):
                        range_date = datetime.combine(from_date, datetime.min.time()) + timedelta(days=day)
                        print(f'range date {range_date.date()}')
                        if range_date.date() == current_date:
                            print(f'in range {range_date}')
                            in_shedule = True
                            break
                    if in_shedule and in_time:
                        print(f'in_time time: {current_time}')
                        if bool(Log.objects.filter(stream=stream, attempt_date=current_date).count()):
                            print('stream', stream.name, ' - already executed')
                            continue
                    else:
                        # not a correct time to execute
                        print('stream', stream.name, ' - not correct time, skip')
                        continue
                else:
                    if current_date < stream.started_at:
                        # stream too early for execution
                        print('stream', stream.name, ' - too early')
                        continue
                    else:
                        # stream is ended
                        print('stream', stream.name, ' - not in date')
                        stream.status = ENDED
                        stream.is_active = False
                        stream.save()
                        print('stream', stream.name, ' - ended')
                        continue
            else:
                # set status ended
                stream.status = ENDED
                stream.save()
                print('stream', stream.name, ' - not active, ended')
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
            print(recipients)
            recipients = ['yuryev@ru',]
            response = send_email_by_django(stream.message.subject, stream.message.body, recipients)
            print('Итог: ',stream.name, stream.message.subject, stream.message.body, recipients, f' ответ: {response}')
            # response = f'text {stream.regularity}'
            for log in logs:
                log.response = response
                log.save()
