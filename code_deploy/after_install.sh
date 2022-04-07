# cd /home/ec2-user/webservice/

# source newenv/bin/activate

# python3 manage.py test

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/home/ec2-user/webservice/cloudwatch-config.json -s
sudo systemctl start amazon-cloudwatch-agent.service