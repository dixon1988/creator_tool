basepath=$(cd `dirname $0`; pwd)
echo "basepath:"$basepath

python3 $basepath/python_service/pkg_server.py
