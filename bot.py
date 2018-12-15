from __future__ import (absolute_import, division, print_function, unicode_literals) 

import json as JSON
 
from bothub_client.bot import BaseBot 
from bothub_client.decorators import channel 
from bothub_client.decorators import command
from bothub_client.messages import Message  
import watson_developer_cloud
from watson_developer_cloud import AssistantV1


class Bot(BaseBot):            
	@command('start')
	def start_message(self, event, context, content):
		self.send_message('안녕하세요. 세종대왕봇입니다.')
		
	@channel()
	def default_handler(self,event,context):
	
		assistant = AssistantV1(
         version='2018-11-26',
         iam_apikey='o861MgDaxNdBUeAbUuU_EolNeHjjPrtCZbRHsmo7gOwB',
         url='https://gateway-wdc.watsonplatform.net/assistant/api'
		)
      
		n=event['content']
		n.rstrip()
		
		response = assistant.message(
         workspace_id='4aa742b3-5451-4692-9ac6-e241f4ff7f8f',
         input={
            'text': n
         }
		).get_result()
      
		user_data =  UserData(self, self.get_user_data())
		context = user_data.get_state()
      
      
		if context == 'IDLE': #직전 대화에서 학습과정이 없는 경우
			if response['intents'] == [] or response['intents'][0]['confidence'] <= 0.4: #인식하는 인텐트가 존재하지 않을 경우 or 인식된 인텐트의 정확도가 0.4 이하일 경우
				user_data.set_data(n)
				user_data.set_state('BUSY')
				self.EWord_to_KWord(response,n) #입력 값에 순화대상어가 있는지 확인 & 있을 경우 순화어 정보출력
				self.send_message("세종대왕봇: 잘 못 알아듣겠어요. 뭐라고 대답하면 좋을지 원하시는 대답을 입력해서 학습시켜주세요.\n")   
				if response['intents'] == []:
					print('입력값 의도 : {}\n'.format(response['intents']))
				else:
					if response['intents'][0]['confidence'] <= 0.4:
						print('인식률 : {}\n'.format(response['intents'][0]['confidence']))
				self.User_makes_intent(n,assistant,response)
          
			else: #인식하는 인텐트의 confidence가 0.7이상일 경우 
				if response['intents'][0]['confidence'] >= 0.7:
          
					self.EWord_to_KWord(response,n)
            
					if response['output']['text']==[]:
				
						self.send_message("세종대왕봇: 죄송해요. 지금은 대답하고 싶지 않아요.\n")
               
					else:
						self.send_message('세종대왕봇: {}\n'.format(response['output']['text'][0]))
						print('인식률:{}'.format(response['intents'][0]['confidence']))
						print('입력값 의도:{}\n'.format(response['intents'][0]['intent']))

				elif response['intents'][0]['confidence'] < 0.7: #인식하는 인텐트의 confidence가 0.7 미만일 경우
					self.EWord_to_KWord(response,n)
					self.send_message("세종대왕봇: 다시 한번 말씀해주세요. 이해하지 못했어요.\n")
					print('인식률:{}'.format(response['intents'][0]['confidence']))
					print('입력값 의도:{}\n'.format(response['intents'][0]['intent']))
					
		elif context == 'BUSY': #직전 대화에서 학습과정이 있는 경우
				
			user_data.set_state('IDLE')
			w = user_data.get_data()
			self.User_makes_dialog(assistant,w,n,response)
			
	def EWord_to_KWord(self,response,n): #순화대상어에 대한 순화어 정보출력함수
   
		json_data = open("words.json",'r')
		word_obj = JSON.loads(json_data.read())
      
		fin={}
		lists_for_key=[]
		#외래어 엔티티 식별
		if response['entities'] != []:
			for r in range(len(response['entities'])):
				if response['entities'][r]['confidence']>=0.85:
					if response['entities'][r]['value'] in word_obj.keys():
						fin[response['entities'][r]['value']] = [] 
	  
         
		 
				
			for key in word_obj.keys():
				if key in n:
					lists_for_key.append(key)
					#중복되는 외래어 중 하나만 출력하게 하기 위한 분류 작업
					for i in range(len(lists_for_key)):
						fin[lists_for_key[i]]=[]
						for j in range(len(lists_for_key)):
							if i != j:
								if lists_for_key[i] not in fin:
									if lists_for_key[i] in lists_for_key[j]:
										fin[lists_for_key[i]]=[lists_for_key[j]]
								else:
									if lists_for_key[i] in lists_for_key[j]:
										fin[lists_for_key[i]].append(lists_for_key[j])
		for i in fin:
			if fin[i] == []:
				self.send_message("세종대왕봇 : '{}'는(은) 외래어 입니다.순우리말로는 '{}'이(가) 있으니 순우리말을 사용해보세요.\n".format(i,word_obj[i]))

   
	def User_makes_intent(self,n,assistant,response): #인텐트 추가 함수
      
		n_r=n.replace(" ","_")
		
		if '?' or '!' or '~' in n_r:
			n_r = n_r.replace("?","_질문")
			n_r = n_r.replace("!","_느낌표")
			n_r = n_r.replace("~","_물결")
			
		new_intent = assistant.create_intent(
         workspace_id = '4aa742b3-5451-4692-9ac6-e241f4ff7f8f',
         intent = n_r,
         examples = [{'text':n }]
		).get_result()
      
      
	def User_makes_dialog(self,assistant,w,n,response): #다이얼로그 추가 함수
      
		w_r=w.replace(" ","_")
		
		if '?' or '!' or '~' in w_r:
			w_r = w_r.replace("?","_질문")
			w_r = w_r.replace("!","_느낌표")
			w_r = w_r.replace("~","_물결")
      
		new_dialog = assistant.create_dialog_node(
         workspace_id = '4aa742b3-5451-4692-9ac6-e241f4ff7f8f',
         conditions = '#'+w_r,
         dialog_node = w_r,
         output = {
            'text': n
         },
        ).get_result()

		self.send_message("세종대왕봇: '{}' 를 학습 중입니다. 1분 후에는 완료될 예정이니 그 전까지 다른 얘기라도 할까요?\n".format(new_dialog['output']['text']))

class UserData(object): 
	def __init__(self, bot, data): 
		self.bot = bot 
		self.user_data = {} 
		self.user_data['state'] = data.get('state') or 'IDLE' 
		self.user_data['data'] = data.get('data') or [] 
 
	def get_state(self): 
		return self.user_data['state'] 
      
	def set_state(self, state): 
		self.user_data['state'] = state 
		self.bot.set_user_data(self.user_data) 

	def get_data(self): 
		return self.user_data['data'] 
      
	def set_data(self, data): 
		self.user_data['data'] = data 
		self.bot.set_user_data(self.user_data) 
   