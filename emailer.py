import zipfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import Encoders
from os.path import basename
from smtplib import SMTP


class Email(object):
    
    def __init__(self, subject, sender, recipients, message):
        self.subject = subject
        self.sender = sender
        self.recipients = recipients
        self.message = message
        self.msg = None

    def send(self):
        self.__generate_email__()
        self.msg["Subject"] = self.subject
        self.msg["From"] = self.sender
        self.msg["To"] = ",".join(self.recipients) if type(self.recipients) is list else self.recipients
        s = SMTP()
        s.connect()
        s.sendmail(self.sender, self.recipients, self.msg.as_string())

    def __generate_email__(self):
        self.msg = MIMEText(self.message)


class EmailAttachment(Email):
    
    def __init__(self, subject, sender, recipients, message, files):
        super(EmailAttachment, self).__init__(subject, sender, recipients, message)
        self.files = files
        
    def compress(self):
        zfiles = []
        for file in self.files:
            _zfile = file + ".zip"
            with zipfile.ZipFile(_zfile, "w", zipfile.DEFLATED) as _zipped_file:
                _zipped_file.write(file)
            zfiles.append(_zfile)
        self.files = zfiles

    def __attach_files__(self):
        if type(self.files) is not list:
            files = [self.files]
        # Allow overriding of file name when sending
        for file_name in files:
            if type(file_name) in (list, tuple):
                file_name, output_filename = file_name
            else:
                output_filename = basename(file_name)

            # Add the CSV as an attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(open(file_name, "rb").read())
            Encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment; filename='%s'" % output_filename)
            self.msg.attach(part)

    def __generate_email__(self):
        self.msg = MIMEMultipart()
        self.msg.attach(MIMEText(self.message))
        self.__attach_files__()


if __name__ == "__main__":

    subject = "Class Test"
    sender = ""
    recipients = ""
    message = "This is just a test"

    e = Email(subject, sender, recipients, message)
    e.send()
