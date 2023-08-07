import pandas as pd
import json
from datetime import datetime as dt
from datetime import timedelta
import calendar
import matplotlib.pyplot as plt
from util.plots import pie_plot, line_plot

def pre_month(sourcedate: dt) -> dt :
    year = sourcedate.year if sourcedate.month !=1 else sourcedate.year - 1
    month = sourcedate.month - 1 if sourcedate.month > 1 else 12
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return dt(year, month, day)

# Opening JSON file, using 'test_json/result.json' for local development
# using 'result.json' for pushing to Gihub Repo (Github Actions)
f = open('result.json')
# returns JSON object as a dictionary
data = json.load(f)

# To transform json into dataframe
# colname =  data['results'][1]['result']['rawData'][0]
colname = ['Timestamp', 'Date', 'Category','Payment','Currency','Amount', 'Remarks'] 
list_result = data['results'][1]['result']['rawData']
df = pd.DataFrame(list_result[1:], columns =colname)

# transform date type
df['T_Date'] = df['Date'].apply(lambda x: dt.strptime(x, '%m/%d/%Y'))
df['Amount'] = df['Amount'].astype(float)

# Setting Time period
start_date = pre_month(dt.today())
end_date = dt.today() - timedelta(days=1)

# Set time period exact to 00:00:00
start_date = start_date.replace(hour=0,minute=0,second=0, microsecond=0)
end_date = end_date.replace(hour=0,minute=0,second=0, microsecond=0)

# filter df for time period (last 1 week)
df_a = df[df['T_Date'] >= start_date]
interval_df = df_a[df_a['T_Date'] <= end_date]

# The sum of expense in last week
month_expense = interval_df['Amount'].sum()
month_expense = "{:.2f}".format(month_expense)

# string for output
start_date_str = start_date.strftime("%m/%d")
end_date_str = end_date.strftime("%m/%d")
sum_str = str(month_expense)

# test for print
print("Total Expense: €" + sum_str)

# save the message in txt file
txt_file = open('message.txt',"w")
message_totxt = 'Last Month: €' + sum_str +' from '+ \
	start_date_str+' to '+ end_date_str
txt_file.write(message_totxt)
txt_file.close()
print(message_totxt)

# Groupby Category & Sum the amount, Sorted it in decending way
cate_df = interval_df[['Amount','Category']].groupby(by=['Category'],as_index=False).sum()
cate_df = cate_df.sort_values(by=['Amount'], ascending=False, ignore_index=True)

# Groupby day & sum the amount (for line plot)
fordaydf = interval_df[interval_df.Category != "Insurance"]
fordaydf = fordaydf[fordaydf.Category != "Transportation"]
fordaydf = fordaydf[fordaydf.Category != "Rental"]
day_df = fordaydf[['Amount', 'T_Date']].groupby(by=['T_Date'], as_index=True).sum()
# ===== To Draw plot =====
pie_plot(cate_df, start_date_str, end_date_str)
line_plot(day_df, start_date, end_date)
