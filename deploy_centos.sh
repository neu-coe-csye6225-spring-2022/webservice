cd /home/ec2-user/
mkdir webservice
cp /tmp/webservice.zip /home/ec2-user/webservice/webservice.zip

sudo yum install unzip -y

cd webservice
unzip webservice.zip
ls -al


#DB_PW="abc12345"
#
## Install & Setup MySQL
#sudo yum install https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm -y
sudo yum update -y
sudo amazon-linux-extras install epel -y
#sudo rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
#sudo yum install mysql-community-server -y
#sudo systemctl enable --now mysqld
#
#TEMP_PW=$(sudo grep 'temporary password' /var/log/mysqld.log)
#PATTERN="root@localhost: "
#TEMP_PW=${TEMP_PW#*$PATTERN}
#echo $TEMP_PW
#
#sudo sed -i 's/127\.0\.0\.1/0\.0\.0\.0/g' /etc/my.cnf
#mysql -u root --connect-expired-password --password="$TEMP_PW" <<-EOF
#ALTER USER 'root'@'localhost' IDENTIFIED BY 'amazon-linux-2-Yiqing@';
#flush privileges;
#UNINSTALL COMPONENT 'file://component_validate_password';
#ALTER USER 'root'@'localhost' IDENTIFIED BY '$DB_PW';
#flush privileges;
#EOF
#
#mysql -u root --password="$DB_PW" -e 'USE mysql; UPDATE `user` SET `Host`="%" WHERE `User`="root" AND `Host`="localhost"; DELETE FROM `user` WHERE `Host` != "%" AND `User`="root"; FLUSH PRIVILEGES; CREATE DATABASE webservice_db;'
#
#sudo service mysqld restart


# Install AWS CodeDeploy
CODEDEPLOY_BIN="/opt/codedeploy-agent/bin/codedeploy-agent"
$CODEDEPLOY_BIN stop
sudo yum erase codedeploy-agent -y

sudo yum install ruby wget -y
cd /home/ec2-user
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent status

# Install python3 dev & necessary packages in virtual env
sudo yum group install "Development Tools" -y
export CFLAGS="-std=c99"
sudo yum install python3-devel mysql-devel -y

sudo pip3 install virtualenv

cd /home/ec2-user/webservice
virtualenv newenv
source newenv/bin/activate
pip3 install pytest django djangorestframework bcrypt mysqlclient boto3 django-storages django-s3direct


# Automatically start web service after login
crontab -l > mycron
echo "@reboot sh /home/ec2-user/webservice/start_webservice_centos.sh" >> mycron
crontab mycron
rm mycron

# Start webservice
#./start_webservice_centos.sh
#sudo reboot
#sudo systemctl restart crond.service