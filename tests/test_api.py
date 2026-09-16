from fastapi.testclient import TestClient
from factory_engine.app import app, events
c=TestClient(app)
def test_capture():
    events.clear(); r=c.post('/events',json={'machine_id':'CNC-07','operator_id':'OP-12','event_type':'downtime','reason':'tool change'})
    assert r.status_code==201 and c.get('/events').json()[0]['machine_id']=='CNC-07'
def test_validation():
    assert c.post('/events',json={'machine_id':'','operator_id':'x','event_type':'cycle'}).status_code==422
