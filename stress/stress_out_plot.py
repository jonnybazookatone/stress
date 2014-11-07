import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dateutil import parser
import datetime
from python.lib.wikibot import wikiLib

def parse_gp(file_name="/diska/home/jonny/sw/python/stress/stress/gp_timings.dat"):
  
  infile = open(file_name, "r")
  lines = infile.readlines()
  
  out_dict = {"Date": [], "GP_PageLoadTime": [], "GP_PageLoginTime": [], "GP_PageLogoutTime": []}

  for i in range(len(lines)):
    value = [j for j in lines[i].strip().split(" ") if j !=""]
    if value[0] == "#": continue
    
    out_dict["Date"].append(parser.parse(value[0]))
    out_dict["GP_PageLoadTime"].append(value[1])
    out_dict["GP_PageLoginTime"].append(value[2])
    out_dict["GP_PageLogoutTime"].append(value[3])

  for item in out_dict.keys():
    out_dict[item] = np.array(out_dict[item])
  
  return out_dict

if __name__ == "__main__":
 
  gp = parse_gp()
 
  fig = plt.figure(0, figsize=(10,10))
  ax1 = fig.add_subplot(311)
  ax2 = fig.add_subplot(312)
  ax3 = fig.add_subplot(313)

  ax1.errorbar(gp["Date"], gp["GP_PageLoadTime"], fmt="o", ls="-", color="red", label="GP Page Load Time")
  ax2.errorbar(gp["Date"], gp["GP_PageLoginTime"], fmt="o", ls="-", color="blue", label="GP Page Login Time")
  ax3.errorbar(gp["Date"], gp["GP_PageLogoutTime"], fmt="o", ls="-", color="green", label="GP Page Logout Time")

  for ax in ax1, ax2, ax3:
    ax.legend()
    ax.grid(True)
    ax.set_xlabel("Date [ISO-Central European Time]")
    ax.set_ylabel("Time taken [seconds]")
    ax.set_ylim([-1,30])


  fig.autofmt_xdate() # automatically rotates dates appropriately for you figure. 
 
  plt.savefig("/diska/home/jonny/sw/python/stress/stress/gp_timings.jpg", format="jpg")

  upload = True
  if upload:
    wiki_content = wikiLib.exportPage("wgrpipe")
    wiki_content = wiki_content[0:len(wiki_content)-3]

    wiki_content.append("== GP Benchmark Test ==")
    wiki_content.append("'''Updated bi-hourly.''' Last updated: {0}".format(datetime.datetime.today().isoformat()))
    wiki_content.append("")
    wiki_content.append("{{attachment:gp_timings.jpg||width=\"800\"}}")

    wikiLib.writetoPage("wgrpipe", wiki_content, attachment="gp_timings.jpg", clobber=True)

  print("Uploaded")



#  plt.show()
