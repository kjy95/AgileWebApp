# AgileWebApp
make agile web app
1.
python 에서 html 로 메세지를 보내는 과정이 있어서(로그인 실패) messages 모듈을 설치해야 됩니다.
powershell에서 django-messages-master 디렉토리로 이동후 아래 설치법에 있는 명령어
-python setup.py install
-easy_install django-messages
다운로드 링크 :
https://github.com/arneb/django-messages
설치법 : 
http://django-messages.readthedocs.io/en/latest/install.html
<<<<< messages 모듈은 이제 github에 같이 올라가 있습니다 다운받으실 필요는 없고, 설치만 해주시면 됩니다>>>>>
Konlpy(한국어 정보처리 모듈, 문자열에서 명사를 추출 수 있는 모듈) 설치하기 
본 모듈은, wordcloud 를 생성할 때, 명사만을 추출해서 진행을 하기 때문에 설치해줍니다.
0. 비트수를 모두 맞추어 주셔야 합니다. (가끔 'python이 중지되었습니다' 하고 서버가 자동으로 꺼집니다)
OS 비트 == python 비트 == java 비트 (ex) OS 가 64비트면 python 도 64비트, java도 64 비트가 설치 되어야해요)
Java 비트수 체크 방법 : cmd -> java -d64 -version , cmd -> java -d32 -version 
Python 비트수 체크 방법 : cmd or powershell -> python -> 아래 python 코드 입력
#python code
import sys,platform
print(platform.architecture())
#endcode
1. konlpy 는 jdk를 요구 합니다.
http://www.oracle.com/technetwork/java/javase/downloads/index.html
OS 비트(64비트,32비트)와 같은 비트 수를 받으셔야 됩니다. (OS 비트 == JDK 비트)
2. jdk는 환경 변수 설정이 필요합니다. 
http://prolite.tistory.com/975
3. jpype whl 파일이 필요합니다.
http://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype 
파이썬 버젼(비트 아님)과 알맞는 파일을 설치해 주셔야 됩니다. 
파이선 버젼 체크 : powershell or cmd -> python --version 
ex ) JPype1-0.6.2-cp36-cp36m-win_amd64 --> JPype1 0.62버젼, cp36 --> python 3.6 버전
설치 : pip install 파일명.whl
4. 모듈 설치
    1. pip install konlpy   (konlpy 공식 사이트 : http://konlpy.org/ko/latest/)
    2. pip install pytagcloud (wordcloud를 만드는 모듈 입니다. )
    3. pip install pygame (wordcloud 를 만드는데 필요한 모듈입니다.)
    4. pip install simplejson (설치 도중 오류가 발생하면, 1.pip uninstall simplejson 2. easy_install simplejson 으로 해결됬었습니다)
    5. pip install matplotlib
    6. pip install numpy
    7. pip install psycopg2
5. 폰트 설정
    -pytagcloud 모듈 설치가 선행되어야 합니다. 
    -pytagcloud 가 기본적으로 한글은 표시가 안되서 별도로 폰트를 넣어줘야 합니다.
    1. pytagcloud 모듈이 설치된 폴더로 이동해야됩니다.
     (C:\Users\사용자계정\AppData\Local\Programs\Python\Python36\Lib\site-packages\pytagcloud)
     주로 이폴더에 pytagcloud 설치가 되는데, 사용자마다 위치가 조금씩 다를 수 있습니다.
    2. pytagcloud 에서 fonts 폴더로 이동합니다. 
    3. github에 나눔 글꼴 파일을 같이 올렸습니다. (NanumGothic)
     (http://ngio.tistory.com/m/5264 여기서도 받을 수 있습니다.)
    4. 나눔글꼴파일(NanumGothic.ttf)를 2번에서의 fonts 폴더에 넣어주고, fonts.json 을 열어줍니다.
    5. 적절한 위치?에 아래와 같은 코드를 추가해줍니다.
    {
    "name": "Nanum Gothic",
    "ttf": "NanumGothic.ttf",
    "web": "http://fonts.googleapis.com/earlyaccess/nanumgothic.css"
  	},

6. import 오류 
 http://davincii.tistory.com/entry/matplotlib-import-%EC%8B%9C-%EC%97%90%EB%9F%AC-%EB%B0%9C%EC%83%9D-%EB%8C%80%EC%B2%98%EB%B0%A9%EB%B2%95
 matplotlib 에서 생기는 오류 해결방법.
<<<<<<<20170811 황규도>>>>>>>
7. 엑셀 output
http://www.hanul93.com/openpyxl-basic/
위 사이트를 따라 openyxl설치
import xlwt
-https://pypi.python.org/pypi/xlwt 
-위 홈페이지에서 최신 버전의 xlwt를 다운로드하고
-pip install xlwt
8. 차트, 차트 이미지 추출
pip install plotly --upgrade
pip install ipython
