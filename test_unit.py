import unittest
from unittest.mock import patch, MagicMock
from startstopec2 import lambda_handler, get_ec2_instances, start_instance, stop_instance

class TestAWSStartStop(unittest.TestCase):

    @patch('startstopec2.get_ec2_instances')
    def test_lambda_handler(self, mock_get_ec2_instances):
        # Mock instances
        mock_instance_stopped = MagicMock()
        mock_instance_stopped.state = {'Name': 'stopped'}
        mock_instance_stopped.id = 'i-stopped'

        mock_instance_running = MagicMock()
        mock_instance_running.state = {'Name': 'running'}
        mock_instance_running.id = 'i-running'

        mock_get_ec2_instances.return_value = [mock_instance_stopped, mock_instance_running]

        with patch('startstopec2.start_instance') as mock_start_instance, \
             patch('startstopec2.stop_instance') as mock_stop_instance:

            lambda_handler(None, None)

            # Assert start_instance was called for stopped instance
            mock_start_instance.assert_called_once_with(mock_instance_stopped)

            # Assert stop_instance was called for running instance
            mock_stop_instance.assert_called_once_with(mock_instance_running)

    @patch('startstopec2.boto3.resource')
    def test_get_ec2_instances(self, mock_boto3_resource):
        mock_ec2 = MagicMock()
        mock_instances = mock_ec2.instances.filter.return_value
        mock_boto3_resource.return_value = mock_ec2

        instances = get_ec2_instances('test-key', 'test-value')

        mock_ec2.instances.filter.assert_called_once_with(
            Filters=[{'Name': 'tag:test-key', 'Values': ['test-value']}]
        )
        self.assertEqual(instances, mock_instances)

    def test_start_instance(self):
        mock_instance = MagicMock()
        mock_instance.id = 'i-1234567890abcdef0'

        with patch('builtins.print') as mock_print:
            start_instance(mock_instance)

            mock_instance.start.assert_called_once()
            mock_print.assert_called_once_with('Started instance: i-1234567890abcdef0')

    def test_stop_instance(self):
        mock_instance = MagicMock()
        mock_instance.id = 'i-1234567890abcdef0'

        with patch('builtins.print') as mock_print:
            stop_instance(mock_instance)

            mock_instance.stop.assert_called_once()
            mock_print.assert_called_once_with('Stopped instance: i-1234567890abcdef0')

if __name__ == '__main__':
    unittest.main()