#! /bin/python3

################################################################################
# A Python script to webscrape match information from cricbuzz.com and output as
# 1> A numbered, colour-coded list of available matches
# 2> Plain output of match selected using argument. Get status by :
#   send-notify "SCORE" "$(cric.py <num> | awk -f\( '{print $NF }' )"
# 3> Detailed information of current play as:
#   cric.py <num> d <loop-time>
################################################################################

import sys, requests, time, os
from datetime import datetime as dt
from colorama import Fore, Style
from bs4 import BeautifulSoup 

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

list = []
url = "https://www.cricbuzz.com"
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
res = soup.find_all( 'li' , class_ = 'cb-view-all-ga cb-match-card cb-bg-white')

for entry in res:
    info = entry.a.text
    
    for section in entry.find_all('div'):
        unix_time = section.get('ng-if')
        if unix_time is not None:
            info  += str(dt.fromtimestamp(int(unix_time.split()[0][1:-3])).strftime('@ %A, %I:%M %p'))
            break;
    list.append(info)

if len(sys.argv) == 1 :
    mxleft = max([entr.index('•') for entr in list])
    #num_list = [entr.split('•')[0].rjust(mxleft) + '[' + str(idx) + ']' + entr.split('•')[1] for idx, entr in enumerate(list)]
    num_list = [''.join([entr.split('•')[0].rjust(mxleft), '[' , str(idx), ']', entr.split('•')[1]]) for idx, entr in enumerate(list)]
    #print('\n'.join(num_list))
    for entry in num_list:
        if "won" in entry:
            print(Fore.YELLOW + entry)
        elif "No result" in entry or "abandoned" in entry:
            print(Fore.WHITE + entry)
        elif "(" in entry or "opt" in entry:
            print(Fore.GREEN + entry)
        else:
            print(Fore.CYAN + entry)

else:
    print( Style.BRIGHT + list[ int( sys.argv[1] ) ].replace("I ","I\n") + Style.RESET_ALL)

    if len(sys.argv) == 2: sys.exit()
    if sys.argv[2] == 'd':
        link = res[ int( sys.argv[1] ) ].find('a').get('href')
        try:
            while 1 :
                req = requests.get(url + link)
                soup = BeautifulSoup(req.content, "html.parser")
                res = soup.find( 'div', class_ = 'cb-col-67 cb-col')
                if not hasattr(res, "strings"): print(Fore.RED + "  Nothing to See"); sys.exit(0)
                list.clear()
                for string in res.strings:
                    list.append(string)
                print(Fore.CYAN + "\t\t" + str(dt.now()))
                for i in range(0,len(list)//6):
                    print(Fore.MAGENTA, end="") if i%3==0 else { print(Fore.GREEN, end="") if i > 2 else print(Fore.YELLOW, end="")}
                    for j in range(0,6):
                        num = 6*i+j
                        print(f'{list[num][0:20]:>20}', end="\t") if num%6==0 else print(f'{list[num]:5}', end=" ")
                    print("\n") if i%3==2 else print("")
                sys.exit(0) if len(sys.argv) == 3 else time.sleep(int(sys.argv[3]))
                for i in range(-3,len(list)//6):
                    print(LINE_UP, end=LINE_CLEAR)
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        print("Some Error")

Style.RESET_ALL
