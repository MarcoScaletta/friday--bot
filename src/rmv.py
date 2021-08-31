import asyncio
import aiohttp
from RMVtransport import RMVtransport
import datetime

a = None
rmv = RMVtransport()
async def main():
    async with aiohttp.ClientSession():
        rmv = RMVtransport()
        data = await get_departures(station_id="3004736")
        print(data)

async def get_departures(station_id):
    res = ""
    data = (await rmv.get_departures(station_id)).journeys
    directions = dict()
    for d in data:
        if d.product in ['Tram', 'Bus']:
            direction = d.direction

            if d.departure == d._now:
                dep = "now"
            else:
                dep = d.departure - d._now if d.departure > d._now else d._now - d.departure
                dep = str(dep)[:-3]
                if d.departure < d._now:
                    dep = dep + " ago"
            if not direction in directions:
                directions[direction] = dict()
            if not d.number in directions[d.direction]:
                directions[d.direction][d.number] = list()
            directions[d.direction][d.number] += [dep]
    for direction in directions:
        res += direction
        for number in directions[direction]:
            res+="\n"+number 
            for dep in directions[direction][number]:
                res += " [" + dep + "]"
        res += "\n\n"
    return res


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
