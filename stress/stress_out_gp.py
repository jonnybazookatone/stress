from stress import WebPage
import datetime
import os, sys

def main():

  THEPATH = "/diska/home/jonny/sw/python/stress/stress"

  with open("{0}/users.txt".format(THEPATH), "r") as f:
    webpage, username, password = f.readlines()[0].strip().split(" ")
  
  GP = WebPage(webpage, headless=True)
  GP.pageLoad(wait="dlg")
  if not GP.timed_out:

    GP.pageLogin(username=username, password=password,
               username_value="u", password_value="p", login_value="b",
               wait="heading")
    GP.pageLogout(logout_value="tool-exit", confirm_value="//button[text()=\"Yes\"]",
                wait="dlg")

  GP.quit()

  today = datetime.datetime.today().isoformat()

  if not os.path.isfile("{0}/gp_timings.dat".format(THEPATH)):
    outfile = open("{0}/gp_timings.dat".format(THEPATH), "w")
    outfile.write("# Date GP_PageLoadTime GP_PageLoginTime GP_PageLogoutTime\n")
  else:
    outfile = open("{0}/gp_timings.dat".format(THEPATH), "a")

  outfile.write("{0} {1} {2} {3}\n".format(today, GP.load_time, GP.login_time, GP.logout_time))
  outfile.close()

  print("Time taken to load GP: {0}".format(GP.load_time))
  print("Time taken to login:   {0}".format(GP.login_time))
  print("Time taken to logout:  {0}".format(GP.logout_time))

if __name__ == "__main__":
  main()
