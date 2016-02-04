import os
import flask
import string
import urllib
import bs4
import re
import simplejson as json
from collections import Counter


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

  a = bs4.BeautifulSoup( urllib.urlopen( url ), "lxml-xml" )

  base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=XML'

  url = base +'&id=' + string.join( [ v.get_text() for v in a.findAll('Id') ], ',')+'&retmax=' +str(num)

  a = bs4.BeautifulSoup( urllib.urlopen( url ),"lxml-xml" )

  s=''
  for v in a.findAll('AbstractText'): s+= v.get_text()

  data=[]
  for v in parse(s):
    data.append( {'key':v[0], 'value':v[1]} )

  return flask.render_template('word_cloud.html', data = json.dumps(data) )



def parse( s ):
  #s=open('./source').readlines()[0]
  stp_wrds = { w.strip('\n') for w in open('./static/stop_words.txt').readlines()}

  word_list = Counter(string.split(re.sub('[^A-Za-z0-9\-]+', ' ', s) ))
  for w in word_list.keys():
    if string.lower(w) in stp_wrds: del word_list[w]
    elif unicode.isdigit(w): del word_list[w]
    elif unicode.isdigit(w[0]): del word_list[w]
    elif w[0] == '-': del word_list[w]		

  return word_list.most_common(1000)

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
