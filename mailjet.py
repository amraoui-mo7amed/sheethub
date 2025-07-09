from mailjet_rest import Client
from decouple import config 

class MailJet:
    def __init__(self) -> None:
        self.api_key = config('MJ_API_KEY')
        self.api_secret = config('MJ_SECRET_KEY')
        self.client = Client(auth=(self.api_key, self.api_secret), version='v3.1')
        self.from_email = config('DEFAULT_FROM_EMAIL')
        self.from_name = config('DEFAULT_FROM_NAME')
        self.account_activation_templateID = int(config('ACCOUNT_ACTIVATION_TEMPLATEID'))
    def sendMessage(self, templateID: int, subject: str ,recipiant_email : str ,recipiant_name : str, variabels: dict):
        data = {
        'Messages': [
                        {
                                "From": {
                                        "Email": self.from_email,
                                        "Name": self.from_name
                                },
                                "To": [
                                        {
                                                "Email": recipiant_email,
                                                "Name": recipiant_name
                                        }
                                ],
                                "TemplateID": templateID,
                                "TemplateLanguage": True,
                                "Subject": str(subject)
                        }
                ]
        }
        if variabels:
            data['Messages'][0]['Variables'] = variabels
        
        try:
            result = self.client.send.create(data=data)
            response_json = result.json()
            print(response_json)
            status = response_json.get("Messages", [{}])[0].get("Status")
            message_id = response_json.get("Messages", [{}])[0].get("To", [{}])[0].get("MessageID")
            if result.status_code == 200 and status == "success":
                return True, status
            else:
                return False, response_json
            
        except Exception as e:
            return False, str(e)
