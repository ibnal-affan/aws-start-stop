import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:auto-start-stop', 'Values': ['yes']}]
    )

    for instance in instances:
        if instance.state['Name'] == 'stopped':
            instance.start()
            print(f'Started instance: {instance.id}')
        elif instance.state['Name'] == 'running':
            instance.stop()
            print(f'Stopped instance: {instance.id}')
