from datetime import datetime, timezone
from enum import Enum
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

class EventType(str, Enum):
    cycle="cycle"; downtime="downtime"; quality="quality"
class Event(BaseModel):
    machine_id:str=Field(min_length=1)
    operator_id:str=Field(min_length=1)
    event_type:EventType
    value:float|None=None
    reason:str|None=None
    occurred_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))

app=FastAPI(title="Factory Floor Telemetry Engine")
events:list[Event]=[]
clients:set[WebSocket]=set()

@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/events')
def recent(limit:int=100): return events[-limit:]
@app.post('/events',status_code=201)
async def create(event:Event):
    events.append(event)
    payload={'type':'shop_floor_event','event':event.model_dump(mode='json')}
    dead=[]
    for ws in clients:
        try: await ws.send_json(payload)
        except Exception: dead.append(ws)
    for ws in dead: clients.discard(ws)
    return event
@app.websocket('/ws/supervisor')
async def supervisor(ws:WebSocket):
    await ws.accept(); clients.add(ws)
    try:
        while True: await ws.receive_text()
    except WebSocketDisconnect: clients.discard(ws)
