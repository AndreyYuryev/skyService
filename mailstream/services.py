NULLABLE = {'blank': True, 'null': True}

DAILY = 'D'
WEEKLY = 'W'
MONTHLY = 'M'
REGULARITY_VALUES = [(DAILY, 'раз в день'), (WEEKLY, 'раз в неделю'), (MONTHLY, 'раз в месяц'), ]

CREATED = 'CR'
STARTED = 'ST'
ENDED = 'ED'
STATUS_VALUES = [(ENDED, 'завершена'), (CREATED, 'создана'), (STARTED, 'запущена'), ]

SUCCESS_ATTEMPT = 'S'
ERROR_ATTEMPT = 'E'
ATTEMPT_VALUES = [(SUCCESS_ATTEMPT, 'успешно'), (ERROR_ATTEMPT, 'с ошибкой'), ]
