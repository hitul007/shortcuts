sudo apt-get update
sudo apt-get install -y supervisor nginx

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
exec "$SHELL"

sudo apt-get -y install build-essential libncursesw5-dev libreadline-gplv2-dev libssl-dev libgdbm-dev libc6-dev libsqlite3-dev libbz2-dev libffi-dev
sudo apt install -y zlib1g-dev libffi-dev libssl-dev libbz2-dev libncursesw5-dev libgdbm-dev liblzma-dev libsqlite3-dev tk-dev uuid-dev libreadline-dev 

# If not using Ubuntu and using the redhat based system then only execute below command.
sudo yum install openssl-devel bzip2-devel libffi-devel gcc

pyenv install 3.6.3

git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
exec "$SHELL"

echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile

exec "$SHELL"

sudo apt-get install -y libpq-dev gcc python-dev

# If need Tensorflow
sudo apt-get -y install libtesseract-dev libleptonica-dev


# If centos
yum install gcc openssl-devel bzip2-devel libffi-devel
