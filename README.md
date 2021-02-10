# Harker Bell Schedule API
A modern, lightweight, lighting-speed bell schedule API built for developers building applications needing the bell schedule, in a nice neat format.

## Why?
We were making a project ourselves that needed the bell schedule in JSON format, so we thought, "why not make it for others to use"?

## API Refrence

**Base URL**: https://harker-schedule.herokuapp.com/v1

---------------

### `/all`
This endpoint returns the entire schedule for all five days of the week. \
Parameters:
* `block` (optional): Get timings for a time block in each day's schedule. Example: `p1` for period one.

---------------

### `/day/<day>`
This endpoint returns the schedule for a day. `<day>` can be monday-friday, or "today".\
Parameters: 
* `block` (optional): Get timings for a time block in the day's schedule. Example: `p1` for period one.

---------------

### `/day/<day>/time/<time>`
This endpoint returns the period for a given time and day. `<day>` can be monday-friday, or "today". For example, if you wanted to know what period is at 9:30 on Monday, you could make a request to `/day/monday/time/09:30`.

---------------

### `/current/block`
This endpoint provides the current period, start and end times for it, and how much time is left in the period.

---------------

## Warnings and info

If an endpoint returns `{"data": None}`, it means there are no results. This can happen when you try to get the schedule of Saturday, or getting the current period after school is over.