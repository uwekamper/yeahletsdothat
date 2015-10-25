Yeah Let's Do That
==================

"Yeah Let's Do That" (YLDT) is a self-hosted crowd-funding tool.

**DO NOT USE THIS!** This is early alpha stage. Really, I mean it.
You could loose all your money!

http://github.com/uwekamper/yeahletsdothat/

Payment Plugins
---------------

YLDT supports a number of different payment methods.

Currently supported methods:
* Braintree payments (credit cards, Paypal, Bitcoin)
* Cash payments (for face-to-face meetings with manual processing)

Planned:
* Bitcoin
* DogeCoin

Configuration of the Bitcoin daemon (bitcoin.conf)
--------------------------------------------------

The Bitcoin payment plugin is defunct at the moment. This is just for reference.

Your bitcoind/bitcoin-qt configuration file should look like this.

    testnet=1
    server=1
    rpcuser=bitcoinrpc
    rpcpassword=*yourpassword*

How Payments Are Processed
--------------------------

The following state graph shows the states which a transaction can go through.


                +----------------------------------------------+
                |                                              |
            +---+---+                    +----------+          |
    +------+|pledged|+-----------------> |unverified|+----+    |
    |       +-------+                    +----+-----+     |    |
    |                                         |           |    |
    |    payment was rejected                 |           |    |
    |         +-----+                         |           |    |
    |         |     | try again!              |           |    |
    |         |     v                         v           |    |
    |       +-+--------+                 +--------+       |    |
    |       | payment  | <--------------+|verified|       |    |
    |       |processing|                 +------+-+       |    |
    |       +--+----+--+                        |         |    |
    |          |    |    give up trying         |         |    |
    |   success|    +--------------+            v         |    |
    |          |                   |     +-------+        |    |
    |          v                   +---> |aborted| <------+    |
    |       +---------+                  +-------+             |
    +-----> |completed|                      ^                 |
            +---------+                      |                 |
                                             +-----------------+

When a new transaction is created, it is immediately in the "pledged" state.
In every step the transaction can go into the "aborted" state – either trough
user interaction or a failing payment.



