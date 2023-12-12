import requests
import json
from app.utils.email import EmailConstants


class CreateEmail:
    @staticmethod
    def send_email(to_email: str, subject: str = 'Hey', text_content: str = 'Test email'):
        url = EmailConstants.URL
        payload = json.dumps(
            {
                "sender": {"name": EmailConstants.FROM_NAME, "email": EmailConstants.FROM_ADDR},
                "to": [{"email": f"{to_email}"}],
                "subject": subject,
                "textContent": text_content,
            }
        )
        headers = {
            "accept": "application/json",
            "api-key": EmailConstants.API_KEY,
            "content-type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        return response
