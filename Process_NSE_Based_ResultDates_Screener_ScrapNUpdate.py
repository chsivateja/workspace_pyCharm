##Amit - purpose - Scrap the screener based on the results dates csv file mentioned below.
# Get all data for Quarter_date and Financial_ratio tables, update Final rating etc.

import csv
import DBManager
import platform
import Module_Final_Rating
import requests
import datetime
import Module_Scrapper_Screener_India_Stocks
import Constants


class Process_NSE_Based_ResultDates_Screener_ScrapNUpdate:

    def __init__(self):
        self.con = DBManager.connectDB()
        self.cur = self.con.cursor()

        self.module_Scrapper_Screener_India_Stocks = Module_Scrapper_Screener_India_Stocks.Module_Scrapper_Screener_India_Stocks()
        self.finalRatingModule = Module_Final_Rating.Module_Final_Rating()


    def csv_reader(self,file_obj):
        reader = csv.DictReader(file_obj, delimiter=',')
        nseidString= ''
        count = 0

        for line in reader:
            print(line["Symbol"]),
            print(line["BoardMeetingDate"])
            nseidString+=  "'%s'," % line["Symbol"]
            count +=1
            #call the Sc
        print ("Total records in CSV files to be processed- ", count)
        print( nseidString)
        nseidString = nseidString[:-1]
        nseidString = '('+nseidString+')'
        print( nseidString)
        return nseidString


    def getStockDetails(self,nseidString ):

        ###expalin sql - following sql will only take those nseid where latest quater data is NOT alread scrapped.
        ###This is to avoid scrapping ones alreay have latest data.
        #second union in the sql is to add stocks from result_calendar table who has declared results but not in the NSE
        # csv file for some reason..
        
        select_sql = "select fullid, nseid, enable_for_vendor_data,industry_vertical from stocksdb.stock_names sn where nseid in "
        select_sql += "(select nseid from"
        select_sql += "(select nseid from stocksdb.fa_quaterly_data_secondary where  period != '"+Constants.latest_period+"' and quater_sequence=5 and nseid in %s " %nseidString
        select_sql += " union "
        select_sql += "select nseid from stocksdb.fa_quaterly_data where period != '"+Constants.latest_period+"' and quater_sequence=5 and  nseid in %s ) temp ) " %nseidString
        select_sql += " union "
        select_sql += " select sn.fullid, sn.nseid, sn.enable_for_vendor_data,sn.industry_vertical from stocksdb.result_calendar rc, stocksdb.stock_names sn where rc.nseid = sn.nseid and sn.fullid not in "
        select_sql += " (select fr.fullid from stocksdb.final_rating fr  where latest_quarter = '"+Constants.latest_quarter+"') and (rc.result_date <= DATE_ADD(CURDATE(), "
        select_sql += " INTERVAL -1 DAY) and rc.result_date >= DATE_ADD(CURDATE(), INTERVAL -7 DAY) ) "

        #Testing sql
#        select_sql = "select fullid, nseid, enable_for_vendor_data,industry_vertical from stocksdb.stock_names sn where nseid in ('NIITTECH') "
        
        '''
        ###Explain sql -  this sql will try update all those stocks whihc does  not have latest quater results. This could be reason that
        # Nse calendar does not have entry for those
        select_sql = "select fullid, nseid, enable_for_vendor_data,industry_vertical from stocksdb.stock_names sn where nseid in "
        select_sql += "(select nseid from"
        select_sql += "(select nseid from stocksdb.fa_quaterly_data_secondary where  period != '"+Constants.latest_period+"' and quater_sequence=5 "
        select_sql += " union "
        select_sql += "select nseid from stocksdb.fa_quaterly_data where period != '"+Constants.latest_period+"'  and quater_sequence=5  ) temp ) "
        '''

        ###Explain Sql - This sql will update all stcoks in the csv file wheather they are already updated or not.
        #select_sql = "select fullid, nseid, enable_for_vendor_data,industry_vertical from stocksdb.stock_names sn where nseid in %s " %nseidString

        #print select_sql
        self.cur.execute(select_sql)

        rows = self.cur.fetchall()
        data = list()
        for row in rows:
            # print row[0], row[1]
            dd = dict()
            dd["fullid"] = row[0]
            dd["nseid"] = row[1]
            dd["enable_for_vendor_data"] = row[2]
            dd["industry_vertical"] = row[3]
            data.append(dd)
        # print data
        return data

    def getCSVDataFromNSE(self):
        url = 'https://www.nseindia.com/corporates/datafiles/BM_Last_1_WeekResults.csv'
#        url = 'https://www.nseindia.com/corporates/datafiles/BM_Last_15_Days.csv'
        #Other urls - https://www.nseindia.com/corporates/datafiles/BM_Last_15_Days.csv
        ##  https://www.nseindia.com/corporates/datafiles/BM_Last_1_Month.csv
        ### https://www.nseindia.com/corporates/datafiles/BM_Last_1_WeekResults.csv
        r = requests.get(url)
#        text = r.iter_lines()
#        reader = csv.DictReader(text, delimiter=',')
        decoded_content = r.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        reader = list(cr)
        
        nseidString= ''
        count = 0

        for line in reader[1:]:
            #print line
            #print(line["Symbol"]),
            #print(line["BoardMeetingDate"])
#            nseidString+=  " , " % line[0]
            nseidString+=   "'"+line[0]+"'"
            nseidString+=","
            
            count +=1
            #call the Sc
        print( "Total records in CSV files to be processed- ", count)
        print( "Stocks names from BM_Last_15_Days.csv file to be processed - ")
        #print nseidString
        nseidString = nseidString[:-1]
        nseidString = '('+nseidString+')'
        return nseidString



# ----------------------------------------------------------------------

thisObj = Process_NSE_Based_ResultDates_Screener_ScrapNUpdate()
nseidString = thisObj.getCSVDataFromNSE()
print( nseidString)
#csv_path = "BM_Last_15_DaysResults.csv"
# csv_path = "BM_Last_1_WeekResults.csv"
# with open(csv_path, "rb") as f_obj:
#     nseidString = thisObj.csv_reader(f_obj)

stock_names = thisObj.getStockDetails(nseidString)
print( "Stocks to be processed  ", stock_names.__len__(), " -  ", stock_names)
all_good_stock_names = thisObj.module_Scrapper_Screener_India_Stocks.updateAll(stock_names)
if(len(all_good_stock_names) > 0):
    thisObj.finalRatingModule.updateAll(all_good_stock_names)
else:
    print( " FinalRatingModule is not run since zero stocks in GOOD list")


