import smtplib, email
from email.mime.text import MIMEText
from email.message import Message
import email.utils
import re
import time
import os
import traceback

SMTPSRV = "mail.fastquake.com"

#TODO: Maybe this doesn't need to be a class
class Mailer:
    def __init__(self):
        pass

    def send(self, sender, replyto, rcpts, bccs, subj, body, dryrun=False):
        """sender: Sender address
        replyto: Reply-To address
        rcpts: List containing recipient addresses
        bccs: List containing BCC recipient addresses
        subj: Subject
        body: Body
        dryrun: If True, write to file instead of sending message
        
        Addresses should be in the format "John Doe <jdoe@example.com>"
        No validation is performed!"""

        msg = MIMEText(body)
        msg['Date'] = email.utils.formatdate()
        msg['From'] = sender
        if replyto:
            msg['Reply-To'] = replyto
        msg['To'] = ', '.join(rcpts)
        msg['Subject'] = subj

        sender = email.utils.parseaddr(sender)[1]
        if not sender:
            return 2
        rcpts = [email.utils.parseaddr(rcpt)[1] for rcpt in rcpts]
        if bccs:
            bccs = [email.utils.parseaddr(bcc)[1] for bcc in bccs]
            rcpts.extend(bccs)

        if not dryrun:
            #smtp.connect()
            try:
                smtp = smtplib.SMTP(SMTPSRV)
                smtp.sendmail(sender,rcpts,msg.as_string())
                smtp.quit()
            except:
                traceback.print_exc()
                return 1
        else:
            if not os.path.exists("./dry/"):
                os.mkdir("./dry/")
            f = open("./dry/"+str(time.time()),'w')
            f.write(msg)
            f.close()
        return 0
