# TODO subir daemons de acordo com o especificado em config.json
BASEDIR="/home/aluno/redes/projeto1"

# Kills all running daemons
pkill -f daemon.py
rm $BASEDIR/logs/daemon*

$BASEDIR/slave/daemon.py 5000 &
$BASEDIR/slave/daemon.py 5001 &
$BASEDIR/slave/daemon.py 5002 &
