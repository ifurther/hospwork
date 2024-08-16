import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# support tls1.2
class TLSAdapter(HTTPAdapter):
  def init_poolmanager(self, *args, **kwargs):
    context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    kwargs['ssl_context'] = context
    return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

  def build_response(self, req, resp):
    return super(TLSAdapter, self).build_response(req, resp)
