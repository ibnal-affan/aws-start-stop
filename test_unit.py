import unittest
from unittest.mock import patch, MagicMock
from test import lambda_handler, get_ec2_instances

class TestAWSStartStop(unittest.TestCase):

    @patch('test.get_ec2_instances')
    def test_lambda_handler(self, mock_get_ec2_instances):
        # Mock instances
        mock_instance_stopped = MagicMock()
        mock_instance_stopped.state = {'Name': 'stopped'}
        mock_instance_stopped.id = 'i-stopped'

        mock_instance_running = MagicMock()
        mock_instance_running.state = {'Name': 'running'}
        mock_instance_running.id = 'i-running'

        mock_get_ec2_instances.return_value = [mock_instance_stopped, mock_instance_running]

        with patch('test.start_instance') as mock_start_instance, \
             patch('test.stop_instance') as mock_stop_instance:

            lambda_handler(None, None)

            # Assert start_instance was called for stopped instance
            mock_start_instance.assert_called_once_with(mock_instance_stopped)

            # Assert stop_instance was called for running instance
            mock_stop_instance.assert_called_once_with(mock_instance_running)

if __name__ == '__main__':
    unittest.main()