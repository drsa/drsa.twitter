import argh
from . import search as tsearch
from . import stream as tstream

@argh.arg('output', help="Output file (JSONLines)")
@argh.arg('query', 
    nargs="+",
    help="Twitter query as defined at"
         " https://dev.twitter.com/rest/public/search")
def search(output, query):
    q = ' '.join(query)
    tsearch.search(q, output)

@argh.arg('output', help="Output file (JSONLines)")
@argh.arg('keywords', nargs="+", help="keywords to listen for")
def stream(output, keywords):
    kw = [i.strip() for i in ' '.join(keywords).split(',')]
    tstream.listen(kw, output)

parser = argh.ArghParser()
parser.add_commands([
    search,
    stream
])

def main():
    parser.dispatch()
