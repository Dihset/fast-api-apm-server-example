import datetime
import os
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client


apm = make_apm_client(
    {
        "SERVICE_NAME": "fastapi-app", 
        "SERVER_URL": "http://apm-server:8200",
    }
)
es = AsyncElasticsearch(os.environ["ELASTICSEARCH_HOSTS"])
app = FastAPI()
app.add_middleware(ElasticAPM, client=apm)


@app.on_event("shutdown")
async def app_shutdown():
    await es.close()


@app.get("/")
async def index():
    return await es.cluster.health()
