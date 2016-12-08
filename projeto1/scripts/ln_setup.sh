# Script para gerenciar a distribuição dos arquivos pelo sistema,
# conforme o necessário. 
#
# TODO
# Provavelmente, webserver.py dependerá de outros arquivos (e.g. backend.py).
#
# Basicamente, precisamos de:
# 	- html em /var/www para ser servido pelo Apache
# 	- código do servidor em /usr/lib/cgi-bin para ser utilizado pelo Apache+CGI (configurado em /etc/apache2/conf-enabled/serve-cgi-bin.conf

BASEDIR="/home/aluno/redes/projeto1"

sudo rm -rf /var/www/html
sudo rm -f /usr/lib/cgi-bin/webserver.py
sudo ln -s $BASEDIR/server/webserver.py /usr/lib/cgi-bin/webserver.py
sudo ln -s $BASEDIR/server/templates /var/www/html

# Para que o Apache siga corretamente o symlink,
# o owner do webserver.py deve ser igual ao owner
# do Apache
sudo chown root $BASEDIR/server/webserver.py
