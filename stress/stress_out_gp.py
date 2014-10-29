from stress import WebPage
import datetime
import os, sys

if __name__ == "__main__":

  with open("users.txt", "r") as f:
    username, password = f.readlines()[0].strip().split(" ")
  
  GP = WebPage("http://wgrpipe.ls.eso.org:9222")
  GP.pageLoad(wait="dlg")

  GP.pageLogin(username=username, password=password,
               username_value="u", password_value="p", login_value="b",
               wait="heading")
  GP.pageLogout(logout_value="tool-exit", confirm_value="//button[text()=\"Yes\"]",
                wait="dlg")
  GP.quit()

  today = datetime.datetime.today().isoformat()

  if not os.path.isfile("gp_timings.dat"):
    outfile = open("gp_timings.dat", "w")
    outfile.write("# Date GP_PageLoadTime GP_PageLoginTime GP_PageLogoutTime\n")
  else:
    outfile = open("gp_timings.dat", "a")

  outfile.write("{0} {1} {2} {3}\n".format(today, GP.load_time, GP.login_time, GP.logout_time))
  outfile.close()

  print("Time taken to load GP: {0}".format(GP.load_time))
  print("Time taken to login:   {0}".format(GP.login_time))
  print("Time taken to logout:  {0}".format(GP.logout_time))

