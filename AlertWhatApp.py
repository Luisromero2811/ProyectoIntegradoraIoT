from twilio.rest import Client

class MessageAlert:

    def sendMessage(self,msg):
        account_sid = 'ACed9ab5f34def5a13dec7d941f0b95226'
        auth_token = '34753c5ea1b70bcc67fc040598803b7f'
        try:
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_ ='whatsapp:+14155238886',
                body = msg,
                to = f'whatsapp:+5218715649223'
            )

            if message:
                print(client.sip)
        except:     
            print('ocurrio un error al enviar el mensaje')