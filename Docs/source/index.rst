自动下载 LAADS 卫星数据
====================================

介绍
------------------------------------

这是一个小工具，用于自动获取 LAADS DAAC 数据产品的下载地址，并直接下载文件。

一级产品与大气档案与分发系统（LAADS）分布式主动档案中心（DAAC）是美国宇航局（NASA）地球观测系统数据和信息系统（EOSDIS）的 12 个 DAAC 之一，其学科领域是大气科学。LAADS DAAC 为全球提供 MODIS、SNPP 和 VIIRS 的科学数据产品及所有相关资源。

`下载 laadsDown.py <url>`_
*（将此文件保存到数据存储位置的根目录下）*

系统环境
------------------------------------

* Windows/macOS
* `Python 3.7.2 🔗 <https://www.python.org/>`_
* `安装 Requests 模块 🔗 <http://cn.python-requests.org/zh_CN/latest/user/install.html#install>`_
* `配置环境变量 💬 <https://stackoverflow.com/a/52230415/10860600>`_ 以调用多进程下载::

    "env": {
        "OBJC_DISABLE_INITIALIZE_FORK_SAFETY": "YES"
    }

..
    否则操作系统无法调用多进程下载，并报错。

适用范围
------------------------------------

LAADS DAAC 网站上提供的，单天文件数不超过 1 的卫星产品。

URL 参数说明
------------------------------------

在 LAADS DAAC 网站上下载数据产品时，将获得一个 URL 地址::

    https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/COLLECTION/PRODUCT/YEAR/DAY_OF_YEAR/FILENAME

其中， ``https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/`` 为固定的 URL 前缀，其余参数为：

    ``COLLECTION``
        数据集版本
    ``PRODUCT``
        产品名
    ``YEAR``
        采样年份
    ``DAY_OF_YEAR``
        一年中的第几天。如 2 月 1 日用 ``032`` 表示
    ``FILENAME``
        待获取的文件名

一个完整的 URL 如下::

    https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6/MOD02QKM/2007/018/MOD02QKM.A2007018.0105.006.2014227230926.hdf

这表示一个名为 ``MOD02QKM.A2007018.0105.006.2014227230926.hdf`` 的文件，属于第 ``6`` 版数据集的 ``MOD02QKM`` 产品，它的采样时间是 ``2007`` 年第 ``018`` 天（一月 18 日）。

操作指南
------------------------------------

(1) 确定数据集和产品名
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在 `Find Data <https://ladsweb.modaps.eosdis.nasa.gov/search/>`_ 或 `LAADS Archive <https://ladsweb.modaps.eosdis.nasa.gov/archive/allData>`_ 寻找一个所需的数据文件，从它的下载地址中获取 ``COLLECTION`` 和 ``PRODUCT`` 参数，并修改程序第 2 段的相关代码，如::

    collection = '61'
    product = 'MYD08_D3'

(2) 输入时间范围
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

修改以下 3 个参数：

    ``year``
        要下载数据的年份
    ``first_day``
        起始日（一年中的第几天）
        *取值必须小于或等于* ``last_day``
    ``last_day``
        结束日（一年中的第几天）
        *默认为 0，将自动判断当年的天数并设置为该值。*

如::

    year = 2018
    first_day = 1
    last_day = 0

则将会下载 2018 全年的数据。而::

    year = 2019
    first_day = 45
    last_day = 359

则将下载 2019/2/14 至 2019/12/25 的 315 天数据。


(3) 运行程序
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(4) 检查下载失败的文件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

所有文件下载完成后，终端中将提示下载失败的日期序号，失败的原因可能是：

#. 当天文件不存在，LAADS DAAC 未提供；
#. 网络连接问题，导致文件地址获取失败；

请在 `LAADS DAAC <https://ladsweb.modaps.eosdis.nasa.gov/archive/allData>`_ 网站查找相关文件，以排除文件缺失的可能。如果文件存在，则修改时间范围，重新下载这些文件。


.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. contents::
   :backlinks: none