# import jsonrpclib
from model_mommy import mommy
import pytest
from campaigns.models import Transaction
from yldt_bitcoin import bitcoin
from collections import namedtuple

settings_obj = namedtuple('settings', 'BTC_HOST BTC_PORT BTC_USER BTC_PASS')
conf = settings_obj(
    BTC_HOST='localhost',
    BTC_PORT=18332,
    BTC_USER='bitcoinrpc',
    BTC_PASS='B726rKcomZz7rWVckYX2GsJfhRh7H6AfkDNrPHTByHRw'
)

@pytest.mark.skipif(True, reason='Disabled')
def test_create_bitcoin_address():
    """
    TODO: Bla
    """
    s = jsonrpclib.Server(bitcoin.get_rpc_address(conf))
    before = len(s.listreceivedbyaddress(0, True))
    result = bitcoin.create_bitcoin_address()
    print('New address: {}'.format(result))
    after = len(s.listreceivedbyaddress(0, True))
    assert after > before

def test_get_rpc_address():
    result = bitcoin.get_rpc_address(conf)
    assert result == 'http://bitcoinrpc:B726rKcomZz7rWVckYX2GsJfhRh7H6AfkDNrPHTByHRw@localhost:18332/'

def test_transaction_api():
    """
    TODO
    """
    addr = bitcoin.create_bitcoin_address()
    t = mommy.make(Transaction, state=Transaction.STATE_PLEDGED, btc_address=addr,
        amount=0.001)
    data = self.get_json_by_name('transaction_api', args=(t.id,))
    print(data)
    self.assertEqual(Transaction.STATE_PLEDGED, data['state'])
