sudo systemctl stop mongod
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo systemctl start mongod