这是一个爬取淘宝商品信息和评论的小项目，默认爬取第一页商品搜索中所有商品的前10页评论信息<br>
使用scrapy框架、Beautifulsoup、selenium实现<br>

流程可分为爬取三种链接：<br>
    1.搜索商品页面的链接<br>
    https://s.taobao.com/search?q=u%E7%9B%98&s=44<br>
    观察可得，q=<搜索关键字>,s=<页码，数值整除44的值就是页码><br>

    2.商品详细介绍页面<br>
    https://detail.tmall.com/item.htm?id=570208685303&ali_refid=a3_430583_1006:1110663897:N:u%E7%9B%98:df214e090f93c9e8f2b15d9868847464&ali_trackid=1_df214e090f93c9e8f2b15d9868847464&spm=a230r.1.14.3&sku_properties=5919063:6536025
    可直接爬取

    3.获取评论的url
    https://rate.tmall.com/list_detail_rate.htm?itemId=570208685303&sellerId=2438280281&currentPage=1<br>
    观察可得，需要获取itemId、sellerId的值，并可以通过改变currentPage的值实现评论翻页<br>


代码调试过程中遇到的问题：<br>
    1.scrapy的setting中可设置是否遵守robot.txt，本项目需要把该项改为False才能继续爬取;<br>
    2.在python中‘’的作用和“”近似，但在json‘’不能用作“”;<br>

