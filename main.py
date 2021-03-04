import flask
from datetimerange import DateTimeRange
from datetime import date, datetime
from time import localtime, strftime
import calendar
from json import loads
from os import getenv
from requests import get
from flask_cors import CORS

app = flask.Flask(__name__, template_folder='.')
CORS(app)

def get_schedule(day=None):
    schedule = loads(
        open(
            'schedule.json',
            'r'
        ).read()
    )
    if day:
        try:
            return(schedule[day])
        except KeyError:
            return(None)
    else:
        return(schedule)

def check_range(block, day, to_verify):
    today = str(date.today())
    schedule = get_schedule(day)
    if schedule != None:
        block_timings = schedule[block]
    else:
        return(None, None)
    if block != 'passing_period':
        start = block_timings['start']
        end = block_timings['end']
        time_range = DateTimeRange(f'{today}T{start}:00+0800', f'{today}T{end}:00+0800')
        return(f'{today}T{to_verify}:00+0800' in time_range, None)
    else:
        for passing_per in block_timings:
            start = passing_per['start']
            end = passing_per['end']
            time_range = DateTimeRange(f'{today}T{start}:00+0800', f'{today}T{end}:00+0800')
            if f'{today}T{to_verify}:00+0800' in time_range:
                return(True, block_timings.index(passing_per))
        return(None, None)

def find_delta(start, end):
    format = '%H:%M'
    delta = str(
        datetime.strptime(end, format) - datetime.strptime(start, format)
    )
    if len(delta[delta.index(':')]) == 1:
        delta = '0' + delta
    return(delta)

@app.route('/<version>/all')
def all(version):
    '''
    This endpoint returns the schedule for Monday - Friday.
    Optional parameters: 
        - 'block': Get timings for a time block in each day's schedule.
    '''
    data = loads(
        open(
            'schedule.json', 'r'
        ).read()
    )
    res = {}
    param = flask.request.args.get('block')
    if param != None:
        for day in data:
            res[day] = data[day][param]
    else:
        res = {
            'data': data
        }
    return(res)
        

@app.route('/<version>/day/<day>')
def day(day, version):
    '''
    This endpoint returns the schedule for a day.
    Optional parameters: 
        - 'block': Get timings for a time block in the day's schedule.
    '''
    if day.lower() == 'today':
        day = calendar.day_name[date.today().weekday()].lower()
    try:
        data = loads(
            open(
                'schedule.json', 'r'
            ).read()
        )[day]
    except KeyError:
        return({
            'data': None
        })

    block = flask.request.args.get('block')

    if block != None:
        try:
            res = {
                'data': {
                    block: data[block]
                }
            }
        except KeyError:
            res = {
                'data': None
            }
    else:
        res = {
            'data': data
        }

    return(res)

@app.route('/<version>/day/<day>/time/<time>')
def time(day, time, version):
    '''
    This endpoint returns the period for a given time and day.
    '''
    if day == 'today':
        day = calendar.day_name[date.today().weekday()].lower()

    schedule = get_schedule(day=day)
    if schedule == (None):
        return({
            'data': None
        })
    for block in schedule:
        if block != 'passing_period':
            if check_range(block, day, time)[0]:
                return({
                    'data': {
                        block: schedule[block]
                    }
                })
        else:
            xcheck_range = check_range(block, day, time)
            if xcheck_range[0]:
                return({
                    'data': {
                        block: schedule[block][xcheck_range[1]]
                    }
                })
    return({
        'data': None
    })

@app.route('/v1/current/block')
def current_block():
    '''
    This endpoint provides data for the current block.
    '''
    day = calendar.day_name[date.today().weekday()].lower()
    schedule = get_schedule(
        day=day
    )
    if schedule == (None):
        return({
            'data': None
        })
    for block in schedule:
        print(strftime('%H:%M', localtime()))
        _range = check_range(
                block, 
                day, 
                strftime('%H:%M', localtime())
        )
        if _range[0]:
            if block != 'passing_period':
                return({
                    'data': {
                        block: schedule[block],
                        'time_left': find_delta(
                            strftime(
                                '%H:%M', 
                                localtime()
                            ), schedule[block]['end']
                        )[:-3]
                    }
                })
            else:
                return({
                    'data': {
                        'passing_period': schedule['passing_period'][_range[1]],
                        'time_left': find_delta(
                            strftime(
                                '%H:%M', 
                                localtime()
                            ), schedule['passing_period'][_range[1]]['end']
                        )[:-3]
                    }
                })

    return({
        'data': None
    })

@app.route('/v2/current/block')
def current_block_2():
    '''
    This endpoint provides data for the current block.
    '''
    day = calendar.day_name[date.today().weekday()].lower()
    schedule = get_schedule(
        day=day
    )
    if schedule == (None):
        return({
            'data': None
        })
    for block in schedule:
        print(strftime('%H:%M', localtime()))
        _range = check_range(
                block, 
                day, 
                strftime('%H:%M', localtime())
        )
        if _range[0]:
            if block != 'passing_period':
                return({
                    'data': {
                        'block': block,
                        'block_timings': schedule[block],
                        'time_left': find_delta(
                            strftime(
                                '%H:%M', 
                                localtime()
                            ), schedule[block]['end']
                        )[:-3]
                    }
                })
            else:
                return({
                    'data': {
                        'block': 'passing_period',
                        'block_timings': schedule['passing_period'][_range[1]],
                        'time_left': find_delta(
                            strftime(
                                '%H:%M', 
                                localtime()
                            ), schedule['passing_period'][_range[1]]['end']
                        )[:-3]
                    }
                })

    return({
        'data': None
    })

@app.route('/')
def main():
    res = current_block()['data']
    
    if res != None:
        time_left = res['time_left']
        del res['time_left']
        current_per = list(res.keys())[0]
        if current_per[0] == 'p':
            current_per = current_per[-1:]
            period = 'period'
        else:
            period = ''
        print(time_left)
        hours = time_left[:time_left.index(':')]
        minutes = time_left.replace(':', '').replace(hours, '')
        if hours[0] == '0':
            hours = hours[-1:]
        if hours == '0':
            hours = ''
        else:
            hours = hours + ' hours and '
        print(hours)

        return '{}{} minutes left in {} {}'.format(hours, minutes, period, current_per)
    else:
        return('School\'s out!')