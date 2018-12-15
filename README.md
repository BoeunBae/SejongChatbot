# SejongChatbot(세종대왕챗봇)

순화어,신조어에 대한 정보를 제공하는 비목적성 대화형 챗봇

1. 사용자가 외래어를 사용하면 해당 외래어에 대한 순화어를 제공하고 난 후 대화를 이어나갑니다.

2. 사용자가 신조어의 뜻을 물어보면 해당 신조어의 의미를 알려줍니다.

3. 특정 목적이 없는 일상대화가 가능하며 학습되지 않은 사용자의 입력에 대한 대답을 사용자가 직접 학습시킬 수 있습니다.


# 개발환경

window 10 (x64)

IBM Watson Bluemix

Python 3.6

Bothub Studio(Chatbot hosting service)

Telegram(interface)


# 개발과정

1. IBM 블루믹스를 이용하여 데이터를 학습시킵니다.(학습 파일 - SejongChatbot.json)

2. 외래어와 순화어의 정보가 있는 API를 json형태로 저장하여 원하는 외래어, 순화어 데이터를 추가합니다.(순화어 파일 - words.json)

3. Bothub를 통해 코드를 작성하여 IBM Watson을 호출하여 높은 confidence(인식률)에 따라 output을 출력합니다.

4. Telegram과 연동하여 사용자가 직접 챗봇을 사용할 수 있도록 합니다.

