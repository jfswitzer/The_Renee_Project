sudo apt-get update
sudo apt-get upgrade
sudo apt-get install gcc-multilib build-essential python3-dev git
sudo apt-get install python3
sudo apt install software-properties-common
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
wget https://www.python.org/ftp/python/3.8.9/Python-3.8.9.tgz
tar -xf Python-3.8.9.tgz
cd Python-3.8.9
./configure --enable-optimizations
make install
pip3 install -r requirements.txt


