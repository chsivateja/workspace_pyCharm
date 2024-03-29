
#import urllib2
from urllib.request import urlopen,Request
import urllib.request
import json
import DBManager
import pandas
from datetime import datetime, time
import EmailUtil
import time as t
import requests

class GoogleFinanceAPI:
    def __init__(self):
        self.con = DBManager.connectDB()
        self.cur = self.con.cursor()
        #https://finance.google.com/finance?q=NSE:NCC
        self.url_prefix = "https://finance.google.com/finance?q="
        self.url_suffix = "&output=json"

    def getStockList(self):
        select_sql ="select fullid, nseid from stocksdb.amit_portfolio where display_seq is not null and is_inactive != 'y' order by display_seq "

        self.cur.execute(select_sql)

        rows = self.cur.fetchall()
        data = list()
        for row in rows:
            # print row[0], row[1]
            dd = dict()
            dd["fullid"] = row[0]
            dd["nseid"] = row[1]
            data.append(dd)
        # print data
        return data

    def getFOStockList(self):
        print ("\n\n***************  Running it for only FO stocks\n\n")
        select_sql ="select fullid, nseid from stocksdb.amit_portfolio where display_seq is not null and is_fo = 'y' and is_inactive != 'y'  order by display_seq "

        self.cur.execute(select_sql)

        rows = self.cur.fetchall()
        data = list()
        for row in rows:
            # print row[0], row[1]
            dd = dict()
            dd["fullid"] = row[0]
            dd["nseid"] = row[1]
            data.append(dd)
        # print data
        return data

    '''
    def get(self, symbol):
        url = self.prefix + "%s" % ( symbol)
        u = urllib2.urlopen(url)
        content = u.read()

        obj = json.loads(content[3:])
        return obj[0]
    '''
    def getAllQuotes(self, stock_names):

        try:
            content = []


            for row in stock_names:
                try:
                    fullid = row['fullid']
                    if '&' in fullid:
                        fullid = fullid.replace('&','%26')
                    url = self.url_prefix+ "%s" % ( fullid)+self.url_suffix
                    
#                    url = 'https://finance.google.com/finance?q=NASDAQ:AAPL&output=json'
#                    url = 'https://finance.google.com/finance?q=NSE%3AINFY&output=json'
#                    url= 'https://finance.google.com/finance/getprices?q=JINDALSTEL&x=NSE'
                    
                    rsp = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
                    content2 = {}
                    if rsp.status_code in (200,):
                        temp = rsp.content
                    
#                        for line in temp.splitlines():
#                            print(line)
#                            
                        fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
                        #print fin_data

                        #print('Last Trade Price: {}'.format(fin_data['l']))
                        #print('Change: {}'.format(fin_data['c']))
                        #print('Change %: {}'.format(fin_data['cp']))


                        lp = fin_data['l'];
                        volume = fin_data['vo'];

                        if 'M' in volume:
                            volume = volume.replace("M", "")
                            volume = float((volume).replace(",", ""))
                            volume = volume * 1000000  ## convert million into number
                        elif 'B' in volume:    
                            volume = volume.replace("B", "")
                            volume = float((volume).replace(",", ""))
                            volume = volume * 1000000000  ## convert million into number
                            
                        else:
                            volume = float((volume).replace(",", ""))
                         
                        volume = round(volume)
                        # content2.append(row['fullid']);
                        # content2.append('{}'.format(fin_data['l']));
                        # content2.append('{}'.format(fin_data['c']));
                        # content2.append('{}'.format(fin_data['cp']));
                        # content2.append('{}'.format(fin_data['op']));
                        # content2.append('{}'.format(fin_data['e']));
                        # content2.append('{}'.format(fin_data['t']));

                        content2['fullid'] = fullid;
                        lp = float(('{}'.format(fin_data['l'])).replace(",", ""));
                        change = float(('{}'.format(fin_data['c'])).replace(",", ""));

                        prev_close = lp-change;

                        content2['l'] = '{}'.format(fin_data['l']).replace(",", "");
                        content2['c'] = '{}'.format(fin_data['c']).replace(",", "");
                        content2['cp'] = '{}'.format(fin_data['cp']).replace(",", "");
                        content2['pcls'] = '{}'.format(prev_close);

                        content2['e'] = '{}'.format(fin_data['e']);
                        content2['t'] = '{}'.format(fin_data['t']);
                        content2['volume'] = '{}'.format(volume);
                except Exception as e1:
                    print ("\n******Amit exception in getAllQuotes for fullid - \n ", fullid)
                    print (str(e1))
                    pass

                #print content2
                content.append(content2);

            #print content

        except Exception as e:
            print ("\n******Amit exception in getAllQuotes \n ")
            print (str(e))
            pass


        return content


    def saveIntoDB(self, allQuotes):

        print ("\n*** Amit saving following qoutes to database")
        records = []
        fullid= ""
        for row in allQuotes:

            try:
                fullid = row['e']+":"+row['t']
                #print "fullid - ", fullid
                record = (( row['l'], row['c'],row['cp'],row['pcls'],row['volume'], fullid))
                print (record)
                records.append(record )

            except Exception as e:
                print ("\n******Amit saveIntoDB, some issue with quotes, row data - ", row)
                print (str(e))
                pass

        # for record in records:
        #     print record
        #     print record[0], record[1]
        #     sql = "update amit_portfolio set last_trade_price=%s,  price_change=%s, change_perct=%s, previous_close=%s where nseid=%s"
        #     self.cur.execute(sql, tuple(record))

        #use batch execute rahter above  1by 1
        sql = "update amit_portfolio set last_trade_price=%s,  price_change=%s, change_perct=%s, previous_close=%s, volume=%s where fullid=%s"
        self.cur.executemany(sql, records)
        self.con.commit()

    def in_between(self,now, start, end):
        if start <= end:
            return start <= now < end
        else:  # over midnight e.g., 23:30-04:15
            return start <= now or now < end

if __name__ == "__main__":
    c = GoogleFinanceAPI()

    #stock_names = c.getStockList()
    #Get only FO when Google is slow...
    stock_names = c.getFOStockList()

    records = [] ## LIST OF LISTS
    minutes_count = 0  # compare with 7 Hrs run daily from 9-4 pm (7*60=420)
    #EmailUtil.send_email_as_text(" amit_portfolio_update.py job started - ", "", "")
    print ("\n*** Amit Started getting quotes")

    #while minutes_count < 420:
    #Run b/w morning 9 am to 4:00 pm IST
    while (c.in_between(datetime.now().time(), time(5,00), time(22,00))):
        allQuotes = c.getAllQuotes(stock_names)

        if allQuotes:
            c.saveIntoDB(allQuotes)
        else:
            print ("\n*** Amit All Quotes from Google were empy(due to exception i guess) so not saving in DB")
        if minutes_count == 0:
            EmailUtil.send_email_as_text(" amit_portfolio_update.py job started - ", "", "")
        minutes_count = minutes_count+1
        print ("\n*** Amit Sleeping for 2 minute, remaining loops (420-x)- ", 420- minutes_count, " | Time - ", datetime.now())
        t.sleep(60)

    
    print ("\n*** Amit Exiting the google quote process...TIME is  - ", datetime.now().time())