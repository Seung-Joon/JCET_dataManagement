
import os
import sys
import json
from datetime import datetime

timeFlag = datetime.now()
systemInterpreterPath = "/usr/local/bin/python3.7"
workingAreaPath = os.path.dirname(os.path.abspath(__file__))
generatorFile = workingAreaPath + "/Case1_Error_Report.py"
outputFilePath =  workingAreaPath + '/output/ERROR_DATA_REPORT-'
appSettingDataPath = workingAreaPath + '/AppSettings.json' 
textFilePath =  outputFilePath + timeFlag.strftime("%Y%m%d%H%M%S")

class NoDataException(Exception):
	pass


if __name__ == '__main__':
    try:
        # 레포트 생성
        os.system(systemInterpreterPath + ' ' + generatorFile + ' ' + timeFlag.strftime("%Y-%m-%d, %H:%M:%S") + # Interpreter pythonFile argv1 argv2
                ' > ' +
                textFilePath) #레포트파일

	
        if len(open(textFilePath).readlines()) < 12:
                raise NoDataException

        # 메일 정보 로딩
        with open(appSettingDataPath) as json_file:
                appSettingData = json.load(json_file) # App Setting Data 불러옴

        mail_Settings = appSettingData["mailSettings"]
        mail_Target = mail_Settings["addressee"] # 수신인 지정
        mail_carbonCopy = ",".join(mail_Settings["carbonCopy"]) # 참조 지정


        # 메일 전송
        os.system("mail -s \"Data Error Warning Case 1 - " +  timeFlag.strftime("%Y-%m-%d, %H:%M:%S") + "\" " + # 제목
                mail_Target + " " + # 수신인
                mail_carbonCopy + # 참조
                " < " +
                textFilePath) #레포트 파일

        print("Report Generated.")


    except NoDataException:
        print("Error!! -> Error Data Is Not Exsist.")

    except NoDataException:
        pass


