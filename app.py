import flask
import string
import urllib
import bs4

app = flask.Flask(__name__)


@app.route('/index', methods=['GET'] )
def index():
  return flask.render_template('index.html')


@app.route('/cloud', methods=['POST'] )
def cloud():
  base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed'

  terms = flask.request.form['search_term']
  search_string = '+'.join(terms.split())
  num = flask.request.form['num_papers']

  url = base + '&retmax=' +str(num) + '&term='+search_string

  a = bs4.BeautifulSoup( urllib.urlopen( url ),features="xml" )

  base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=XML'
  base='http://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi.'

  url = base +'&id=' + string.join( [ v.get_text() for v in a.findAll('Id') ], ',')
  a = bs4.BeautifulSoup( urllib.urlopen( url ),features="xml" )


  print url

  return a.get_text()






if __name__ == '__main__':
  app.run( debug = True )