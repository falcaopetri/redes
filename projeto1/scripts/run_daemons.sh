BASEDIR="/home/aluno/redes/projeto1"

# Kills all running daemons
pkill -f daemon.py
rm /tmp/daemon*

$BASEDIR/slave/daemon.py 5000 &
$BASEDIR/slave/daemon.py 5001 &
$BASEDIR/slave/daemon.py 5002 &
