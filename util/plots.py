import pandas as pd 
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta

def pie_plot(catedf: pd.DataFrame, start_str: str, end_str: str):
# ===== Pie Plot ======
	# make the explode difference by percentage
	myexplode = [0]*len(catedf)

	plt.figure(figsize=(12, 8))
	plt.pie(catedf.Amount,                           # Value
	        labels = list(catedf.Category),          # Labels
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
	plt.title("Category Donut Plot - \n TOTAL: €"+ str(sum(catedf.Amount))[0:6]+ \
	          "\n " + start_str +" to " +end_str,\
	          {"fontsize" : 15}, x=1.3,y=1)
	# Legend position, content values & position
	plt.legend(bbox_to_anchor=(1.2, 0.4), loc="upper left",fontsize=14,
	          labels=['%s , %1.0f' % (l, (float(s))) for l, s in zip(list(catedf.Category), list(catedf.Amount))],)

	plt.tight_layout()
	# plt.show()
	plt.savefig("figure/CatMonthPlot.jpg", dpi=200)

def get_date_list(date1: dt , date2: dt) -> list:
	date_list = []
	for n in range(int((date2 - date1).days)+1):
		date_list.append((date1+timedelta(n)).strftime("%Y-%m-%d"))
	return date_list

def get_amount_list(date_list: list, ori_date: list, ori_amount: list) -> list:
	count = 0
	lst_amount = []
	ori_date_str = [i.strftime("%Y-%m-%d") for i in ori_date]
	for str_dt in date_list:
		if str_dt in ori_date_str:
			lst_amount.append(ori_amount[count])
			count+=1
		else: lst_amount.append(0)
	return lst_amount

def line_plot(daydf: pd.DataFrame, startdate: dt, enddate: dt):
	datelist = get_date_list(startdate, enddate)
	amountlist = get_amount_list(datelist, list(daydf.index), list(daydf.Amount))	
	sum_amount = str(sum(amountlist))
	plt.figure(figsize=(10, 6))
	plt.plot(datelist, amountlist, color='red', marker='o')
	plt.title('Monthly Line Plot w/o Rental, Insu, Trans: €' +sum_amount, fontsize=14)
	plt.xlabel('Date', fontsize=14)
	plt.xticks(rotation=90)
	plt.ylabel('Amount', fontsize=14)
	for x,y in zip(datelist,amountlist):

	    label = "{:.0f}".format(y)

	    plt.annotate(label, # this is the text
	                 (x,y), # these are the coordinates to position the label
	                 textcoords="offset points", # how to position the text
	                 xytext=(10,7), # distance from text to points (x,y)
	                 ha='center',
	                 rotation=45,
	                 fontsize = 10) # horizontal alignment can be left, right or center

	plt.tight_layout()
	plt.grid(True)
	plt.savefig("figure/LinePlot.jpg", dpi=200)
	# plt.show()


