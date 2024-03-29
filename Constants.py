
"""
Constants.py
"""

Vendor_Name = 'DEB'

#Changes to be made every Quarter

#quarter_dates_v1 = {5:'2018-06-30', 4: '2018-03-31', 3: '2017-12-31', 2: '2017-09-30', 1: '2017-06-30', 0: '2017-03-31', -1: '2016-12-31', -2: '2016-09-30', -3: '2016-06-30'}
#screener_quarter_dates_v1 = {5: 'Jun 2018', 4: 'Mar 2018', 3: 'Dec 2017',2: 'Sep 2017',1: 'Jun 2017', 0: 'Mar 2017', -1: 'Dec 2016', -2: 'Sep 2016', -3: 'Jun 2016'}
#quarter_names_v1 = {5: 'Q118', 4: 'Q417', 3: 'Q317',2: 'Q217',1: 'Q117', 0: 'Q416', -1: 'Q316', -2: 'Q216', -3: 'Q116'}
#
#quarter_dates = {5:'2018-09-30', 4:'2018-06-30', 3: '2018-03-31', 2: '2017-12-31', 1: '2017-09-30', 0: '2017-06-30', -1: '2017-03-31', -2: '2016-12-31', -3: '2016-09-30'}
#screener_quarter_dates = {5: 'Sep 2018', 4: 'Jun 2018', 3: 'Mar 2018', 2: 'Dec 2017', 1: 'Sep 2017', 0: 'Jun 2017', -1: 'Mar 2017', -2: 'Dec 2016', -3: 'Sep 2016'}
#quarter_names = {5: 'Q218', 4: 'Q118', 3: 'Q417', 2: 'Q317',1: 'Q217',0: 'Q117', -1: 'Q416', -2: 'Q316', -3: 'Q216'}


quarter_dates_v1 = {5:'2018-09-30', 4:'2018-06-30', 3: '2018-03-31', 2: '2017-12-31', 1: '2017-09-30', 0: '2017-06-30', -1: '2017-03-31', -2: '2016-12-31', -3: '2016-09-30'}
screener_quarter_dates_v1 = {5: 'Sep 2018', 4: 'Jun 2018', 3: 'Mar 2018', 2: 'Dec 2017', 1: 'Sep 2017', 0: 'Jun 2017', -1: 'Mar 2017', -2: 'Dec 2016', -3: 'Sep 2016'}
quarter_names_v1 = {5: 'Q218', 4: 'Q118', 3: 'Q417', 2: 'Q317',1: 'Q217',0: 'Q117', -1: 'Q416', -2: 'Q316', -3: 'Q216'}

quarter_dates = {5:'2018-12-31', 4:'2018-09-30', 3:'2018-06-30', 2: '2018-03-31', 1: '2017-12-31', 0: '2017-09-30', -1: '2017-06-30', -2: '2017-03-31', -3: '2016-12-31'}
screener_quarter_dates = {5: 'Dec 2018', 4: 'Sep 2018', 3: 'Jun 2018', 2: 'Mar 2018', 1: 'Dec 2017', 0: 'Sep 2017', -1: 'Jun 2017', -2: 'Mar 2017', -3: 'Dec 2016'}
quarter_names = {5: 'Q318', 4: 'Q218', 3: 'Q118', 2: 'Q417', 1: 'Q317',0: 'Q217',-1: 'Q117', -2: 'Q416', -3: 'Q316'}


#latest_period='2018-06-30' #change this when lots of results announcements starts
latest_period='2018-12-31'
latest_quarter='Q318'

# How many quarters results needs to be processed. You need to have xpaths for those many Quarters in the xpaths table.
number_of_quarters_to_process = 9
min_xpath_quarter_seq = -3  # How many xpaths to pick ( 5 or 9)
min_quarter_seq_for_rev_profit_indicators = 1 # This flag is to be used to only look at 5-1 Quarter Seq for calculating rev & profit Indicators


#below is used in old scripts no longer used
latest_quarter_date = '2016-06-30 00:00:00'
#current_quarter = 'Q415'
previous_quarter = 'Q415'
prev_to_previous_quarter = 'Q315'

Authkey = '5_pRK9pKefuvZzHe-MkSy'


#dataset suffix
revenue_dataset_suffix = '_Q_SR'
profit_dataset_suffix = '_Q_NP'
profit_margin_dataset_suffix = '_Q_NETPCT'
operating_profit_dataset_suffix = '_Q_OP'
operating_prof_margin_dataset_suffix = '_Q_OPMPCT'
ebidt_dataset_suffix = '_Q_EBIDT'
ebidt_margin_dataset_suffix = '_Q_EBIDTPCT'


#Yahoo url & xpaths
yahooUrl_part1='http://finance.yahoo.com/quote/'
yahooUrl_stats='/key-statistics?p='
yahooUrl_financial='/financials?p='

yLastPrice_Xpath='//*[@id="quote-header-info"]/div[2]/div[1]/section/span[1]'
yEPS_Xpath='//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[1]/div[2]/div[4]/table/tbody/tr[7]/td[2]'
yPE_Xpath='//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[1]/div[1]/div/table/tbody/tr[3]/td[2]'
yPB_Xpath='//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[1]/div[1]/div/table/tbody/tr[7]/td[2]'
yROE_Xpath='//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[2]'
y52WeekHigh_Xpath='//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[2]/div/div[1]/table/tbody/tr[4]/td[2]'
y52WeekLow_Xpath='//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[2]/div/div[1]/table/tbody/tr[5]/td[2]'
yDebt_Xpath='//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[1]/div[2]/div[5]/table/tbody/tr[3]/td[2]'
yDebtEquityRatio_Xpath='//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[1]/div[2]/div[5]/table/tbody/tr[4]/td[2]'
yInterest_Xpath='//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[4]/table/tbody/tr[15]/td[2]'
yCurrentRatio_Xpath='//*[@id="main-0-Quote-Proxy"]/section/div[2]/section/div/section/div[2]/div[1]/div[2]/div[5]/table/tbody/tr[5]/td[2]'

#Google url & xpaths
googleUrl = 'https://www.google.com/finance?q=NASDAQ%3A'
googleFinance_Xpath='//*[@id="navmenu"]/li[7]/a'


gRevenueQ5_Xpath='//*[@id="fs-table"]/tbody/tr[1]/td[2]'
gRevenueQ4_Xpath='//*[@id="fs-table"]/tbody/tr[1]/td[3]'
gRevenueQ3_Xpath='//*[@id="fs-table"]/tbody/tr[1]/td[4]'
gRevenueQ2_Xpath='//*[@id="fs-table"]/tbody/tr[1]/td[5]'
gRevenueQ1_Xpath='//*[@id="fs-table"]/tbody/tr[1]/td[6]'

gProfitQ5_Xpath='//*[@id="fs-table"]/tbody/tr[25]/td[2]'
gProfitQ4_Xpath='//*[@id="fs-table"]/tbody/tr[25]/td[3]'
gProfitQ3_Xpath='//*[@id="fs-table"]/tbody/tr[25]/td[4]'
gProfitQ2_Xpath='//*[@id="fs-table"]/tbody/tr[25]/td[5]'
gProfitQ1_Xpath='//*[@id="fs-table"]/tbody/tr[25]/td[6]'

gOPMQ5_Xpath='//*[@id="fs-table"]/tbody/tr[13]/td[2]'
gOPMQ4_Xpath='//*[@id="fs-table"]/tbody/tr[13]/td[3]'
gOPMQ3_Xpath='//*[@id="fs-table"]/tbody/tr[13]/td[4]'
gOPMQ2_Xpath='//*[@id="fs-table"]/tbody/tr[13]/td[5]'
gOPMQ1_Xpath='//*[@id="fs-table"]/tbody/tr[13]/td[6]'

gEBITQ5_Xpath='//*[@id="fs-table"]/tbody/tr[17]/td[2]'
gEBITQ4_Xpath='//*[@id="fs-table"]/tbody/tr[17]/td[3]'
gEBITQ3_Xpath='//*[@id="fs-table"]/tbody/tr[17]/td[4]'
gEBITQ2_Xpath='//*[@id="fs-table"]/tbody/tr[17]/td[5]'
gEBITQ1_Xpath='//*[@id="fs-table"]/tbody/tr[17]/td[6]'


#Screener.in url & xpaths
screenerBaseUrl = 'https://www.screener.in/company/'
screenerBaseUrl_part2='/consolidated/'


# Final Rating Weightages
# revenueW = 1.0
roeW = 0.25
icW = 0.25  # Interest Coverage ratio
deW = 0.25 #debt equity ratio
opmANDebitW = 0.5
genericW = 1.0

#variable for Process_Screener_Excel_Data
browser_path='C:/Program Files (x86)/Mozilla Firefox/firefox.exe'
excel_download_dir='C:/xampp/htdocs/stockcircuitserver/fund_analysis/screener_excels'
excel_output_excel='C:/xampp/htdocs/stockcircuitserver/fund_analysis/screener_excels/output.csv'

# screener userid 7 pwd
screener_userid = 'richasharma2099@gmail.com'
screener_pwd = 'amit1973'

#
PHANTOMJS_PATH ='D:/workspace_pyCharm/phantomjs.exe'