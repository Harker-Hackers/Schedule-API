import flask
from json import loads

app = flask.Flask(__name__)

@app.route('/all')
def all():
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
        

@app.route('/day/<day>')
def day(day):
    '''
    This endpoint returns the schedule for a day.
    Optional parameters: 
        - 'block': Get timings for a time block in the day's schedule.
    '''
    data = loads(
        open(
            'schedule.json', 'r'
        ).read()
    )[day]

    param = flask.request.args.get('block')

    if param != None:
        try:
            res = {
                'data': data[param]
            }
        except KeyError:
            res = {
                'message': 'Time block not found.'
            }
    else:
        res = {
            'data': data
        }

    return(res)
app.run(debug=True)