import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Email details
# Email details
sender_email = ""
receiver_email = ""
subject = ""
smtp_server = ""
smtp_port = 0
smtp_username = ""
smtp_password = ""

# Create a multipart message
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject

# HTML content with inline image
html_content = """
<html>
<body>
<p>This is an example email with an inline image:</p>
<img src="cid:image1" alt="Inline Image">
<p>This is the inline image embedded in the email.</p>
</body>
</html>
"""
msg.attach(MIMEText(html_content, "html"))

# Attach the image
with open("image.png", "rb") as img_file:
    img = MIMEImage(img_file.read())
    img.add_header("Content-ID", "<image1>")
    msg.attach(img)

# Send the email
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(msg)

print("Email sent successfully")









https://www.urlshort.dev/
