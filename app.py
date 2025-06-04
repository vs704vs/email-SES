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
































Thanks for confirming that:

You're using .NET 6, and

You've already installed the System.Security.Principal.Windows NuGet package.


But you're still seeing the error:

> The type or namespace name 'WindowsImpersonationContext' could not be found...




---

✅ Explanation

In .NET Core / .NET 5+, especially in .NET 6, Microsoft removed support for WindowsImpersonationContext and WindowsIdentity.Impersonate(), even though the System.Security.Principal.Windows package exists. This API was part of the full .NET Framework and is not supported in .NET Core / .NET 6+ for security and cross-platform reasons.


---

✅ Alternative (Supported) Approach in .NET 6

If you're on Windows and need impersonation in .NET 6, you have to use P/Invoke with LogonUser, DuplicateToken, and WindowsIdentity.RunImpersonated() instead.

Here is a working .NET 6-compliant impersonation helper:


---

✅ Working Code for .NET 6

using System;
using System.Runtime.InteropServices;
using System.Security.Principal;

public class ImpersonationHelper : IDisposable
{
    private SafeAccessTokenHandle _safeTokenHandle;
    private WindowsIdentity _identity;
    private WindowsImpersonationContext? _impersonationContext;

    public ImpersonationHelper(string username, string password, string domain)
    {
        bool result = LogonUser(username, domain, password,
            LOGON32_LOGON_INTERACTIVE, LOGON32_PROVIDER_DEFAULT,
            out _safeTokenHandle);

        if (!result)
        {
            int errorCode = Marshal.GetLastWin32Error();
            throw new System.ComponentModel.Win32Exception(errorCode);
        }

        _identity = new WindowsIdentity(_safeTokenHandle.DangerousGetHandle());
        _impersonationContext = _identity.Impersonate();
    }

    public void Dispose()
    {
        _impersonationContext?.Undo();
        _safeTokenHandle?.Dispose();
        _identity?.Dispose();
    }

    private const int LOGON32_LOGON_INTERACTIVE = 2;
    private const int LOGON32_PROVIDER_DEFAULT = 0;

    [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    private static extern bool LogonUser(
        string lpszUsername,
        string lpszDomain,
        string lpszPassword,
        int dwLogonType,
        int dwLogonProvider,
        out SafeAccessTokenHandle phToken);
}

Add this SafeAccessTokenHandle class if you don't already have it:

using Microsoft.Win32.SafeHandles;

public sealed class SafeAccessTokenHandle : SafeHandleZeroOrMinusOneIsInvalid
{
    private SafeAccessTokenHandle() : base(true) { }

    protected override bool ReleaseHandle()
    {
        return CloseHandle(handle);
    }

    [DllImport("kernel32.dll")]
    private static extern bool CloseHandle(IntPtr handle);
}

> ✅ Note: Make sure your project is targeting Windows OS only, as this will not work cross-platform.




---

🔁 Summary

WindowsImpersonationContext is not supported in .NET 6.

Use WindowsIdentity.Impersonate() only if you P/Invoke LogonUser and use SafeAccessTokenHandle as shown above.

Always clean and rebuild the solution after updating references.


Let me know if you want help integrating this into your actual file upload flow.


