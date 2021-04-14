from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import argparse
import json
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

host = "aa5gxwu8zqfvd-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "root.ca.pem"
certificatePath = "d0747de591.cert.pem"
privateKeyPath = "d0747de591.private.key"
port = 8883
clientId = "noah"
topic = "projectESP32/occupation"

'''class AWSIoTMQTTClient:
	def __init__(self):
		self.WhyIoTwhy = self.WhyIoTwhy()
'''
class WhyIoTwhy(GridLayout):
	def __init__(self, **kwargs):
		super(WhyIoTwhy, self).__init__(**kwargs)
		self.cols=3
		self.lot2 = Button(text='Lot2', background_color=(0, 1, 0, 1))
		self.lot1 = Button(text='Lot1', background_color=(0, 1, 0, 1))
		self.nulllot = Label()
		self.nulllot2 = Label()
		self.nulllot3 = Label()
		self.nulllot4 = Label()
		self.lot3 = Button(text='Lot3', background_color=(0, 1, 0, 1))
		button_quit = Button(text='Quit', font_size=48)
		button_quit.bind(on_press=self.quit_app)
		button_reload = Button(text='reload', font_size=48)
		button_reload.bind(on_press=self.reload)
		self.cc = Label(text='Number of Cars:', font_size=24)
		self.add_widget(self.lot2)
		self.add_widget(self.nulllot)
		self.add_widget(self.lot1)
		self.add_widget(self.lot3)
		self.add_widget(self.nulllot3)
		self.add_widget(self.nulllot4)
		self.add_widget(button_quit)
		self.add_widget(button_reload)
		self.add_widget(self.cc)

	def awsbs(self, instance, dic):
		for i in dic:
			if dic[i] == 'unoccupied':
				if i == 'lot1':
					self.lot1.background_color = (0, 1, 0, 1)
				elif i == 'lot2':
					self.lot2.background_color = (0, 1, 0, 1)
				elif i == 'lot3':
					self.lot3.background_color = (0, 1, 0, 1)
			elif dic[i] == 'occupied':
				if i == 'lot1':
					self.lot1.background_color = (1, 0, 0, 1)
				elif i == 'lot2':
					self.lot2.background_color = (1, 0, 0, 1)
				elif i == 'lot3':
					self.lot3.background_color = (1, 0, 0, 1)
			elif i == 'cars':
				self.cc.text = 'Number of Cars:{}'.format(dic[i])
			else:
				continue

	def reload(self, value):
		myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
		myAWSIoTMQTTClient.configureEndpoint(host, port)
		myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

		# AWSIoTMQTTClient connection configuration
		myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
		myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
		myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
		myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

		myAWSIoTMQTTClient.connect()

		myAWSIoTMQTTClient.subscribe(topic, 1, self.customCallback)

	def customCallback(self, client, userdata, message):
		print("Received a new message: ")
		msg = json.loads(message.payload)
		self.awsbs(message, msg)
		print(msg)
		print("from topic: ")
		print(message.topic)
		print("--------------")

	def quit_app(self, value):
		App.get_running_app().stop()

class Smth(App):
	def build(self):
		return WhyIoTwhy()





if __name__ == '__main__':
	Smth().run()
#loopCount = 0
while True:
	time.sleep(1)