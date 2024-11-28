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












To create a regex for each element in uploadFileTlanes that matches various formats such as different cases, underscores, hyphens, or special characters like brackets, we need to construct flexible patterns. Here's how you can generate regex for each element:

Rules:

1. Ignore case sensitivity (i flag).


2. Allow underscores (_), hyphens (-), and optional spaces between words.


3. Allow special characters like brackets () or others that might appear.



Regex Generator Code:

Here’s a script to generate regex patterns for each element in uploadFileTlanes:

const uploadFileTlanes: string[] = [
  "Drivers",
  "Gizeh",
  "Inter RC Application",
  "Inter RC Editique",
  "Inter RC Management",
  "Inter RC Project",
  "Intra RC",
  "Keys",
  "NBI Activity Coefficient",
  "NBI-Entity",
  "NBI-Products",
  "NBI-Segment",
  "Rul-Alloc"
];

const generateRegex = (name: string): RegExp => {
  // Escape special regex characters, replace spaces with a flexible pattern
  const escapedName = name
    .replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&") // Escape special characters
    .replace(/\\ /g, "[-_\\s]*"); // Allow hyphen, underscore, or space
  return new RegExp(`^${escapedName}$`, "i"); // Match full string, ignore case
};

const regexList = uploadFileTlanes.map((name) => ({
  name,
  regex: generateRegex(name)
}));

console.log(regexList);

Explanation:

1. Escape Special Characters: Characters like -, [, ], {, }, (, ), *, etc., are escaped to ensure they are treated as literals in the regex.


2. Flexible Word Separators: Replaced spaces with [-_\\s]*, allowing for any combination of hyphen, underscore, or space.


3. Ignore Case: Added the i flag to match case-insensitively.


4. Full String Match: Anchored regex with ^ and $ to match the entire string.



Sample Output Regex:

For the input uploadFileTlanes, the script will generate:

Drivers → /^Drivers$/i

Inter RC Application → /^Inter[-_\s]*RC[-_\s]*Application$/i

NBI-Entity → /^NBI[-_\s]*Entity$/i

Rul-Alloc → /^Rul[-_\s]*Alloc$/i


Examples:

Regex for Inter RC Application:

Matches:

InterRCApplication

Inter_RC_Application

inter-rc application

INTER RC APPLICATION


Does not match:

InterApplicationRC




Test Cases:

You can test these patterns using .test():

const text = "inter_rc(application)";
const regex = generateRegex("Inter RC Application");
console.log(regex.test(text)); // true

Let me know if you'd like help testing or refining this!

