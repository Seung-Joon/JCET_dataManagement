import os
import json
from datetime import datetime

timeFlag = datetime.now()
os.system('/usr/local/bin/python3.7 /home/oracle/Desktop/JCET_FIXDATA/CASE1/Case1_Error_Report.py ' + timeFlag.strftime("%Y-%m-%d, %H:%M:%S") + ' > ' + '/home/oracle/Desktop/JCET_FIXDATA/CASE1/output/ERROR_DATA_REPORT-' + timeFlag.strftime("%Y%m%d%H%M%S"))

with open('/home/oracle/Desktop/JCET_FIXDATA/CASE1/AppSettings.json') as json_file:
	appSettingData = json.load(json_file) # Read App Setting Data json file

mail_Settings = appSettingData["mailSettings"]

mail_Target = mail_Settings["addressee"] # 수신인 지정
mail_carbonCopy = ",".join(mail_Settings["carbonCopy"]) # 참조 지정

#print(mail_carbonCopy)

os.system("mail -s \"Data Error Warning Case 1 - " +  timeFlag.strftime("%Y-%m-%d, %H:%M:%S") + "\" " + mail_Target + " " + mail_carbonCopy + " < /home/oracle/Desktop/JCET_FIXDATA/CASE1/output/ERROR_DATA_REPORT-" + timeFlag.strftime("%Y%m%d%H%M%S"))

