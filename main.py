from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uuid, time, logging, os

app = FastAPI(title='AI Sonny Core', version='0.1')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ai_sonny')

class IngestPayload(BaseModel):
    source: str
    title: str | None = None
    url: str | None = None
    timestamp: str | None = None
    platform: str | None = None
    metadata: dict | None = {}

IN_MEMORY_QUEUE = []

def scout_and_verify(item):
    logger.info('Scout: analyzing item id=%s', item['id'])
    # Simulated scoring & verification
    time.sleep(1)
    item['virality_score'] = 85 if 'viral' in (item.get('title') or '').lower() else 30
    logger.info('Verifier: checks for id=%s', item['id'])
    time.sleep(1)
    item['verified'] = True
    item['package_id'] = 'pkg_' + uuid.uuid4().hex[:8]
    logger.info('Package created: %s for id=%s', item['package_id'], item['id'])

@app.post('/ingest')
async def ingest(payload: IngestPayload, background: BackgroundTasks):
    item = payload.dict()
    item['id'] = 'media_' + uuid.uuid4().hex[:8]
    item['received_at'] = time.time()
    IN_MEMORY_QUEUE.append(item)
    logger.info('Ingest received: %s', item['id'])
    background.add_task(scout_and_verify, item)
    return {'id': item['id'], 'status': 'accepted'}

@app.get('/health')
async def health():
    return {'status':'ok','queue_len': len(IN_MEMORY_QUEUE)}

@app.get('/packages')
def list_packages():
    # Return lightweight package summaries
    return [{'package_id': p.get('package_id'), 'title': p.get('title'), 'virality_score': p.get('virality_score'), 'verified': p.get('verified')} for p in IN_MEMORY_QUEUE if p.get('package_id')]
