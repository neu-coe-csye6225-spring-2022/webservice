#python3 manage.py test

cd /home/ec2-user/webservice/

source newenv/bin/activate

# Since the god-damn CentOS cannot use sudo to start Django service directly on port 80
# An alternative solution is to redirect port 80 to 8080 and run web service on port 8080
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080

IPV4_ADDR=$(host myip.opendns.com resolver1.opendns.com | grep "myip.opendns.com has" | awk '{print $4}')
IPV4_ADDR=$(echo "$IPV4_ADDR" | sed "s/\./-/g")
IPV4_DNS=ec2-"$IPV4_ADDR".compute-1.amazonaws.com

python3 manage.py migrate
echo | nohup python3 -u manage.py runserver "$IPV4_DNS":8080 &
#python3 manage.py runserver "$IPV4_DNS":8080 &