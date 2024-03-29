# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 06:28:00 2018

@author: amahe6
"""
import numpy as np
import pandas as pd
import DBManager
#import Module_Get_Live_Data_From_Google
import time
import EmailUtil
import ModuleAmitException
import time as t

class Process_SEPA_Analysis:
    
    def __init__(self):
        self.con = DBManager.connectDB()
        self.engine = DBManager.createEngine()
        self.cur = self.con.cursor()
#        self.module_Get_Live_Data_From_Google = Module_Get_Live_Data_From_Google.Module_Get_Live_Data_From_Google()


    def getLastComment(self):

        select_sql = "select  a.nseid, a.is_imp, a.comments from stock_sepa_analysis a, (select max(id) as id from stock_sepa_analysis where comments != ' ' group by nseid) b  "
        select_sql += " where a.id = b.id " 


        df = pd.read_sql(select_sql, self.con)
#        df = df['nseid'].str.strip() 
#        df = df.apply(lambda x: x.str.strip())
        return df  
    
    def getMarketDataForAStock(self, nseid):
        
        select_sql = "select * from stocksdb.stock_market_data smd where smd.nseid = '%s' order by my_date  " % (nseid)
        df = pd.read_sql(select_sql, self.con)
        return df            
        
        
    def findSEPA(self,stock_names):
        
        outputDf = pd.DataFrame()
        for index, row in stock_names.iterrows():
            nseid = row.nseid
            short_name = row.short_name
            isFO = row.isFO
            
#            print('Processing  - ', nseid, ' at # - ', index)
            df = self.getMarketDataForAStock(row['nseid'])
            if df.empty:
#                print("No Data for ", nseid)
                continue
            fulldf = df.drop(['id','high', 'low', 'open','last', 'turnover', 'last_modified'], axis=1)
           
            
            MAdf = self.calculateAverages(fulldf) 
            #MAdf has only one record now
            MAdf['short_name'] = [short_name]
            MAdf['isFO'] = [isFO]
            MAdf = self.findSEPAStage(MAdf, fulldf) # you need complere df to get last 10 records for filtering volumes for up/down days
            outputDf = outputDf.append(MAdf)
            
        return outputDf

    def getFOStockList(self):

        #Prod sql 
        select_sql = "select symbol nseid , symbol as short_name from stocksdb.fo_mktlots sn "
        df = pd.read_sql(select_sql, self.con)
        df = df.apply(lambda x: x.str.strip())
        return df  
    
    def getStockList(self):

        ##Get all stocks from amit_portfolio and all FO stocks         

        select_sql = " select SUBSTR(fullid, 5) nseid, short_name, 'n' as isFO FROM stocksdb.fa_financial_ratio "
        select_sql += " where SUBSTR(fullid, 5) not in (select symbol from  stocksdb.fo_mktlots )  "
        select_sql += " union "
        select_sql += " select  SUBSTR(fullid, 5) nseid, short_name, 'n' as isFO  FROM stocksdb.fa_financial_ratio_secondary "
        select_sql += " where SUBSTR(fullid, 5) not in (select symbol from stocksdb.fo_mktlots )   "
        select_sql += " union "
        select_sql += " select symbol nseid,sn.name,  'y' as isFO  from stocksdb.fo_mktlots fo, stock_names sn "
        select_sql += " where sn.nseid = fo.symbol "
        
        # sql to try on less records
#        select_sql = "SELECT SUBSTR(fullid, 5) nseid, short_name, 'n' as isFO FROM stocksdb.fa_financial_ratio  "
        
        #testing 1
#        select_sql = "select nseid, nseid as short_name,'n' as isFO from stocksdb.stock_names sn where nseid in ('AXISBANK')"

#        select_sql = "select  nseid, nseid as short_name,'n' as isFO from stocksdb.amit_portfolio sn where nseid in ('APOLLOTYRE')"
        #testing 2 
#        select_sql = "select symbol nseid , symbol as short_name, 'y' as isFO  from stocksdb.fo_mktlots sn "


        df = pd.read_sql(select_sql, self.con)
#        df = df['nseid'].str.strip() 
        df = df.apply(lambda x: x.str.strip())
        return df  
    
    def findSEPAStage(self, mydf, fulldf):
        mydf.is_copy = False
        nseid = mydf['nseid'].iloc[0]
        isFO = mydf['isFO'].iloc[0]
        last_x_records_df = fulldf.tail(10)
        pos_day_count = 0
        neg_day_count = 0
        pos_days_vol_sum = 1 #avoid divid by zero !
        neg_days_vol_sum = 1
        pos_close_chg_sum = 0
        neg_close_chg_sum = 0
#        neg_to_pos_vol_ratio = 0
        
        for index, row in last_x_records_df.iterrows():
#            print(row)
            if(row['perct_change'] > 0 ):
                pos_day_count +=1
                pos_days_vol_sum +=row['volume']
                pos_close_chg_sum +=row['perct_change']
            else:
                neg_day_count +=1
                neg_days_vol_sum +=row['volume']
                neg_close_chg_sum +=row['perct_change']
            
#        neg_to_pos_vol_ratio = round(neg_days_vol_sum/pos_days_vol_sum, 2)
        pos_close_chg_sum = round(pos_close_chg_sum,2)
        neg_close_chg_sum = round(neg_close_chg_sum,2)
        total_price_change = round(pos_close_chg_sum+neg_close_chg_sum, 2)
        gap_100dma_200dma = mydf['100dma'].values[0] - mydf['200dma'].values[0] # assuming 100d > 200d
        
        pivot_point1 =  round((mydf['100dma'].values[0] - 0.4 * gap_100dma_200dma),2)
        pivot_point2 =  round((mydf['200dma'].values[0] - 0.2 * gap_100dma_200dma),2)
        
        close = mydf['close'].values[0]
        volume = mydf['volume'].values[0]
        min_volume =  50000
#        print(nseid, pos_day_count,neg_day_count,pos_days_vol_sum,neg_days_vol_sum,neg_to_pos_vol_ratio,pos_close_chg_sum, neg_close_chg_sum)
        print(nseid, close,volume, gap_100dma_200dma,pivot_point1, total_price_change)
        

        #Stage 1->2 bw_050_100_dma Logic
        if((mydf['50dma'] < mydf['100dma'] ).bool() and (mydf['100dma'] < mydf['200dma']).bool()
             and (mydf['5d_avg_vol'] > mydf['10d_avg_vol'] ).bool()  and pos_days_vol_sum > neg_days_vol_sum  
             and (mydf['close'] > mydf['50dma']).bool() and (mydf['close'] < mydf['100dma']).bool()
             and total_price_change > 4 ): 
            
            mydf['Stage'] = ['Stage 1->2 bw_050_100_dma']
#            print("\n\n**** Stage 1->2 for bw_050_100_dma", nseid , "\n\n")

        #Stage 1->2 bw_100_200_dma Logic
        elif((mydf['50dma'] < mydf['100dma'] ).bool() and (mydf['100dma'] < mydf['200dma']).bool()
             and (mydf['5d_avg_vol'] > mydf['10d_avg_vol'] ).bool()  and (mydf['close'] > mydf['100dma']).bool() 
             and (mydf['close'] < mydf['200dma']).bool() 
             and total_price_change > 4 and pos_days_vol_sum > neg_days_vol_sum  ): 
            
            mydf['Stage'] = ['Stage 1->2 bw_100_200_dma']
            print("\n\n**** Stage 1->2 bw_100_200_dma for ", nseid , "\n\n")
            
            
        #Stage 2
        elif((mydf['50dma'] > mydf['100dma'] ).bool() and (mydf['100dma'] > mydf['200dma']).bool() 
                and (mydf['5d_avg_vol'] > mydf['10d_avg_vol'] ).bool() #and (mydf['10d_avg_vol'] > mydf['15d_avg_vol']).bool()
                  and pos_days_vol_sum > neg_days_vol_sum and (mydf['close'] > mydf['50dma']).bool()  ):   
                
            mydf['Stage'] = ['Stage 2']
            
        
        #Stage 3   
        # This stage was not useful hence commenting and earlier stage3->4 made as stage 3
        # and new logic for actula 3->4
        
#        elif((mydf['close'] < mydf['50dma']).bool() and (mydf['close'] > mydf['100dma']).bool() 
#                  and (mydf['50dma'] > mydf['100dma']).bool() and (mydf['100dma'] > mydf['200dma']).bool() ):
#                 #and (mydf['50dma'] > mydf['100dma'] ).bool()  and (mydf['50dma'] > mydf['200dma'] ).bool() ):
#            mydf['Stage'] = ['Stage 3']
##            print("\n\n**** Stage 3 ! for ", nseid , "\n\n")

        
#        #Stage 3->4 logic
#        elif(neg_days_vol_sum > pos_days_vol_sum and total_price_change < -4
#              and  (mydf['50dma'] < mydf['100dma']).bool() and (mydf['100dma'] > mydf['200dma']).bool() ):
#            mydf['Stage'] = ['Stage 3->4']
##            print("\n\n**** Stage 3->4 for ", nseid , "\n\n")

#        #Stage 3->4 logic Amit Try new logic - I
#        elif((mydf['50dma'] > mydf['100dma']).bool() and (mydf['100dma'] > mydf['200dma']).bool() 
#                and (mydf['close'] < mydf['200dma']).bool() 
#                ):
#            mydf['Stage'] = ['Stage 3->4']
#            print("\n\n**** Stage 3->4 for ", nseid , "\n\n")
            
        #Stage 3 logic Amit Try new logic (earleir was stage 3-4)
        elif((mydf['50dma'] > mydf['100dma']).bool() and (mydf['100dma'] > mydf['200dma']).bool() 
                and (mydf['close'] < mydf['100dma']).bool() and (mydf['close'] > mydf['200dma']).bool()
                and (mydf['close'] < pivot_point1).bool()
                and total_price_change < 0    ):
            
            mydf['Stage'] = ['Stage 3']
#            print("\n\n**** Stage 3 for ", nseid , "\n\n")

        #Stage 3->4 logic Amit Try new logic -  333
        elif((mydf['50dma'] > mydf['100dma']).bool() and (mydf['100dma'] > mydf['200dma']).bool() 
                and (mydf['close'] < mydf['200dma']).bool() #and (mydf['close'] > mydf['200dma']).bool()
                and (mydf['close'] < pivot_point2).bool()
                and total_price_change < 0
                ):
            mydf['Stage'] = ['Stage 3->4']
#            print("\n\n**** Stage 3->4 for ", nseid , "\n\n")

            
        #Stage 1->2 Sideways for FO stocks
        elif(isFO == 'y' and (mydf['5d_avg_vol'] > mydf['10d_avg_vol'] ).bool() and pos_days_vol_sum > neg_days_vol_sum 
             and (mydf['close'] > mydf['50dma']).bool() and (mydf['close'] > mydf['100dma']).bool()
             and (mydf['close'] > mydf['200dma']).bool() ):
                
            mydf['Stage'] = ['Stage 1->2 Sideways FO']
#            print("\n\n****Stage 1->2 Sideways FO for ", nseid , "\n\n")

        
        #No Stage perhaphs...
        else:
#            print(" NO - Close DMA Criteria is NOT Met for ",nseid)
            mydf['Stage'] = ['None']
        
#        print(mydf)
        return mydf


    def calculateAverages(self, df):
        #this is to supress the copy warning..
        df.is_copy = False
        
        df['50dma'] = df['close'].rolling(window=50).mean()
        df['100dma'] = df['close'].rolling(window=100).mean()
        df['200dma'] = df['close'].rolling(window=200).mean()
        
        df['5d_avg_vol'] = df['volume'].rolling(window=5).mean()
        df['10d_avg_vol'] = df['volume'].rolling(window=10).mean()
        df['15d_avg_vol'] = df['volume'].rolling(window=15).mean()
        
        
        # Amit - dont drop these col, now added to SEPA table
#        df = df.drop(['prev_day_close', 'perct_change','prev_day_vol','vol_chg_perct'], axis=1)
#        print(df[-1:])
        #you need only last record
        df = df[-1:]
        df.is_copy = False
        df['dist_50dma'] = ((df['close'] - df['50dma'])* 100)/df['50dma']
        df['dist_100dma'] = ((df['close'] - df['100dma'])* 100)/df['100dma']
        
        df['5d_10d_vol_chg'] = ((df['5d_avg_vol'] - df['10d_avg_vol'])* 100)/df['10d_avg_vol']
        df['5d_15d_Vol_chg'] = ((df['5d_avg_vol'] - df['15d_avg_vol'])* 100)/df['15d_avg_vol']
        
        return df        

    
    def saveInDB(self, df):
        df = self.copyCommentsFromPreviousRecords(df)
        df.to_sql('stock_sepa_analysis', self.engine, if_exists='append', index=False)
        print("SEPA saved in DB")         

    def copyCommentsFromPreviousRecords(self,df):
        
        commDf = self.getLastComment()
        df['comments'] = ''
        df['is_imp'] = ''
        for i, row in commDf.iterrows():
            nseid = row['nseid']
            comments = row['comments']
            is_imp = row['is_imp']
            df.loc[df['nseid'] == nseid, 'comments'] = comments
            df.loc[df['nseid'] == nseid, 'is_imp'] = is_imp
            

            
        return df
       
        
thisObj = Process_SEPA_Analysis()
pd.set_option('display.expand_frame_repr', False)
np.set_printoptions(suppress=True)
pd.options.display.float_format = '{:.2f}'.format

start_time = time.time()
stock_names= thisObj.getStockList()
#fo_stocks= thisObj.getFOStockList()
print ("stock_names - \n", stock_names)
print('Processing # of stocks - ', len(stock_names))
df = thisObj.findSEPA(stock_names)

if not df.empty:
    df = df.loc[df['Stage'] != 'None']
#    df = df.loc[df['Stage'] == 'Stage 1->2 bw_100_200_dma']
    
    tempdf = df[['nseid','Stage']]
    print(tempdf.to_string())
    print("\n # of stocks - ", len(tempdf))
          
    #df = df[(df['close'] < 400) & (df['dist_50dma'] > 9)]
    try:
        # uncomment folowing lines for prod
        thisObj.saveInDB(df)
        print(" NOT Saved in DB")
    except Exception as e1:
        print ("\n******Exception in saving SEPA in DB, sleep for 5 minute and try...\n\n\n" )
        print (str(e1))
        ModuleAmitException.printInfo()
        #May be Db conn has gone bad so close it and initialize again.. Lets try !
        thisObj.con.close()                    
        thisObj.con = DBManager.connectDB()
        thisObj.cur = thisObj.con.cursor()
    
        t.sleep(300)
        thisObj.saveInDB(df)


#print ("\n\n****** Saved results in DB *****************" )
#print("Total time taken by process --- %s seconds ---" % (time.time() - start_time))
EmailUtil.send_email_with_body("Process_SEPA_Analysis.py",tempdf.to_string())
#    