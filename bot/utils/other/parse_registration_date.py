async def parse_registration_date(date_info):
    registration_date_date = str(date_info).split()[0]
    registration_date_time = str(date_info).split()[1]
    year = registration_date_date.split('-')[0]
    month_number = registration_date_date.split('-')[1]
    month = ''
    if month_number == '01':
        month = 'января'
    elif month_number == '02':
        month = 'февраля'
    elif month_number == '03':
        month = 'марта'
    elif month_number == '04':
        month = 'апреля'
    elif month_number == '05':
        month = 'мая'
    elif month_number == '06':
        month = 'июня'
    elif month_number == '07':
        month = 'июля'
    elif month_number == '08':
        month = 'августа'
    elif month_number == '09':
        month = 'сентября'
    elif month_number == '10':
        month = 'октября'
    elif month_number == '11':
        month = 'ноября'
    elif month_number == '12':
        month = 'декабря'

    day = registration_date_date.split('-')[2] if not (registration_date_date.split('-')[2]).startswith('0') else (registration_date_date.split('-')[2])[1:]

    hour = registration_date_time.split(':')[0]
    minute = registration_date_time.split(':')[1]

    parse_date_info = {
        'day': day,
        'month': month,
        'year': year,
        'hour': hour,
        'minute': minute,
    }

    return parse_date_info