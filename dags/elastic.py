import datetime
import os

from elasticsearch import Elasticsearch, helpers
#Be careful to put Elastic URL and not Kibana Url! On the cloud version, you should see "es" and not "kb"
password = os.environ["ENV_PASSWORD"]
client = Elasticsearch(hosts=["https://baseball.es.us-central1.gcp.cloud.es.io:9243"], basic_auth=('elastic', password))
docs = []
docs.append({"name": "Bob", "timestamp": datetime.utcnow().isoformat()})

helpers.bulk(client, docs, index = "index_for_python_test")

