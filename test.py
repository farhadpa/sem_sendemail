import unittest
from unittest.mock import patch, MagicMock
import smtplib
from main import send_email
import os

class TestSendEmailFunction(unittest.TestCase):
    test_password = os.getenv('email_password')

    @patch('smtplib.SMTP')
    def test_successful_email_sending(self, mock_smtp):
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance

        mock_request = MagicMock()
        mock_request.args.get.return_value = 'farhad.panahi@gmail.com'

        result, headers = send_email(mock_request)

        self.assertEqual(result['message'], 'Email sent successfully to farhad.panahi@gmail.com:')
        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
        self.assertEqual(headers['Access-Control-Allow-Methods'], 'GET')

        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with('semexample1@gmail.com', self.test_password)
        mock_smtp_instance.sendmail.assert_called_once_with('semexample1@gmail.com', 'farhad.panahi@gmail.com', '''Subject: Alert
    According to your attendance and activity you are likely to fail the course. Please contact your professor.''')
        mock_smtp_instance.quit.assert_called_once()

    @patch('smtplib.SMTP')
    def test_unsuccessful_email_sending(self, mock_smtp):
        mock_smtp_instance = MagicMock()
        mock_smtp_instance.login.side_effect = smtplib.SMTPAuthenticationError(535, 'Authentication failed')
        mock_smtp.return_value = mock_smtp_instance

        mock_request = MagicMock()
        mock_request.args.get.return_value = 'farhad.panahi@gmail.com'

        result, headers = send_email(mock_request)

        self.assertEqual(result['message'], "Email failed to send.(535, 'Authentication failed')")
        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
        self.assertEqual(headers['Access-Control-Allow-Methods'], 'GET')

        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with('semexample1@gmail.com', self.test_password)

    @patch('smtplib.SMTP')
    def test_exception_handling(self, mock_smtp):
        mock_smtp_instance = MagicMock()
        mock_smtp_instance.login.side_effect = Exception('Something went wrong')
        mock_smtp.return_value = mock_smtp_instance

        mock_request = MagicMock()
        mock_request.args.get.return_value = 'farhad.panahi@gmail.com'

        result, headers = send_email(mock_request)

        self.assertEqual(result['message'], 'Email failed to send.Something went wrong')
        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
        self.assertEqual(headers['Access-Control-Allow-Methods'], 'GET')

        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with('semexample1@gmail.com', self.test_password)

if __name__ == '__main__':
    unittest.main()
