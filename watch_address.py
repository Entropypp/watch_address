#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
import logging
import traceback
logging.basicConfig(level=logging.DEBUG)
import json 
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) 
import argparse
import smtplib
from email.message import EmailMessage



def get_sats_balance(btc_explorer_url,btc_address):
	try:
		request = requests.get("https://{}/api/address/{}".format(btc_explorer_url,btc_address),verify=False)
		return int(request.json()['txHistory']['balanceSat'])
	except Exception as e:
		logging.info(e)
		return -1

def address_balance_changed(sats_expected,sats_balance):
	return sats_balance != sats_expected


	
def send_email(from_email,to_email,subject,message,email_user,email_pass,server,port):
	msg = EmailMessage()
	msg.set_content(message)
	msg['From'] = from_email
	msg['To'] =  to_email.split(";") if to_email.find(";") else to_email
	msg['Subject'] = subject

	server = smtplib.SMTP(server, port)
	server.starttls()
	server.login(email_user, email_pass)
	server.send_message(msg)
	server.quit()
	return True

####Main
parser = argparse.ArgumentParser()
parser.add_argument('-x','--explorer',default='', required=True,help="Bitcoin Explorer URL:port")
parser.add_argument('-a','--address',default='', required=True,help="Bitcoin address to watch")
parser.add_argument('-n','--nickname',default='', required=True,help="Bitcoin address nickname")
parser.add_argument('-s','--sats',type=int, default=0, required=True,help="Expected sats ")
parser.add_argument('-f','--frm', default='', required=True,help="Email From Address")
parser.add_argument('-t','--to', default='', required=True,help="Email To")
parser.add_argument('-e','--server', default='', required=True,help="Email Server")
parser.add_argument('-u','--user', default='', required=True,help="SMTP User")
parser.add_argument('-p','--psw', default='', required=True,help="SMTP Password")
parser.add_argument('-o','--port', type=int, default=587, help="SMTP Port")
args = parser.parse_args()
sats_balance = get_sats_balance(args.explorer,args.address)
if sats_balance == -1:
	subject = "Cannot connect to node to check Address '{}'".format(args.nickname)
	message = "Your BTC Node seems to be down"
else:	
	subject = "Address '{}' balance has changed".format(args.nickname)
	message = "BTC balance is {} sats".format(sats_balance)

if address_balance_changed(args.sats,sats_balance):
	send_email(args.frm,args.to,subject,message,args.user,args.psw,args.server,args.port)

