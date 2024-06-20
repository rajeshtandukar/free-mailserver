# Free Mailserver Setup using Mailu
Automate the setup of an Free SMTP email server on a remote server from your local machine.
This repository provides python code to setting up a free SMTP mail server using [Mailu](https://mailu.io/). Mailu is a simple yet full-featured mail server as a set of Docker images.

## Prerequisites

- A CentOS server with Docker and Docker Compose installed
- A domain name for your mail server
- Basic knowledge of Docker and command-line operations

## Features

- Full SMTP, IMAP, and Webmail server
- Web-based administration interface
- Spam and virus filtering

## Installation Steps

```bash
git clone https://github.com/rajeshtandukar/free-mailserver.git
cd free-mailserver
python3  -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python script.py <hostname> <ip> <username> <password>
```
Replace '&lt;hostname&gt;', '&lt;ip&gt;', '&lt;username&gt;', and '&lt;password&gt;' with the appropriate values for your remote server. For example:
```bash
python script.py yourdomain.com 173.209.150.123 root  ber72ki#dre@#%~
```

## Installation Steps

After running the script, verify that your Mailu mail server is up and running by accessing it via your web browser 

- Webmail : [https://main.yourdomain.com/webmail/](https://test.mailu.io/webmail/)
- Admin UI : [https://mail.yourdomain.com/admin/](https://test.mailu.io/admin/)
