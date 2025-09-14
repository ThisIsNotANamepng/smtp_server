import asyncio
from aiosmtpd.controller import Controller
from email import message_from_bytes
from email.policy import default
import pandas as pd
from io import BytesIO
import os
import json

email_passwords = {
    "administratorek@localhost": "admin_password",
    "user1@localhost": "user1_password",
    "user2@localhost": "user2_password"
}

class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        peer = session.peer
        mailfrom = envelope.mail_from
        rcpttos = envelope.rcpt_tos
        data = envelope.content

        print('Peer:', peer)
        print('Mail from:', mailfrom)
        print('Rcpt to:', rcpttos)

        msg = message_from_bytes(data, policy=default)

        # Prepare log entry as dict for JSON
        log_entry = {
            "peer": str(peer),
            "mail_from": mailfrom,
            "rcpt_to": rcpttos,
            "subject": msg.get('Subject', ''),
        }
        body = msg.get_body(preferencelist=('plain'))
        if body:
            log_entry["body"] = body.get_content()
        else:
            log_entry["body"] = None

        attachments = []
        for rcptto in rcpttos:
            if rcptto in email_passwords:
                log_entry["message_for"] = rcptto
                for part in msg.iter_attachments():
                    content_type = part.get_content_type()
                    if content_type == 'text/csv' or content_type == 'application/csv':
                        csv_data = part.get_payload(decode=True)
                        df = pd.read_csv(BytesIO(csv_data))
                        attachments.append({
                            "type": content_type,
                            "csv_shape": [df.shape[0], df.shape[1]]
                        })
                    else:
                        attachments.append({
                            "type": content_type,
                            "info": "ignored"})
            else:
                log_entry["unknown_recipient"] = rcptto
                log_entry["attachments"] = attachments
                with open('log.log', 'a') as f:
                    f.write(json.dumps(log_entry) + '\n')
                return '550 Unknown recipient'
        log_entry["attachments"] = attachments
        with open('log.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        return '250 Message accepted for delivery'

def run_server():
    # Clear log.log on startup
    with open('log.log', 'w') as f:
        f.write('')
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=1026)
    controller.start()

    print("SMTP server is running. Press Ctrl+C to stop.")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()

if __name__ == "__main__":
    run_server()
