from flask import Flask, request

from service import GatewayService

app = Flask(__name__)
gateway = GatewayService()


@app.route('/')
def index():
    return 'API Gateway'


@app.post('/api/fetch_from_doi')
def fetch_from_doi():
    data = request.json

    doi_list = data.get('doi', type=list[str])
    skip_flags = data.get('skip_flags', type=list[str], default=[])

    for doi in doi_list:
        gateway.send_to_kafka('fetch_doi', {
            'doi': doi,
            'skip_flags': skip_flags
        })

    return 'DOIs sent to Kafka for processing'


if __name__ == "__main__":
    app.run()