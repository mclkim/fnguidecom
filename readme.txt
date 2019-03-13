# How to Install Python 3.6.4 on CentOS 7

https://www.rosehosting.com/blog/how-to-install-python-3-6-4-on-centos-7/
```
sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
sudo yum update
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
python3.6 -V
```

# FnguideCom
```
git clone https://github.com/mclkim/fnguidecom.git
cd fnguidecom
python3.6 -m venv venv
(혹은)
$ python3 -m virtualenv venv 
$ virtualenv venv --python=python3.6

. ./venv/bin/activate

python setup.py install
cd api
python __main__.py
```

# pip freeze
```
beautifulsoup4==4.6.0
bs4==0.0.1
certifi==2018.4.16
chardet==3.0.4
et-xmlfile==1.0.1
idna==2.7
jdcal==1.4
numpy==1.15.0rc2
openpyxl==2.5.4
pandas==0.23.3
python-dateutil==2.7.3
pytz==2018.5
requests==2.19.1
six==1.11.0
tqdm==4.23.4
urllib3==1.23
```

# 주기적 크롤링 (crontab 등록)
```bash
# 매일23시13분 
13 23 * * * /home/mclkim/fnguidecom/api/__main__.py
```

https://askubuntu.com/questions/855901/install-pandas-to-python3-5-instead-of-2-7
