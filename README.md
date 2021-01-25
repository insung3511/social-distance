<div align="center" style="text-align:center">

# Korean
If you wanna read English version document <a href="#eng-version">Click here</a>
</div>

# social-distance
사회적 거리두기를 시각화 하며 측정을 하는 CCTV 프로젝트 이다. 사실 이게 선린인터넷고등학교 2020 IoT 경진대회 때문에 시작하게 된 프로젝트이다. 사실 리드미를 작성해보니 아마 보고서랑 거의 비슷하게 갈거 같긴 한듯. 

# What did I used it?
## macOS
<pre>
./Software
macOS Catlina (실제 개발 당시에는 카탈리나 였으나 지금은 Big sur)
Python 3.9
openCV 4.4.0

./Hardware
Facetime Webcam
Just my Macbook Pro (early, 2015)
</pre>

## Raspberry Pi
<pre>
./Software
Raspberry Pi OS
Python 3.7.2 (virtuelenv)
openCV 4.1.1 (virtuelenv)

./Hardware
Raspberry Pi Camera v2
</pre>

# Directory
가장 중요한 Python 파일들은 아래와 동일하다.
```python
main.py 
plot.py
utils.py
```
그리고 프론트 파일은 
```HTML
./Iot_Contest/frontend/
```
안에 모두 담아 두었다. 프론트 엔드 같은 경우는 경진대회에서 같이 진행 했던 민서가 모두 만들었다. <BR> 
<strong>SHOUT OUT TO M.S.</strong>

# Run
```bash
$ python main.py
```
단 OpenCV와 numpy가 정-상적으로 설치가 되어있다는 가정하에 해야한다. 또한 OpenCV를 pip를 통한 설치보다는 build를 통한 설치를 추천한다. 이유는 pip로 설치하는 경우에는 Pre-CPU 가 된 모듈을 받아 설치하는거라 빌드가 안된다. 가공식품과 직접 요리 하는 것의 차이라고 생각하면 된다.

# 실행 순서도
말로 설명하기에는 너무나도 복잡한데 막상 보면 간단함. 이게 무슨 말인지는 직접 사진을 보시고 판단 해주시길... 
![working1](./images/pic1.png)
![working2](./images/pic2.png)
![working3](./images/pic3.png)
![working4](./images/pic4.png)
여기서 몇가지 전공적(?)인 내용을 추가 하자면 Human Detection 에서는 yolov3를 활용하였다. <a href="./models/yolov3.cfg"> ~~"폴더 안에 모델 있어요.."~~ </a>. main.py 에서 yolov3.cfg 모델을 활용하는데 plot.py 에서 화면 변환을 하고 좌표를 끌어 오고 Human Detection 이 되는 것이다. 참고로 지금 저거 그대로 돌리면 분명 터진다. ~~내 잘못 아니다!~~ <br> <br>

이게 깃허브에서 100MB 이상의 파일을 못 올린다고 한다. 이거 업로드를 할때 Github Desktop을 사용해서 하는데 올릴때 에러난다고 하도 징징 거려서 빡쳐서 지웠다. 그래서 이 코드 그대로 쓸거면 <a href="https://pjreddie.com/media/files/yolov3.weights">여기서</a> 모델(혹은 가중치? 공부 더해서 수정할께욤ㅎ) 을 다운 받아줘야 한다. 다운 받은 후에는 <u> models/ </u> 디렉토리에 넣어줘야 한다.

# Final Result!
![Safari Capture Image](./images/pic5.png)
![Physica Real Photo](./images/pic6.png)
대회 전에 삼성동 별마당 도서관에서 테스트를 한 결과물이다. 

# 기획은 했으나 구현을 하지 못한 부분
가장 먼저 Time table이다. 각 시간 마다 사람 명 수를 저장하여 DB에 저장하는 것이 목표 였으나 사회적 거리두기에 중점을 두고 계속 진행을 하다 보니 이 부분은 신경 쓰지 못한 것 같다. 

# 이 시국에 굳이 별마당?
이유는 진짜 간단하다. 조명 때문이다. <br> 
yolov3 의 모델은 훌륭한 모델이다. 진짜로. 굉장히 빠른 속도로 낮은 사양에서도 빠르게 Object Detection이 가능한 모델 이기 때문이다. 하지만 조명의 영향을 받는 것은 어쩔수 없는 사실이다. 컴퓨터 시각처리를 진행하면 어쩔수 없이 영향을 받게 되는 요소 중 하나이다. 실내에서는 항상 일정한 조명을 쏘기 때문에 그림자가 여러 방해 요소들이 확 줄어든다. 물론 별마당 도서관의 천장이 유리로 되어 있어서 뚫려 있기는 한다 하지만 그래도 일정 조명은 똑같은 조명이다. <br> 

또한 이 프로젝트의 주 목표는 사회적 거리두기의 측정인 만큼 통풍이 잘 되지 않는 곳에서 코로나 확산은 실외보다 더더욱 심하다. 그렇기 때문에 별마당 도서관이 가장 적당하다고 판단을 하였다.

<br> 
별마당 외에도 여러 장소에서 테스트를 진행 하였다. 테사로사 POSCO(?) 에서도 해봤는데 각도가 안나오고 조명이 감성 조명이라고 해야하나 한 쪽만 내리 찍는 조명인지랑 테스트 장소로서 적합하지가 않았다. 또한 창문으로 하게 되면 반사가 생기고 앞에 나무들 때문에 사람 인식율이 떨어진다. 다른 쪽으로 간다 해도 건물들이 있다. ~~아니 일단 무엇보다 반사가 너무 불편해~~. 별마당이 개인적으로는 가장 좋았다. 단점으로는 눈치게임 자리 잡기.. 

# 아니 파일 정리좀..
그게 있잖아요,, 저도 할려고 했는데 이게 뭐 하나 잘못 지웠다가 갑자기 싹다 다 안되서 다시 수정하고 시간 낭비할거 같아서 그냥 덤프 파일 그대로 올립니다...  <br>

~~오해의 요지가 있을까봐 작성해둡니다. 그.. 여기 보면 CSS 파일이 굉장히 많아서 제가 CSS코드를 많이 작성한 줄 알거 같은데 아닙니다..~~ <br> 

Jan.16.2021. 일단 파일 정리를 하긴 했지만 아직 불필요한 파일들이 더 있을거 같다. 지속적으로 정리를 할 예정

# My final comment
일단 라즈베리파이 너무 뜨거워서 손은 정말 따뜻했다. 방열판은 진짜 필수 이고 라즈베리파이 전압이 굉장히 부족했다. 그래서 하다가 터질까봐 많이 불안하다가 다행히도 안 터졌다. 

<div align="center" style="text-align:center" id="eng-version">

# English

</div>

# social-distance
It is a CCTV project that visualizes and measures social distance. In fact, the project started because of the IoT contest held at Sunrin Internet High School in 2020. Actually, I'm using README.md, but I think it'll be almost the same as the report I submitted to school.

# What did I used it?
## macOS
<pre>
./Software
macOS Catlina (It was Catalina at the time of development, but now using Big Sur.)
Python 3.9
openCV 4.4.0

./Hardware
Facetime Webcam
Just my Macbook Pro (early, 2015)
</pre>

## Raspberry Pi
<pre>
./Software
Raspberry Pi OS
Python 3.7.2 (virtuelenv)
openCV 4.1.1 (virtuelenv)

./Hardware
Raspberry Pi Camera v2
</pre>

# Directory
The most important Python files are:
```python
main.py 
plot.py
utils.py
```
and frontend files are:
```HTML
./Iot_Contest/frontend/
```
I have placed it in the directory I created above. In the case of the front end, it was produced by Minseo, who worked on the project together. <BR> 
<strong>SHOUT OUT TO M.S.</strong>
~~For your information, Minseo is a our club members.~~

# Run
```bash
$ python main.py
```
OpenCV and numpy must be installed normally. It is also recommended that you install OpenCV through a build instead of installing pip. This is because if you install it as a pip, you will receive a pre-CPU module and cannot build it. You can think of it as the difference between processed food and cooking it yourself.

# Operating Principles
It's too complicated to explain in words, but it's simple. I want you to look at the picture and see what it means.
![working1](./images/pic1.png)
![working2](./images/pic2.png)
![working3](./images/pic3.png)
![working4](./images/pic4.png)
Here are some of the key (?) content that Human Detection leverages yolov3. Using the <a href="./models/yolov3.cfg">yolov3.cfg</a> model on main.py includes screen conversion, importing coordinates, and person detection on plot.py. For your information, it doesn't work if you turn it as it is. ~~That's not my fault!~~
<br>

They say that they cannot upload more than 100MB of files to GitHub. I deleted it because there was an error while using Github Desktop when uploading. Therefore, if you want to use this code, you must download the <a href="https://pjreddie.com/media/files/yolov3.weights">model</a>. After download the model, you must moved it and put it in the __./model__ directory.

# Final Result!
![Safari Capture Image](./images/pic5.png)
![Physica Real Photo](./images/pic6.png)
This is the result of the test at the Coex library in Samseong-dong before the presentation.

# The part planned but not implemented.
First of all, it's a timetable. The goal was to save people every hour and save them in the DB, but I couldn't pay attention to this as I kept focusing on social distancing.

# Why did you go to the library?
The reason is really simple. It's because of the lighting. <br>

The model of yolov3 is a great model. A very fast model that can detect very low specification objects. However, it is inevitable to be affected by the lighting. One of the factors that inevitably affect the processing of computer images. The shadow is greatly reduced because constant lighting is always done indoors. Of course, the ceiling of the library is glass, so it is open, but the lighting is the same. <br> 

Also, the main goal of the project is to measure social distance, so the spread of corona in poorly ventilated areas is more serious than outdoors. So I decided that the COEX library is the most suitable. <br> 

The test was conducted in several places besides Stade. Although it was purchased as POSCO (?) Tessa, it was not suitable as a test site to check whether there were no angles or whether the lighting was emotional. Also, if you do it through the window, the tree in front of you will reduce the recognition rate of people. <br>

# Yo, man' Clean up the files...
As you know, I tried to do something wrong, but it suddenly didn't work. So I am uploading the dump file because it will be a waste of time.

I'm writing it in case you get misunderstood. As you can see here, there are so many CSS files that there are many CSS codes, but the actual amount of code used is very small.

January 16, 2021. I cleaned up the file, but I think there are still more unnecessary files. It is configured continuously.
