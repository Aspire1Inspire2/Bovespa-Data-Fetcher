from urllib import urlopen
import re
from django.utils import simplejson
from models import Company


ERRORS= {   "FSW-0001":"Este per�odo n�o � v�lido.",
            "FSW-0002":"Este per�odo n�o � v�lido; insira uma data inicial menor que a data final.",
            "FSW-0003":"A data inicial n�o � v�lida; insira uma data menor que a data de hoje.",
            "FSW-0004":"A data final n�o � v�lida; insira uma data menor ou igual a data atual.",
            "FSW-0101":"Par�metro size menor que 1","FSW-0102":"Par�metro page menor que 1",
            "FSW-0103":"Par�metro fields inv�lido","FSW-0104":"Par�metro idt menor que 1",
            "FSW-0201":"Par�metro inv�lido",
            "FSW-0202":"Campo IDT inv�lido",
            "FSW-0401":"N�o h� informa��o dispon�vel para esta a��o/�ndice.",
            "FSW-0402":"Campo target inv�lido",
            "FSW-0404":"URL n�o encontrada",
            "FSW-0500":"Internal Server Error",
            "FSW-0400":"Bad Request"
        }

WS_URL = 'http://cotacoes.economia.uol.com.br/ws/asset/%s/intraday?size=500&page=1'


def geturl(url):
    print 'looking url ' + (url)
    content = urlopen(url).read()
    print 'load successful'
    return content

def main():
    companies = db.GqlQuery("SELECT * FROM WatchedQuote ORDER BY code")
    for company in companies:
       idt = company.idt
       data = geturl(WS_URL % idt)
       idtjson = simplejson.loads(data)
       for quote in idtjson['data']:
           q = Quote()
           q.company = company
           for att in quote:
               q.__setattr__(att, quote[att])
           q.put()
        
if (__name__=='__main__'):
    main()

