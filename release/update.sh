echo '删除log'
rm /home/www/ZhiMing/zhiming.log

PROJ_ROOT=/home/www/ZhiMing/src

cd $PROJ_ROOT
echo '更新源码'
sudo -u www git pull
sudo -u www git submodule update --init --recursive --remote

FRONT_ROOT=$PROJ_ROOT/src/frontend
DIST=$FRONT_ROOT/dist

cd $FRONT_ROOT
echo '编译前端文件'
sudo -u www yarn install
sudo -u www yarn build
sudo -u www rm $DIST/js/*.map

sudo -u www rm /var/html/zhiming/* -rf
sudo -u www cp $DIST/* /var/html/zhiming/ -r

if [ `whoami` = "root" ]
then
    echo '重启服务'
    systemctl restart zhiming
else
    echo '权限不足，无法重启'
fi
