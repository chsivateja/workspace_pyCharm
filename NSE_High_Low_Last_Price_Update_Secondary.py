#!/usr/bin/env python
#Amit Purpose - Run this program to update the last_price, 52 week high , 52 week low etc for all the SECONDARY stcoks in
# fa_financial_ratio_secondary table. Set the flag update_now to y for stock where update is needed.

import DBManager
import time
import NSE_High_Low_Last_Price_Module
import EmailUtil


class NSE_High_Low_Last_Price_Update_Secondary:

    def __init__(self):
        print ("Calling NSE_High_Low_Last_Price_Update_Secondary constructor")
        self.con = DBManager.connectDB()
        self.cur = self.con.cursor()
        self.nseHighLowModule = NSE_High_Low_Last_Price_Module.NSE_High_Low_Last_Price_Update()

    def run(self, table_name):
        #obj = NSE_High_Low_Last_Price_Update()
        start_time = time.time()
        stock_names =  self.nseHighLowModule.getStocksMarkedForUpdates(table_name)
        print (stock_names)
        print( "Number of Stocks processing - ", len(stock_names))
        totalCount = len(stock_names)
        count = 0

        for row in stock_names:
            # print row
            count = count + 1
            print ("\n\ncalling MSE_Hogh_Low for - ", row['fullid'], "(", count, "/", totalCount, ")")

            self.nseHighLowModule.updateLiveData(row, table_name)

        print( "\n\n Quarterly Data Exception list - ")
        print(  self.nseHighLowModule.qd_exception_list)
        print( "\nFinancial Ratio Exception list - ")
        print(  self.nseHighLowModule.fr_exception_list)

        print("\n\nTime Taken --- in minutes ---", int((time.time() - start_time)) / 60)


# run for secondary stocks
print( "\n\n\n run for secondary stocks")
thisObj = NSE_High_Low_Last_Price_Update_Secondary()
thisObj.run('fa_financial_ratio_secondary')

EmailUtil.send_email_as_text("NSE_High_Low_Last_Price_Update_Secondary", thisObj.nseHighLowModule.fr_exception_list, "")

