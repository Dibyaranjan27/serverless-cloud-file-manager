<h1 align="center">☁️ Serverless Cloud File Manager ☁️</h1>

<p align="center">
  A comprehensive Cloud Computing project implementing an enterprise-grade, event-driven serverless architecture locally — featuring Amazon S3, AWS Lambda, DynamoDB, and a custom Flask frontend.
</p>

<div align="center">
  <img src="https://img.shields.io/badge/Python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/AWS-Serverless-orange?style=for-the-badge&logo=amazon-aws" alt="AWS"/>
  <img src="https://img.shields.io/badge/Docker-passing-brightgreen?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
</div>

---

## 📖 Table of Contents
- [The Story Behind This Project](#-the-story-behind-this-project)
- [Cloud Concepts Demonstrated](#-cloud-concepts-demonstrated)
- [Key Features](#-key-features)
- [Architecture Analysis](#-architecture-analysis)
- [Tech Stack](#-tech-stack)
- [Installation and Usage](#-installation-and-usage)
- [File Structure](#-file-structure)
- [Security Best Practices](#-security-best-practices)
- [Contribution](#-contribution)
- [Screenshots](#-screenshots)
- [License](#-license)
- [Author](#-author)

---

## 📜 The Story Behind This Project

This project was built for a 4th semester Cloud Computing college syllabus.

Instead of relying on expensive, real-world AWS accounts that require credit cards and run the risk of unexpected billing charges, I decided to build a **fully simulated, enterprise-grade cloud architecture entirely locally and for free.** 

Using **LocalStack** and **Docker**, this project proves a genuine understanding of modern cloud computing by successfully integrating asynchronous microservices, NoSQL databases, and event-driven computing pipelines without ever touching the public internet.

If you find this helpful for your own Cloud Computing studies, feel free to drop a **star ⭐** or **fork it 🍴**!

---

## 📚 Cloud Concepts Demonstrated

| Concept | Where It's Used |
|---|---|
| **Serverless Compute** | AWS Lambda automatically extracts metadata in the background without provisioning servers |
| **Event-Driven Architecture** | S3 `s3:ObjectCreated:*` events automatically trigger the Lambda pipeline |
| **Object Storage** | Uploaded files are streamed directly into an Amazon S3 bucket |
| **NoSQL Databases** | Amazon DynamoDB stores the extracted file metadata for fast retrieval |
| **Containerization** | The entire multi-service stack is orchestrated using Docker Compose |

---

## 📌 Key Features

- ☁️ **Full Local AWS Simulation** — Zero cloud costs, runs completely offline.
- 📁 **Batch Processing** — Select and upload dozens of files simultaneously.
- ⚡ **Asynchronous Extraction** — Background Lambda functions handle processing to keep the UI fast.
- 🔍 **Instant Search** — Real-time client-side search filtering for massive file lists.
- 📱 **Mobile Responsive** — Custom stacked-card layout for viewing files on small screens.
- ⬇️ **Direct Downloads** — Stream your uploaded files back directly from S3.
- 🎨 **Glassmorphism UI** — Beautiful, modern frontend design.

---

## 🏗️ Architecture Analysis

<div align="center">
  <img src="docs/img/architecture_diagram.png" alt="Architecture Diagram" width="100%" style="border-radius: 8px; margin-bottom: 20px;" />
</div>

The data pipeline follows a strict, decoupled, asynchronous flow:

1. **Upload**: The Flask app acts solely as an API gateway, streaming the binary file into S3.
2. **Event**: S3 fires an `ObjectCreated` event containing the file's Amazon Resource Name (ARN).
3. **Compute**: Lambda boots up instantly, parses the event, retrieves the file size and timestamp, and formats it.
4. **Database**: Lambda writes a new record into DynamoDB.
5. **Retrieval**: When the user requests the page, Flask runs a quick table scan on DynamoDB to render the UI.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.9, Flask, Boto3 (AWS SDK)
- **Frontend:** HTML5, CSS3, Vanilla JS, Jinja2
- **Infrastructure:** LocalStack, Docker, Docker Compose
- **Simulated Cloud Services:** AWS S3, AWS Lambda, AWS DynamoDB

---

## 🚀 Installation and Usage

### **1. Clone the Repository**
```sh
git clone https://github.com/Dibyaranjan27/cloud-file-manager.git
cd cloud-file-manager
```

### **2. Start the Environment**
You must have Docker and Docker Compose installed.
```sh
docker-compose up -d
```
*Note: On the very first run, LocalStack will take a moment to initialize the S3 buckets and Lambda functions.*

### **3. Access the Application**
Open your browser and navigate to:
```text
http://localhost:5000
```

### **4. Stop the Environment**
```sh
docker-compose down
```

---

## 📂 File Structure

```text
/cloud-file-manager
│
├── app/
│   ├── app.py              # Flask Web Application backend
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Builds the web application container
│   ├── static/
│   │   ├── style.css       # Glassmorphism & responsive CSS
│   │   ├── main.js         # Client-side search and UI logic
│   │   └── background.jpg  # UI background image
│   └── templates/
│       └── index.html      # Jinja2 frontend template
│
├── lambda/
│   └── process_file.py     # Serverless AWS Lambda function
│
├── docker-compose.yml      # Multi-container orchestration (Web + LocalStack)
├── init-aws.sh             # Bootstraps S3, Lambda, and DynamoDB on startup
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## 🛡️ Security Best Practices

- **NoSQL Injection Proof:** DynamoDB is used instead of SQL, entirely neutralizing SQL injection attacks.
- **Path Traversal Protection:** Implements `werkzeug.utils.secure_filename()` on all upload and download routes to prevent directory traversal exploits.
- **XSS Prevention:** Flask's Jinja2 templating engine automatically escapes all user-provided file names before rendering them in the HTML table.

---

## 🤝 Contribution

Feel free to contribute to this project! Fork the repository, make your improvements, and submit a pull request. All contributions are welcome.

If you have any questions or suggestions, feel free to contact me. I'd be happy to help! 😊

---

## 🖥️ Screenshots

<details>
<summary><b>Click to view Screenshots! 📸</b></summary>

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://images.unsplash.com/photo-1614064641913-a53b53c126d9?q=80&w=600&auto=format&fit=crop" alt="HOMEPAGE DASHBOARD" width="400">
        <br/>
        <em>HOMEPAGE DASHBOARD</em>
      </td>
      <td align="center">
        <img src="https://images.unsplash.com/photo-1555421689-491a97ff2040?q=80&w=600&auto=format&fit=crop" alt="MOBILE RESPONSIVE VIEW" width="400">
        <br/>
        <em>MOBILE RESPONSIVE VIEW</em>
      </td>
    </tr>
  </table>
</div>

*(Note: Replace the image `src` URLs in `README.md` with your actual local screenshot paths once you take them!)*

</details>

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 💡 Author

<p align="center">
<em>Crafted with pixels & passion by</em>
<br>
<strong>Dibyaranjan Maharana</strong>
<br>
<a href="https://github.com/Dibyaranjan27">GitHub</a> | <a href="https://www.linkedin.com/in/dibyaranjan-maharana-1228012b2/">LinkedIn</a>
</p>
