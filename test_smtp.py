import smtplib

FROM = "sender@example.com"
TO = ["user1@localhost"]
SUBJECT = "You haven't seen this befire"
BODY = "Lol Jk you have."

message = f"""\
From: {FROM}
To: {', '.join(TO)}
Subject: {SUBJECT}

{BODY}
"""

with smtplib.SMTP("127.0.0.1", 1026) as server:
    server.sendmail(FROM, TO, message)
print("Test email sent.")
