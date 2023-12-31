#! /bin/python3

################################################################################
# A Python script to webscrape match information from cricbuzz.com and output as
# 1> A numbered, colour-coded list of available matches
# 2> Plain output of match selected using argument. Get status by :
#   send-notify "SCORE" "$(cric.py <num> | awk -f\( '{print $NF }' )"
# 3> Detailed information of current play as:
#   cric.py <num> d/s <loop-time>
################################################################################

import sys, requests, time, os
from datetime import datetime as dt
from colorama import Fore, Style
from bs4 import BeautifulSoup

LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"

list = []
url = "https://www.cricbuzz.com"
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
res = soup.find_all("li", class_="cb-view-all-ga cb-match-card cb-bg-white")

for entry in res:
    info = entry.a.text

    for section in entry.find_all("div"):
        unix_time = section.get("ng-if")
        if unix_time is not None:
            info += str( dt.fromtimestamp(int(unix_time.split()[0][1:-3])).strftime( "@ %A, %I:%M %p"))
            break
    list.append(info)

if len(sys.argv) == 1:
    mxleft = max([entr.index("•") for entr in list])
    # num_list = [entr.split('•')[0].rjust(mxleft) + '[' + str(idx) + ']' + entr.split('•')[1] for idx, entr in enumerate(list)]
    num_list = [ "".join( [entr.split("•")[0].rjust(mxleft), "[", str(idx), "]", entr.split("•")[1]]) for idx, entr in enumerate(list) ]
    for entry in num_list:
        if "won" in entry:
            print(Fore.YELLOW + entry)
        elif "No result" in entry or "abandoned" in entry:
            print(Fore.WHITE + entry)
        elif "run" in entry or "opt" in entry or "Break" in entry:
            print(Fore.GREEN + entry)
        else:
            print(Fore.CYAN + entry)

else:
    print(Style.BRIGHT + list[int(sys.argv[1])].replace("I ", "I\n") + Style.RESET_ALL)

    if len(sys.argv) == 2:
        sys.exit()
    if sys.argv[2] == "d":
        link = res[int(sys.argv[1])].find("a").get("href")
        try:
            while 1:
                req = requests.get(url + link)
                soup = BeautifulSoup(req.content, "html.parser")
                res = soup.find("div", class_="cb-col-67 cb-col")
                if not hasattr(res, "strings"):
                    print(Fore.RED + "  Nothing to See")
                    sys.exit(0)
                list.clear()
                for string in res.strings:
                    list.append(string)
                status = soup.find("div", class_="cb-col cb-col-67 cb-scrs-wrp").text
                print(Fore.CYAN + status + "\n\t\t" + str(dt.now()))
                for i in range(0, len(list) // 6):
                    print(Fore.MAGENTA, end="") if list[i * 6] == "Batter" or list[ i * 6 ] == "Bowler" else {
                        print(Fore.GREEN, end="")
                        if i > 2
                        else print(Fore.YELLOW, end="")
                    }
                    for j in range(0, 6):
                        num = 6 * i + j
                        print( f"{list[num][0:20]:>20}", end="\t") if num % 6 == 0 else print(f"{list[num]:5}", end=" ")
                    print("\n") if list[((i+1) * 6)%len(list)] == "Batter" or list[ ((i+1) *6)%len(list) ]== "Bowler" else print("")
                ##print(Fore.CYAN + soup.find("div", class_="cb-col cb-col-33 cb-key-st-lst").text[11:] + Style.RESET_ALL)

                sys.exit(0) if len(sys.argv) == 3 else time.sleep(int(sys.argv[3]))
                lines = os.get_terminal_size()[0]
                for i in range(-4-(len(status)//lines), len(list) // 6):
                    print(LINE_UP, end=LINE_CLEAR)
        except KeyboardInterrupt:
            sys.exit(0)
    if sys.argv[2] == "s":
        link = res[int(sys.argv[1])].find("a").get("href").split("/")[2]
        req = requests.get(url + '/api/html/cricket-scorecard/' + link)
        #print(Fore.GREEN + url + '/api/html/cricket-scorecard/' + link + Style.RESET_ALL)
        soup = BeautifulSoup(req.content, "html.parser")
        #print(Fore.CYAN + soup.find_all('div', class_=["cb-col cb-scrcrd-status cb-col-100 cb-text-live","cb-col cb-scrcrd-status cb-col-100 cb-text-live"]).text + Style.RESET_ALL)
        print(Fore.CYAN + soup.find('div').text + Style.RESET_ALL)
        for jim in soup.find_all('div', class_="cb-col cb-col-100 cb-ltst-wgt-hdr"):
            try:
                #for jam in jim.find_all('div', class_=["cb-col cb-col-100 cb-scrd-itms","cb-col cb-col-100 cb-scrd-sub-hdr cb-bg-gray"]):
                for jam in jim.find_all('div', recursive=False):
                    list.clear()
                    for jum in jam.find_all('div'):
                        list.append(jum.text)
                    count=0;
                    for jum in list:
                        count+=1;
                        if jum == "Batter":
                            print(Fore.YELLOW, end="")
                        elif jum == "Bowler":
                            print(Fore.GREEN, end="")
                        if count == 1:
                            print(f'{jum:^20}', end="\t")
                        elif count == 2:
                            print(f'{jum:<25}', end="\t")
                        else:
                            print(f'{jum:^6}', end="\t")
                    print()
                print('')
            except AttributeError: pass
    else:
        print("Some Error")

Style.RESET_ALL
#/api/html/cricket-scorecard/75602
#/live-cricket-scores/75602/sl-vs-nz-41st-match-icc-cricket-world-cup-2023
