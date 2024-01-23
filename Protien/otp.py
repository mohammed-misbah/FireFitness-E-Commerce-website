#======SINCH-OTP Validation======#

import requests

def send_request(phonenumber):
  # print("in otp",phonenumber)
  url = "https://verificationapi-v1.sinch.com/verification/v1/verifications"
  payload="{\n  \"identity\": {\n  \"type\": \"number\",\n  \"endpoint\": \"+91"+format(phonenumber)+"\"\n  },\n  \"method\": \"sms\"\n}"
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic MGI1OTQ5NjItMzEzNi00MmJlLTkwNmMtZTBkMTg1NTViMTRjOmZ0aXRMN1p1cUVpa0pMMGtXbjMxVFE9PQ==',
    'Accept-Language': 'en-US'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  print(response)
  try:
    response
  except:
    messages = None
  messages = True
  return messages


def verify_Otp(OTP, phonenumber):
  url = "https://verificationapi-v1.sinch.com/verification/v1/verifications/number/+91"+phonenumber
  payload="{ \"method\": \"sms\", \"sms\":{ \"code\": \""+format(OTP)+"\"}}"
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic MGI1OTQ5NjItMzEzNi00MmJlLTkwNmMtZTBkMTg1NTViMTRjOmZ0aXRMN1p1cUVpa0pMMGtXbjMxVFE9PQ=='
  }
  response = requests.request("PUT", url, headers=headers, data=payload)

  res = response.json()
  print(res)
  try:
    if res['message'] == 'Invalid identity or code.':
      response = None
  except:
    response = True
  else:
    response = None  
  return response    
 
