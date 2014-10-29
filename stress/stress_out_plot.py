import numpy as np
import matplotlib.pyplot as plt
from dateutil import parser

def parse_gp(file_name="gp_timings.dat"):
  
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
 
  fig = plt.figure(0)
  ax1 = fig.add_subplot(221)
  ax2 = fig.add_subplot(222)
  ax3 = fig.add_subplot(223)

  ax1.errorbar(gp["Date"], gp["GP_PageLoadTime"], fmt="o", ls="-", color="red")
  ax2.errorbar(gp["Date"], gp["GP_PageLoginTime"], fmt="o", ls="-", color="blue")
  ax3.errorbar(gp["Date"], gp["GP_PageLogoutTime"], fmt="o", ls="-", color="green")
 
  for ax in ax1, ax2, ax3:
    ax.grid(True)
    ax.set_xlabel("Date [ISO]")
    ax.set_ylabel("Time [seconds]")

  fig.autofmt_xdate() # automatically rotates dates appropriately for you figure. 
 
  plt.show()
