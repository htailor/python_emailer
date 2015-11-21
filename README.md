# Python Email Wrapper

A simple python class for sending emails.

Key features
-------------

1. Simple way of sending emails.
2. Add multiple attachments.
2. Add compression(zip) to attached files.

Sending an Email
----------------

```python
from emailer import Email

subject = "Email Test"
sender = "a@b.com"
recipients = "b@c.com", "c@d.com"
message = "This is just a test message"

e = Email(sender, recipients, subject, message)
e.send()
```

Sending an Email with attachments
---------------------------------

```python
from emailer import EmailAttachment

subject = "Email Attachment Test"
sender = "a@b.com"
recipients = "b@c.com", "c@d.com"
message = "This is just a test message"
files = "file1", "file2"

e = EmailAttachment(sender, recipients, subject, message, files)
e.send()
```
With compression:

```python
from emailer import EmailAttachment

subject = "Email Attachment Test"
sender = "a@b.com"
recipients = "b@c.com", "c@d.com"
message = "This is just a test message"
files = "file1", "file2"

e = EmailAttachment(sender, recipients, subject, message, files)
e.compress()
e.send()
```
