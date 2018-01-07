# Install


## macOS Sierra 10.12

* Follow this page and you get environment. https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Mac-OSX
* Then, let's install python libraries with pip.

```
pip install pymssql pyodbc
```

## RedHat 6

* Follow this page first. https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-RHEL-or-Centos
* Before doing the bottom one, install python 3.6.

```
yum install zlib-devel openssl openssl-devel gcc-c++
curl -O 'https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz'
xz -dv Python-3.6.3.tar.xz
tar xf Python-3.6.3.tar
cd Python-3.6.3
./configure
make
sudo make install
sudo pip3 install pyodbc
# You may need to add "PATH" at env_keep and remove secure_path in sudoers to run pip as root.
```

Note that you can create database after login with `isql DSN user pass`.
