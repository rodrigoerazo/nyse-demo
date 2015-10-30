from memsql.common import database, connection_pool
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ticker', help='specify the database containing ask_quotes and bid_quotes tables', default='BLAH')
args = parser.parse_args()
ticker = args.ticker

pool = connection_pool.ConnectionPool()
t = {"ticker":ticker}

best_asks = "SELECT ticker, ask_price, ask_size, exchange, timestamp FROM ask_view WHERE ticker='%(ticker)s' ORDER BY ask_price ASC, ask_size DESC LIMIT 10;" % t
best_asks_per_exchange = "SELECT ticker, ask_price, max(ask_size) AS ask_size, exchange, timestamp FROM ask_view INNER JOIN (SELECT min(ask_price) AS ask_price, exchange, ticker FROM ask_view WHERE ticker='%(ticker)s' GROUP BY exchange) AS t2 USING (ticker, exchange, ask_price) WHERE ticker='%(ticker)s' GROUP BY exchange;" % t 
best_bids = "SELECT ticker, bid_price, bid_size, exchange, timestamp FROM bid_view WHERE ticker='%(ticker)s' ORDER BY bid_price DESC, bid_size DESC LIMIT 10;" % t
best_bids_per_exchange = "SELECT ticker, bid_price, max(bid_size) AS bid_size, exchange, timestamp FROM bid_view INNER JOIN (SELECT max(bid_price) AS bid_price, exchange, ticker FROM bid_view WHERE ticker='%(ticker)s' GROUP BY exchange) AS t2 USING (ticker, exchange, bid_price) WHERE ticker='%(ticker)s' GROUP BY exchange;" % t

with pool.connect('127.0.0.1', 3306, 'root', '', 'stocks') as conn:
    ba = conn.query(best_asks)
    bape = conn.query(best_asks_per_exchange)
    bb = conn.query(best_bids)
    bbpe = conn.query(best_bids_per_exchange)

print "\nBEST ASKS (OVERALL)\nticker\task_price\task_size\texchange"
for i in range(len(ba)):
    print str(ba[i]['ticker']) + "\t" + str(ba[i]['ask_price']) + "\t\t" + str(ba[i]['ask_size']) + "\t\t" + str(ba[i]['exchange']) + "\t\t" + str(ba[i]['timestamp'])

print "\nBEST ASKS (PER EXCHANGE)\nticker\task_price\task_size\texchange"
for i in range(len(bape)):
    print str(bape[i]['ticker']) + "\t" + str(bape[i]['ask_price']) + "\t\t" + str(bape[i]['ask_size']) + "\t\t" + str(bape[i]['exchange']) + "\t\t" + str(bape[i]['timestamp'])

print "\nBEST BIDS (OVERALL)\nticker\tbid_price\tbid_size\texchange"
for i in range(len(bb)):
    print str(bb[i]['ticker']) + "\t" + str(bb[i]['bid_price']) + "\t\t" + str(bb[i]['bid_size']) + "\t\t" + str(bb[i]['exchange']) + "\t\t" + str(bb[i]['timestamp'])

print "\nBEST BIDS (PER EXCHANGE)\nticker\tbid_price\tbid_size\texchange"
for i in range(len(bbpe)):
    print str(bbpe[i]['ticker']) + "\t" + str(bbpe[i]['bid_price']) + "\t\t" + str(bbpe[i]['bid_size']) + "\t\t" + str(bbpe[i]['exchange']) + "\t\t" + str(bbpe[i]['timestamp'])

print ""