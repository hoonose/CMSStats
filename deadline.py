import re, sys, datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
monthd  = {'January'  : 1,
           'February' : 2,
           'March'    : 3,
           'April'    : 4,
           'May'      : 5,
           'June'     : 6,
           'July'     : 7,
           'August'   : 8,
           'September': 9,
           'October'  :10,
           'November' :11,
           'December' :12}

def students_to_times(fname,yr):
  f = open(fname)
  contents = f.read()
  f.close()
  matches = re.findall('<span class="top_hug">(.*?)<dd>(.*?)</dd>(.*?)</span>',contents,re.S)
  dates = []
  for el in matches:
    parsed = re.search('(\w*) (\d*), (\d*):(\d*)(AM|PM)',el[1])
    year = yr
    month = monthd[parsed.group(1)]
    date = int(parsed.group(2))
    if parsed.group(3) == '12':
      hour = 0
    else:
      hour = int(parsed.group(3))
    if parsed.group(5) == 'PM':
      hour += 12
    mins = int(parsed.group(4))
    dates.append(datetime.datetime(year,month,date,hour,mins))
  return dates

def main(fname,hr,mint,day,mth,yr):
  dd = datetime.datetime(yr,day,mth,hr,mint)
  dates = students_to_times(fname,yr)
  dates.sort()
  dates.reverse()
  ttd = [dd - d for d in dates]
  gran = int(raw_input('Enter 0 for hour-level granularity, and 1 for minute-level: '))
  if gran == 0:
    ttd_div = 3600
    word = 'Hours'
    bin_div = 30
  else:
    ttd_div = 60
    word = 'Minutes'
    bin_div = 100
  ttd = [(el.seconds + el.days*24*3600)/ttd_div for el in ttd]
  cutoff = raw_input('I want to see submissions for the last X ' + word + ' (enter "all" to see all): ')
  if cutoff != 'all':
    cutoff = int(cutoff)
    ttd = filter(lambda x : x < cutoff,ttd)
  print "There were " + str(len(ttd)) + " submissions in this time period."
  ax = plt.axes()
  
  n, bins, patches = ax.hist(ttd,bin_div)
  ax.set_xlim(ax.get_xlim()[::-1])
  plt.xlabel(word + ' till deadline')
  plt.ylabel('Number of submissions')
  plt.show()

if __name__ == '__main__':
  fname = raw_input('What is the html file name? ')
  due = raw_input('Please enter when the assignment was due, in the following format (24 hours!): HOUR/MINUTES/DAY/MONTH/YEAR ')
  matches = re.search('(.*)/(.*)/(.*)/(.*)/(.*)',due)
  main(fname,int(matches.group(1)),int(matches.group(2)),int(matches.group(3)),int(matches.group(4)),int(matches.group(5)))
