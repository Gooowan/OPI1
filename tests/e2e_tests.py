import unittest
import subprocess


class TestE2EUserTimeFunctions(unittest.TestCase):

    def test_e2e_totalUserMinutes(self):
        # Start the application as a subprocess
        process = subprocess.Popen(['python', '/Users/bunjee/PycharmProjects/OPI1/main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Simulate user input to check total minutes for a user and then exit
        user_id = 'sample_user'
        output, _ = process.communicate(input=f'5\\n{user_id}\\nexit\\n')

        # Just checking if the output contains the expected phrases. In a more detailed test, you might want to extract the minute count and validate it.
        self.assertIn("Total active time for user", output)
        self.assertIn("seconds", output)

    def test_e2e_averageUserTime(self):
        # Start the application as a subprocess
        process = subprocess.Popen(['python', '/Users/bunjee/PycharmProjects/OPI1/main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Simulate user input to check average user time and then exit
        user_id = 'sample_user'
        output, _ = process.communicate(input=f'6\\n{user_id}\\nexit\\n')

        # Just checking if the output contains the expected phrases. In a more detailed test, you might want to extract the average times and validate them.
        self.assertIn("Average daily active time", output)
        self.assertIn("Average weekly active time", output)

    def test_e2e_nearestOnlineTime(self):
        # Start the application as a subprocess
        process = subprocess.Popen(['python', '/Users/bunjee/PycharmProjects/OPI1/main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)

        # Simulate user input for the nearest online time feature and then exit
        user_id = 'sample_user'
        date = '2023-10-11T12:00:00'
        output, _ = process.communicate(input=f'en\\n2\\n{date}\\n{user_id}\\nexit\\n')

        # Just checking if the output contains the expected phrases. In a detailed test, you might want to validate the actual time.
        self.assertIn("wasUserOnline", output)

    def test_e2e_onlinePrediction(self):
        # Start the application as a subprocess
        process = subprocess.Popen(['python', '/Users/bunjee/PycharmProjects/OPI1/main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)

        # Simulate user input for the online prediction feature and then exit
        date = '2023-10-11T12:00:00'
        output, _ = process.communicate(input=f'en\\n3\\n{date}\\nexit\\n')

        # Just checking if the output contains the expected phrases. In a detailed test, you might want to validate the predicted number.
        self.assertIn("Predicted number of users online", output)

    def test_e2e_userPrediction(self):
        # Start the application as a subprocess
        process = subprocess.Popen(['python', '/Users/bunjee/PycharmProjects/OPI1/main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)

        # Simulate user input for the user prediction feature and then exit
        user_id = 'sample_user'
        date = '2023-10-11T12:00:00'
        tolerance = '0.5'
        output, _ = process.communicate(input=f'en\\n4\\n{date}\\n{user_id}\\n{tolerance}\\nexit\\n')

        # Just checking if the output contains the expected phrases. In a detailed test, you might want to validate the probability.
        self.assertIn("probability", output)

    def test_e2e_general_interaction(self):
        # Start the application as a subprocess
        process = subprocess.Popen(['python', '/Users/bunjee/PycharmProjects/OPI1/main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)

        # Simulate a sequence of invalid and valid user inputs and then exit
        # Adding a slight delay between inputs
        output, error_output = process.communicate(input='de\\nen\\n9\\nexit\\n',
                                                   timeout=10)  # Added timeout for safety

        # Check that the output contains expected phrases indicating successful interaction and error handling
        # Also, checking the error_output (stderr) for any unexpected messages
        self.assertIn("Invalid feature choice. Try again.", output, msg=f"Error output: {error_output}")


