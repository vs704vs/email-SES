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










CREATE PROCEDURE [dbo].[alimIHMDOLArrete]
    @value nvarchar(20),
    @annee nvarchar(4),
    @sql_output nvarchar(2000) OUTPUT
AS
BEGIN
    DECLARE @TEMPS_DATE DATE = DATEADD(month, -12, GETDATE())
    DECLARE @i int = 0
    DECLARE @currentYear int = YEAR(GETDATE())
    DECLARE @tablecpt TABLE(val nvarchar(10))
    DECLARE @tablearrete TABLE(val nvarchar(10))

    -- Original logic
    IF @value = 'COMPARE'
    BEGIN
        INSERT INTO @tablearrete
        SELECT Dt_inventaire FROM [ADM].[arrete] ORDER BY Dt_inventaire ASC

        -- Step 1: Add dates within 3 months of the current date
        WHILE @i < 60
        BEGIN
            DECLARE @calculatedDate DATE = DATEADD(month, @i, @TEMPS_DATE)

            -- Check if date is within 3 months of current date
            IF @calculatedDate <= DATEADD(month, 3, GETDATE())
            BEGIN
                INSERT INTO @tablecpt
                SELECT @calculatedDate AS Dt_inventaire
            END

            SET @i = @i + 1
        END

        -- Step 2: Add quarterly dates for the next year
        DECLARE @nextYear int = @currentYear + 1
        INSERT INTO @tablecpt
        SELECT DATEFROMPARTS(@nextYear, 3, 31) AS Dt_inventaire  -- Q1 End
        UNION ALL
        SELECT DATEFROMPARTS(@nextYear, 6, 30)  -- Q2 End
        UNION ALL
        SELECT DATEFROMPARTS(@nextYear, 9, 30)  -- Q3 End
        UNION ALL
        SELECT DATEFROMPARTS(@nextYear, 12, 31)  -- Q4 End

        -- Step 3: Add year-end dates for the next five years
        DECLARE @yearCounter int = 1
        WHILE @yearCounter <= 5
        BEGIN
            DECLARE @yearEndDate DATE = DATEFROMPARTS(@currentYear + @yearCounter, 12, 31)
            INSERT INTO @tablecpt
            SELECT @yearEndDate AS Dt_inventaire

            SET @yearCounter = @yearCounter + 1
        END

        -- Final Step: Return the dates that are in @tablecpt but not in @tablearrete
        SELECT CONVERT(nvarchar, CONVERT(date, val)) AS Dt_inventaire 
        FROM @tablecpt
        EXCEPT
        SELECT CONVERT(nvarchar, CONVERT(date, val)) AS Dt_inventaire 
        FROM @tablearrete
    END

    -- Original ELSE condition logic here (unchanged)
END
