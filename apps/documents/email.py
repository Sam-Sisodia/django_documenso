from email.mime.text import MIMEText
import os
import smtplib

sender_email = os.getenv("SENDER_EMAIL")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("EMAIL_PASSWORD")
    

def recipientsmail(request,document_links, subject, message):
    results = []
    base_url = f"{os.getenv('FE_SIGN_URL')}"
    for link in document_links:
        receiver_email = link["email"]
        token = link["token"]
        url = f"{base_url}{token}"
        note = f"\n\nNote: {link.get('note')}" if 'note' in link and link['note'] else ""
        email_body = f"{message}\n\nClick on the link to open the document: {url} \n\n{note}"
        msg = MIMEText(email_body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            results.append(link["id"])
        except Exception as e:
            results.append({"recipient": receiver_email, "status": f"Failed to send email: {e}"})
    print("token_id",results)
    return results

def send_otp_to_mail(email,otp):
    receiver_email = email
    message = f"Your varification Otp is \n\n{otp}"  
    email_body = f"{message}"
    msg = MIMEText(email_body)
    msg['Subject'] = "Email Verification"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email Send...",receiver_email)
        
    except Exception as e:
        {"recipient": receiver_email, "status": f"Failed to send email: {e}"}
   






# Get the dynamic host from the request object
# scheme = request.scheme  # 'http' or 'https'
# host = request.get_host()  # e.g., '127.0.0.1:8000'