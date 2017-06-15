
xmanage celery worker --loglevel=info

xmanage  celery flower
or
xmanage  celery  flower  --broker=redis://:ruijiangmei@115.28.72.96:6379/1 
xmanage  celery  flower  --broker=redis://localhost:6379/0

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
一. 如何初始化redis的密码？
总共2个步骤：
a.在配置文件中有个参数： requirepass  这个就是配置redis访问密码的参数。
比如 requirepass test123
b.配置文件中参数生效需要重启重启redis 。
 
二.不重启redis如何配置密码?
a. 在配置文件中配置requirepass的密码（当redis重启时密码依然有效）。
# requirepass foobared
 如  修改成 :
requirepass  test123
 
b. 进入redis重定义参数
查看当前的密码：
[root@slaver251 redis-2.4.16]# ./src/redis-cli -p 6379
redis 127.0.0.1:6379> 
redis 127.0.0.1:6379> config get requirepass
1) "requirepass"
2) (nil)
显示密码是空的，
然后设置密码：
redis 127.0.0.1:6379> config set requirepass test123
OK
再次查询密码：
redis 127.0.0.1:6379> config get requirepass
(error) ERR operation not permitted
此时报错了！
现在只需要密码认证就可以了。
redis 127.0.0.1:6379> auth test123
OK
再次查询密码：
redis 127.0.0.1:6379> config get requirepass
1) "requirepass"
2) "test123"
密码已经得到修改。
当到了可以重启redis的时候 由于配置参数已经修改 所以密码会自动生效。
要是配置参数没添加密码 那么redis重启 密码将相当于没有设置。
 
三.如何登录有密码的redis？
a.在登录的时候 密码就输入
[root@slaver251 redis-2.4.16]# ./src/redis-cli -p 6379 -a test123
redis 127.0.0.1:6379> 
redis 127.0.0.1:6379> config get requirepass
1) "requirepass"
2) "test123"
 
b.先登录再验证：
[root@slaver251 redis-2.4.16]#  ./src/redis-cli -p 6379
redis 127.0.0.1:6379> 
redis 127.0.0.1:6379> auth test123
OK
redis 127.0.0.1:6379> config get requirepass
1) "requirepass"
2) "test123"
redis 127.0.0.1:6379>
 
四. master 有密码,slave 如何配置？
当master 有密码的时候 配置slave 的时候 相应的密码参数也得相应的配置好。不然slave 是无法进行正常复制的。
相应的参数是：
#masterauth
比如:
masterauth  mstpassword
 

 