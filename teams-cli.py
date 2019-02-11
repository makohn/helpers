#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import ssl
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class NoTeamsForYou(Exception):
	pass

class TeamsAPI(object):
	channels = {
		'Python' : '*****.*****.onmicrosoft.com@emea.teams.ms'
	}

	sender = "******"
	smtp_node = 'mail.gmx.net'
	password="******"
	smtp_port = 587
	smtp_endpoint = None 
	context = ssl.create_default_context()

	def __init__(self):
		self.smtp_endpoint = smtplib.SMTP(self.smtp_node, self.smtp_port)

	def send_message(self, channel, subject, message):
		if message is None:
			raise NoTeamsForYou("No message specified, please try again!")

		if not channel in self.channels.keys():
			raise NoTeamsForYou("You have specified an invalid channel")

		mail_message = '<html><body>'
		for line in message.split('\n'):
			mail_message += f"<p>{line}</p>"
		mail_message += '</body></html>'

		msg = MIMEMultipart('alternative')
		msg['Subject'] = ""
		msg['From'] = self.sender
		msg['To'] = f"Channel <{self.channels[channel]}>"
		msg.attach(MIMEText(mail_message, 'html'))

		try: 
			self.smtp_endpoint.ehlo()
			self.smtp_endpoint.starttls(context=self.context)
			self.smtp_endpoint.ehlo()
			self.smtp_endpoint.login(self.sender, self.password)
			self.smtp_endpoint.sendmail(self.sender, self.channels[channel], msg.as_string())
		except Exception as e:
			print(e)
		finally:
			self.smtp_endpoint.quit()


if __name__ == '__main__':
	msg = sys.argv[1]
	channel = sys.argv[2]
	api = TeamsAPI()
	api.send_message(channel=channel, subject='', message=msg)