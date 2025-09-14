import smtplib

FROM = "coolguy81@email.xzy"
TO = ["user1@localhost"]
SUBJECT = input("Subject (Check This Out): ")
BODY = input("Body (Demo): ")

if len(SUBJECT) == 0:
    SUBJECT = "Check This Out"
if len(BODY) == 0:
    BODY = "Look at this super cool thing we built!!"

message = f"""\
From: {FROM}
To: {', '.join(TO)}
Subject: {SUBJECT}

{BODY}
"""

print("\033[94mConnecting to SMTP server at 35.231.167.204:1026...\033[0m")
with smtplib.SMTP("35.231.167.204", 1026) as server:
    print(f"\033[92mConnected. Sending email from {FROM} to {', '.join(TO)}...\033[0m")
    server.sendmail(FROM, TO, message)
    print("\033[93mEmail sent successfully!\033[0m")

