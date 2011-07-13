from riak.transports import RiakHttpTransport
from xml.etree import ElementTree

class RiakSearch:
    def __init__(self, client, transport_class=None,
                 host="127.0.0.1", port=8098):
        if not transport_class:
            self._transport = RiakHttpTransport(host,
                                                port,
                                                "/solr")
        else:
            self._transport = transport_class(host, port, client_id=client_id)

        self._client = client
        self._decoders = {"text/xml": ElementTree.fromstring}
 
    def get_decoder(self, content_type):
        decoder = self._client.get_decoder(content_type) or self._decoders[content_type]
        if not decoder:
            decoder = self.decode

        return decoder

    def decode(self, data):
        return data

    def add(self, doc):
        pass

    def delete(self, doc):
        pass

    def search(self, index, query, **params):
        options = {'q': query, 'wt': 'json'}
        options.update(params)
        headers, results = self._transport.search(index, options)
        decoder = self.get_decoder(headers['content-type'])
        return decoder(results)
