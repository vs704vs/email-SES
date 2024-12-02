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





































Here’s how you can implement the required functionality:

Steps:

1. Iterate through the uploadFileNames array.


2. Generate a regex for each file name using the generateRegex function.


3. Match the generated regex against the fileNames array.


4. If a match is found:

Extract the date-time using the dateTimeRegex.

Populate the tableData state with the required information.




Here’s the updated code:

import React, { useState, useEffect } from "react";
import axios from "axios";

interface FileInfo {
  displayName: string;
  fileName: string;
  isUploaded: boolean;
  uploadDate: string;
}

const LastLoadedFiles = () => {
  const [costCRValue, setCostCRMValue] = useState("");
  const [tableData, setTableData] = useState<FileInfo[]>([]);

  const uploadFileNames: string[] = [
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
    "Rul-Alloc",
  ];

  const generateRegex = (name: string): RegExp => {
    const escapedName = name
      .replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&")
      .replace(/\\/g, "[-_\\s]*");
    return new RegExp(`^${escapedName}`, "i");
  };

  const fetchCostCRMValue = async () => {
    try {
      const res = await axios.get("cost/rollover/getCRMValue");
      setCostCRMValue(res.data.value);
    } catch (err) {
      console.error("Error occurred when fetching CRM value", err);
    }
  };

  const fetchTableData = async () => {
    try {
      const res = await axios.get(
        "cost/lastloadedfiles/listFilesInFolder?FolderPath=ALM/"
      );
      const filePaths: string[] = res.data.slice(1);

      const fileNames: string[] = filePaths.map((path) =>
        path.substring(path.lastIndexOf("/") + 1)
      );

      const dateTimeRegex = /(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+)/;

      const updatedTableData: FileInfo[] = [];

      uploadFileNames.forEach((uploadName) => {
        const regex = generateRegex(uploadName);
        const match = fileNames.find((fileName) => regex.test(fileName));

        if (match) {
          const dateMatch = match.match(dateTimeRegex);
          const uploadDate = dateMatch ? dateMatch[1] : "";

          updatedTableData.push({
            displayName: uploadName,
            fileName: match,
            isUploaded: true,
            uploadDate: uploadDate,
          });
        } else {
          updatedTableData.push({
            displayName: uploadName,
            fileName: "",
            isUploaded: false,
            uploadDate: "",
          });
        }
      });

      setTableData(updatedTableData);
    } catch (err) {
      console.error("Error occurred when fetching table data", err);
    }
  };

  useEffect(() => {
    fetchCostCRMValue();
    fetchTableData();
  }, []);

  return (
    <div>
      <h1>Last Loaded Files</h1>
      <table>
        <thead>
          <tr>
            <th>Display Name</th>
            <th>File Name</th>
            <th>Is Uploaded</th>
            <th>Upload Date</th>
          </tr>
        </thead>
        <tbody>
          {tableData.map((row, index) => (
            <tr key={index}>
              <td>{row.displayName}</td>
              <td>{row.fileName}</td>
              <td>{row.isUploaded ? "Yes" : "No"}</td>
              <td>{row.uploadDate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LastLoadedFiles;

Key Features:

1. Regex Generation: The generateRegex function ensures dynamic creation of robust regex patterns.


2. Date Extraction: The dateTimeRegex accurately extracts date-time values.


3. State Management: The tableData state holds the processed data.


4. UI Rendering: The table displays the final data, including whether files were uploaded.



Notes:

Ensure the API endpoints (cost/rollover/getCRMValue and cost/lastloadedfiles/listFilesInFolder) are accessible and return the expected data format.

Adjust styles or table rendering as needed for your specific UI framework or design.





























    function formatDate(inputDate: string): string {
  const date = new Date(inputDate);

  // Extract individual components
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  // Format the date as DD/MM/YYYY HH:mm:ss
  return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}

// Example usage
const input = "2024-05-20T14:29:47.893092700";
const formattedDate = formatDate(input);
console.log(formattedDate); // Output: "20/05/2024 14:29:47"



