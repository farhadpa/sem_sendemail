import functions_framework
import smtplib
import os

@functions_framework.http
def send_email(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    receiver_email_id = request.args.get('emailto')
    password = os.getenv('email_password')

    s = smtplib.SMTP('smtp.gmail.com', 587)
    sender_email_id = "semexample1@gmail.com"
    message = '''Subject: Alert
    According to your attendance and activity you are likely to fail the course. Please contact your professor.'''
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
    }
    try: 

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(sender_email_id, password)

        # sending the mail
        s.sendmail(sender_email_id, receiver_email_id, message)

        # terminating the session
        s.quit()

        message_text = "Email sent successfully to %s:" % receiver_email_id
        message = {"message": message_text}
        return (message, headers)
    except Exception as e:
        print(e)
        message_text = "Email failed to send." + str(e)
        message = {"message": message_text}
        return (message, headers)