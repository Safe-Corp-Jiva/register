"""
Users

This module contains classes for type annotations and data validation for the User entity.
It also contains the User class which is used to create a user in the Amazon Connect service.

The create method requires a boto3 client to interact with the Amazon Connect service:
  This facilitates testing as it allows the use of a mock client if desired.

Joaquin Badillo
2024-04-14
"""

from typing import Optional, TypedDict

required_fields = (
  "Username",
  "Password",
  "PhoneConfig",
  "SecurityProfileIds",
  "RoutingProfileId"
)

class IdentityInfo(TypedDict):
  FirstName: Optional[str]
  LastName: Optional[str]
  Email: Optional[str]
  SecondaryEmail: Optional[str]
  Mobile: Optional[str]

class PhoneConfig(TypedDict):
  PhoneType: str
  AutoAccept: Optional[bool]
  AfterContactWorkTimeLimit: Optional[int]
  DeskPhoneNumber: Optional[str]

class UserData(TypedDict):
  UserId: str
  UserArn: str

class UserCreatedResponse:
  data: Optional["UserData"]
  error: Optional[str]

class User:
  Username: str
  Password: str
  IdentityInfo: Optional["IdentityInfo"]
  PhoneConfig: "PhoneConfig"
  DirectoryUserId: Optional[str]
  SecurityProfileIds: list[str]
  RoutingProfileId: list[str]
  InstanceId: str

  def __init__(
    self, 
    Username: str, 
    Password: str,
    PhoneConfig: "PhoneConfig",
    InstanceId: str,
    SecurityProfileIds: list[str],
    RoutingProfileId: str,
    IdentityInfo: Optional["IdentityInfo"] = None
  ):
    # Required Fields
    self.Username = Username
    self.Password = Password
    self.PhoneConfig = PhoneConfig
    self.InstanceId = InstanceId
    self.SecurityProfileIds = SecurityProfileIds
    self.RoutingProfileId = RoutingProfileId

    # Optional Fields
    self.IdentityInfo = IdentityInfo

  def create(self, client) -> UserCreatedResponse:
    response = {
      "data": None,
      "error": None
    }

    try:
      response["data"] = client.create_user(
        Username=self.Username,
        Password=self.Password,
        IdentityInfo=self.IdentityInfo,
        PhoneConfig=self.PhoneConfig,
        SecurityProfileIds=self.SecurityProfileIds,
        RoutingProfileId=self.RoutingProfileId,
        InstanceId=self.InstanceId,
      )
    except Exception as e:
      response["error"] = str(e)
      return response
      
    return response