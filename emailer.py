import zipfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import Encoders
from os.path import basename
from smtplib import SMTP


class Email(object):

    def __init__(self, sender, recipients, subject, message):
        self._sender = sender
        self._recipients = recipients
        self._subject = subject
        self._message = message
        self._msg = None

    def __str__(self):
        return ", ".join([sender, ", ".join(recipients), subject, message])

    @property
    def sender(self):
        return self._sender

    @property
    def recipients(self):
        return self._sender

    @property
    def subject(self):
        return self._subject

    @property
    def message(self):
        return self._message

    def send(self):
        self.__generate_email__()
        self._msg["Subject"] = self._subject
        self._msg["From"] = self._sender
        self._msg["To"] = ",".join(self._recipients) if type(self._recipients) is list else self._recipients
        s = SMTP()
        s.connect()
        s.sendmail(self._sender, self._recipients, self._msg.as_string())

    def __generate_email__(self):
        self._msg = MIMEText(self._message)


class EmailAttachment(Email):

    def __init__(self, sender, recipients, subject, message, files):
        super(EmailAttachment, self).__init__(sender, recipients, subject, message)
        self._files = files
        if type(self.files) is not list:
            self._files = [self._files]

    def __str__(self):
        return super(EmailAttachment, self).__str__() + ", " + ", ".join(files)

    @property
    def files(self):
        return self._files

    def compress(self):
        zfiles = []
        for file in self._files:
            _zfile = file.split(".")[0] + ".zip"
            with zipfile.ZipFile(_zfile, "w", zipfile.ZIP_DEFLATED) as _zipped_file:
                _zipped_file.write(file)
            zfiles.append(_zfile)
        self._files = zfiles

    def __attach_files__(self):
        for file_name in self._files:
            if type(file_name) in (list, tuple):
                file_name, output_filename = file_name
            else:
                output_filename = basename(file_name)

            # Add the file as an attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(open(file_name, "rb").read())
            Encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment; filename=%s" % output_filename)
            self._msg.attach(part)

    def __generate_email__(self):
        self._msg = MIMEMultipart()
        self._msg.attach(MIMEText(self._message))
        self.__attach_files__()


if __name__ == "__main__":

    subject = "Emailer Test"
    sender = "a@b.com"
    recipients = "b@c.com", "c@d.com"
    message = "This is just a test message"
    files = "file1", "file2"

    e = Email(sender, recipients, subject, message)
    print e
    # e.send()

    f = EmailAttachment(sender, recipients, subject, message, files)
    print f

    # test sending an email with attachment
    # e = EmailAttachment(subject, sender, recipients, message, files)
    # e.send()

    # test sending an email with a compressed attachment
    # e.compress()
    # e.send()
