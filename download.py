"""Download manual de dados abertos IPMA, sem ligação à infraestrutura IGNISPYRO."""
import argparse, hashlib, json, pathlib, urllib.request
SOURCES = {
    'stations': 'https://api.ipma.pt/open-data/observation/meteorology/stations/stations.json',
    'weather-types': 'https://api.ipma.pt/open-data/weather-type-classe.json',
}
LIMIT = 10_000_000
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise ValueError('Redirecionamento recusado')
def fetch(source, destination):
    url=SOURCES[source]
    request=urllib.request.Request(url,headers={'User-Agent':'IGNISPYRO-Public-Downloads/1.0'})
    with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
        payload=response.read(LIMIT+1)
    if len(payload)>LIMIT: raise ValueError('Resposta superior a 10 MB')
    json.loads(payload)
    destination=pathlib.Path(destination)
    with destination.open('xb') as handle: handle.write(payload)
    return {'source':url,'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',choices=SOURCES);parser.add_argument('output',type=pathlib.Path)
    args=parser.parse_args();print(json.dumps(fetch(args.source,args.output),indent=2))
