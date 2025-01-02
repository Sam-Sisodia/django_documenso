
# def recipientsmail(document_links,subject,message):
#     results = []  # List to store results for each email attempt

#     for link in document_links:
#         # Email details
#         sender_email = "sajal@example.com"
#         receiver_email = link.recipient
#         subject =    subject  if subject else  "Shared Documents" 
#         url = f'http://127.0.0.1:8000/api/sign-document/{link.token}'
#         user_message = message if message else ""
#         body = f"{user_message} Click on link to open the Document {url}"
       
#         # Set up the MIMEText object
#         msg = MIMEText(body)
#         msg['Subject'] = subject
#         msg['From'] = sender_email
#         msg['To'] = receiver_email.email

#         # SMTP server configuration (example with Gmail)
#         smtp_server = "smtp.gmail.com"
#         smtp_port = 587
#         smtp_user = "sajal89304@gmail.com"
#         smtp_password = os.getenv("EMAIL_PASSWORD")

#         try:
#             # Connect to SMTP server
#             with smtplib.SMTP(smtp_server, smtp_port) as server:
#                 server.starttls()  # Secure connection
#                 server.login(smtp_user, smtp_password)
#                 print("Sending email to:", receiver_email.email)
#                 server.sendmail(sender_email, receiver_email.email, msg.as_string())
#             results.append({"recipient": receiver_email.email, "status": "Email sent successfully"})
#         except Exception as e:

#             results.append({"recipient": receiver_email.email, "status": f"Failed to send email: {e}"})
   
#     return results  # Return results after sending all emails

        