import pandas as pd
import json
from datetime import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt

# Opening JSON file, using 'test_json/result.json' for local development
# using 'result.json' for pushing to Gihub Repo (Github Actions)
f = open('result.json')
# returns JSON object as a dictionary
data = json.load(f)

# To transform json into dataframe
# colname =  data['results'][1]['result']['rawData'][0]
colname = ['Timestamp', 'Date', 'Category','Payment','Amount', 'Remarks'] 
list_result = data['results'][1]['result']['rawData']
df = pd.DataFrame(list_result[1:], columns =colname)

# transform date type
df['T_Date'] = df['Date'].apply(lambda x: dt.strptime(x, '%m/%d/%Y'))
df['Amount'] = df['Amount'].astype(float)

# Setting Time period
start_date = dt.today() - timedelta(days=7)
end_date = dt.today() - timedelta(days=1)

# Set time period exact to 00:00:00
start_date = start_date.replace(hour=0,minute=0,second=0, microsecond=0)
end_date = end_date.replace(hour=0,minute=0,second=0, microsecond=0)

# filter df for time period (last 1 week)
df_a = df[df['T_Date'] >= start_date]
df_b = df_a[df_a['T_Date'] <= end_date]

# The sum of expense in last week
week_expense = df_b['Amount'].sum()
week_expense = "{:.2f}".format(week_expense)

# string for output
start_date_str = start_date.strftime("%m/%d")
end_date_str = end_date.strftime("%m/%d")
sum_str = str(week_expense)

# test for print
print(sum_str)
print(start_date_str)
print(end_date_str)

# save the message in txt file
txt_file = open('message.txt',"w")
message_totxt = 'Last week: €' + sum_str +' from '+ \
	start_date_str+' to '+ end_date_str
txt_file.write(message_totxt)
txt_file.close()

# ===== To Draw plot =====

# Groupby Category & Sum the amount, Sorted it in decending way
cate_df = df_b[['Amount','Category']].groupby(by=['Category'],as_index=False).sum()
cate_df = cate_df.sort_values(by=['Amount'], ascending=False, ignore_index=True)

# make the explode difference by percentage
myexplode = [0]*len(cate_df)

# ===== Pie Plot ======
plt.figure(figsize=(12, 7))
plt.pie(cate_df.Amount,                           # Value
        labels = list(cate_df.Category),          # Labels
        autopct = "%1.1f%%",                      # precision
        # explode = myexplode,                      # explode way (list of float)
        pctdistance = 0.8,                        # distance betweeen num and center
        textprops = {"fontsize" : 15},            # fontsize
        shadow=False,                              # shadow
        radius = 1.2)                             # radius long

# draw white circle in the pie 
centre_circle = plt.Circle((0, 0), 0.8, fc='white')
fig = plt.gcf()

# Adding Circle in Pie chart
fig.gca().add_artist(centre_circle)

# Setting title and fontsize
plt.title("Category Donut Plot - \n TOTAL: €"+ str(sum(cate_df.Amount))[0:6]+ \
          "\n " + start_date_str +" to " +end_date_str,\
          {"fontsize" : 15}, x=1.3,y=1)
# Legend position, content values & position
plt.legend(bbox_to_anchor=(1.2, 0.4), loc="upper left",fontsize=14,
          labels=['%s , %1.0f' % (l, (float(s))) for l, s in zip(list(cate_df.Category), list(cate_df.Amount))],)

plt.tight_layout()
plt.savefig("figure/CategoryPlot.jpg", dpi=200)
# plt.show()