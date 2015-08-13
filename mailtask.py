import taskfs

class MailTask:
    def __init__(self,sender,recipients,subject,body,scheduledTime,replyto='',bcc=tuple()):
        if bcc is None:
            bcc = tuple()
        if replyto is None:
            replyto = ''
        self.sender = str(sender)
        self.replyto = str(replyto)             # Reply-To address
        self.recipients = tuple(recipients)     # List of recipient addresses
        self.bcc = tuple(bcc)                   # Blind-copy recipients
        self.subject = str(subject)
        self.body = str(body)                   # Body of the message
        self.scheduledTime = int(scheduledTime) # When the task should occur, Unix timestamp

    def __str__(self):
        return taskfs.md5Task(self)

    def __eq__(self,other):
        return str(self) == str(other)

    def __ne__(self,other):
        return str(self) != str(other)

    def __hash__(self):
        return hash(self.sender)^\
                hash(self.replyto)^\
                hash(self.recipients)^\
                hash(self.bcc) ^\
                hash(self.subject)^\
                hash(self.body)^\
                hash(self.scheduledTime)
