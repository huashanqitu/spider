import sys
import os
# 导入执行spider命令行函数
from scrapy.cmdline import execute

# 获取当前项目目录，添加到系统中
# 方法一:直接输入，不便于代码移植
# (比如小明和小红的项目路径可能不一样，那么小明的代码想在小红的电脑上运行,
# 路径就要手动改了，python怎么能这么麻烦呢，请看方法二)
# sys.path.append("H:\spider_project\spider_bole_blog\spider_bole_blog")
# 方法二：代码获取，灵活，代码移植也不影响
# print(os.path.dirname(os.path.abspath(__file__)))
# result : H:\spider_project\spider_bole_blog\spider_bole_blog
# 获取当前项目路径，添加到系统中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 执行spider命令

# 这里的爬虫名字是spiders中的文件中的name属性
execute(['scrapy', 'crawl', 'xicidaili'])