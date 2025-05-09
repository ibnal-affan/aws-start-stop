import boto3

def get_ec2_instances(tag_key, tag_value):
    ec2 = boto3.resource('ec2')
    return ec2.instances.filter(
        Filters=[{'Name': f'tag:{tag_key}', 'Values': [tag_value]}]
    )

def start_instance(instance):
    instance.start()
    print(f'Started instance: {instance.id}')

def stop_instance(instance):
    instance.stop()
    print(f'Stopped instance: {instance.id}')

def lambda_handler(event, context):
    instances = get_ec2_instances('auto-start-stop', 'yes')

    for instance in instances:
        state = instance.state['Name']
        if state == 'stopped':
            start_instance(instance)
        elif state == 'running':
            stop_instance(instance)
