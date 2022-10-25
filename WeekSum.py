import pandas as pd
import json
from datetime import datetime as dt
from datetime import timedelta

# Opening JSON file
f = open('result.json')
# returns JSON object as a dictionary
data = json.load(f)

# To transform json into dataframe
colname =  data['results'][1]['result']['rawData'][0]
list_result = data['results'][1]['result']['rawData']
df = pd.DataFrame(list_result[1:], columns =colname)

# transform date type
df['T_Date'] = df['Date'].apply(lambda x: dt.strptime(x, '%m/%d/%Y'))
df['Amount'] = df['Amount'].astype(float)

# Setting Time period
start_date = dt.today() - timedelta(days=7)
end_date = dt.today()

# Set time period exact to 00:00:00
start_date = start_date.replace(hour=0,minute=0,second=0, microsecond=0)
end_date = end_date.replace(hour=0,minute=0,second=0, microsecond=0)

# filter df for time period (last 1 week)
df_a = df[df['T_Date'] >= start_date]
df_b = df_a[df_a['T_Date'] <= end_date]

# The sum of expense in last week
week_expense = df_b['Amount'].sum()

# string for output
start_date_str = start_date.strftime("%Y/%m/%d")
end_date_str = end_date.strftime("%Y/%m/%d")
sum_str = str(week_expense)

# test for print
print(sum_str)
print(start_date_str)
print(end_date_str)