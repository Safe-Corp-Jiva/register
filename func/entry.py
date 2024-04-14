"""
Amazon Connect User Registration Lambda.
 Creates a user in Amazon Connect.
 Requires environment variables:
 * AWS_ACCESS_KEY_ID
 * AWS_SECRET_ACCESS_KEY
 * AWS_DEFAULT_REGION
 * CONNECT_ARN
 
Joaquin Badillo
2024-04-14
"""


import os
from typing import Any, Dict

import boto3

from service.users import User, required_fields

TEST = os.environ.get("TEST")

def handle_error(msg):
  if TEST: return { "error": msg }
  else: raise Exception(msg)

def handler(event: Dict[str, Any], context):
  for field in required_fields:
    if field not in event:
      return handle_error(f"Missing required field: {field}")
  
  if event["PhoneConfig"].get("PhoneType") not in ["SOFT_PHONE", "DESK_PHONE"]:
    return handle_error("Invalid PhoneType")

  session = boto3.Session(
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
  )

  client = session.client('connect')

  security_profile_ids = {
    profile["Name"]: profile["Id"]
    for profile in client.list_security_profiles(
      InstanceId=os.environ.get('CONNECT_ARN'),
      MaxResults=5
    ).get("SecurityProfileSummaryList", [])
  }

  routing_profile_ids = {
    profile["Name"]: profile["Id"]
    for profile in client.list_routing_profiles(
      InstanceId=os.environ.get('CONNECT_ARN'),
      MaxResults=5
    ).get("RoutingProfileSummaryList", [])
  }

  user = User(
    Username=event["Username"],
    Password=event["Password"],
    PhoneConfig=event["PhoneConfig"],
    InstanceId=os.environ.get('CONNECT_ARN'),
    SecurityProfileIds=[security_profile_ids[profile] for profile in event["SecurityProfileIds"]],
    RoutingProfileId=routing_profile_ids[event["RoutingProfileId"]],
    IdentityInfo=event.get("IdentityInfo")
  )

  create_response = user.create(client)

  if create_response["error"] != None:
    return handle_error(create_response["error"])
  
  return {
    "data": create_response["data"]
  }