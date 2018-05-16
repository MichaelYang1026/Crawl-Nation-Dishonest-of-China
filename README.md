# Crawl-Nation-Dishonest-of-China
use python3 to crwal individual nation dishontest list
1."crawl_disthontest.py" 
This program is used to store dishonest list in external files. However, every time you run it, it may crawl duplicate logs.
该程序用于将失信人名单储存在外部文件。但是，每次运行的时候，输出的文件中可能会包含重复的记录。

2."crwal_dishontest_mysql.py"
This program is used to store dishonest list in Mysql. Before you run it, you should build Mysql environment and create a database.
In this program, only the logs that never appear in Mysql tables will be inserted.
When you run this program, you'd better have a larger computer display. Otherwise, the simulator of selenium may not reach the screen border, which will cause an error of this program. To prevent this potential error, you can get a large computer display like 27 inches or optimize the codes.
该程序用于将失信人名单储存在Mysql数据库中。在运行程序之前，你需要完成Mysql环境配置并且创建一个数据库。在本程序中，只有从未在数据库表格中出现的记录会被插入数据库中。在运行此程序时，最好电脑配置一个大的显示屏。否则，有可能会由于屏幕过小导致模拟器无法移动到指定位置，从而造成运行错误。为了防范此问题，你可以配置一个27英寸以上的显示屏或者优化代码。
