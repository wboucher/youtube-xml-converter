import datetime
import requests
import math
import html
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Convert YouTube XML subtitles into standard SRT subtitle format

def GetTime(x):
    time_parts = math.modf(float(x))
    sec = timedelta(seconds=time_parts[1],milliseconds=time_parts[0])
    d = datetime(1,1,1) + sec

    return "%02d:%02d:%02d,%03d" % (d.hour, d.minute, d.second, d.microsecond)

in_url = input('Type the URL to convert: ')
in_format = input('SRT or Transcript? ')
r = requests.get(in_url)
xml_subtitles = r.text
xml_soup = BeautifulSoup(xml_subtitles, "lxml-xml")
xml_text = xml_soup.find_all('text')

if(in_format.lower() == 'srt'):
    for i in range(0, len(xml_text)):
        line_start = xml_text[i]['start']
        line_dur = xml_text[i]['dur']
        time_start = GetTime(xml_text[i]['start'])
        time_dur = GetTime(xml_text[i]['dur'])
        time_end = GetTime(float(line_start) + float(line_dur))

        print(f'{i+1}')
        print(f'{time_start} --> {time_end}')
        print(f"{html.unescape(xml_text[i].text)}\n")
elif(in_format.lower() == 'transcript'):
    out_text = ''
    for i in range(0, len(xml_text)):        
        out_text += html.unescape(xml_text[i].get_text().rstrip('\r\n'))
        out_text += ' '
    print(out_text)