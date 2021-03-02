from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for,session 
import requests
import json
import os
import MySQLdb
import re
import messagebird

app = Flask(__name__)

@app.route('/webhook', methods=[ 'POST',"GET"])
def webhook():        
    client = messagebird.Client('NKLuEuNHL8H6uvFZreyIAkt1C', features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])
    balance = client.balance()
    print('Your balance:\n')
    print('  amount  : %d' % balance.amount)
    print('  type    : %s' % balance.type)
    print('  payment : %s\n' % balance.payment)
    
    
    message = client.conversation_create_message(conversation.id, {
    'channelId': 'a84cb9c1-674b-4784-be79-76d9ceb43ba0',
    'type': 'text',
    'content': {
        'text': balance.type
    }
    })

    return message
if __name__ == '__main__':
    app.run()  
