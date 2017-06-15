#coding=utf-8
import httplib
import urlparse
import lxml
import lxml.html
import ast
import MySQLdb


html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="帮助老司机们情报收集、测试系统边界的在线域名情报收集系统">
    <meta name="author" content="dave.fang@outlook.com">
    <meta name="keywords" content="子域名, 域名信息, fuzz, fuzzall, 域名情报收集">
    <meta name="csrf-token" content="t6ZBKtxcvyHtPva0coGX2ot72i9h5atRfajORCwo">
    <title>baidu.com | 域名报告 | 域名情报收集系统 - Fuzz</title>
    <meta name="robots" content="nofollow" />
    <meta name="google-site-verification" content="256Gfx2r305b10kLMjz9dlmTZwg_FgvSVGFfBZb2FVE" />
    <meta name="baidu-site-verification" content="BhBS3Mje0i" />

    <!-- Favicons -->
    <link rel="shortcut icon" href="http://www.fuzzall.com/favicon.ico" type="image/x-icon">

    <!-- Bootstrap Core CSS -->
    <link media="all" type="text/css" rel="stylesheet" href="http://www.fuzzall.com/css/bootstrap.min.css">


    <!-- Custom CSS -->
    <link media="all" type="text/css" rel="stylesheet" href="http://www.fuzzall.com/css/offcanvas.css">

    <link media="all" type="text/css" rel="stylesheet" href="http://www.fuzzall.com/css/patch.css">

    
    <!-- Custom Fonts -->
    <link media="all" type="text/css" rel="stylesheet" href="http://www.fuzzall.com/font-awesome/css/font-awesome.min.css">


</head>

<body>
<nav class="navbar navbar-fixed-top navbar-inverse">
    <div class="container">
        <div class="navbar-header">
            <a class="navbar-brand" href="http://www.fuzzall.com">Fuzz</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
            <ul class="nav navbar-nav">
                <li ><a href="http://www.fuzzall.com">首页</a></li>
                <li ><a href="http://www.fuzzall.com/lab">实验室</a></li>
                <li ><a href="http://www.fuzzall.com/about">关于</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
                                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">evileo <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="http://www.fuzzall.com/user/dashboard">仪表盘</a></li>
                            <li><a href="http://www.fuzzall.com/user/submit">域名提交</a></li>
                            <li role="separator" class="divider"></li>
                            <li><a href="#">设置</a></li>
                            <li><a href="http://www.fuzzall.com/logout">注销</a></li>
                        </ul>
                    </li>
                            </ul>
        </div><!-- /.nav-collapse -->
    </div><!-- /.container -->
</nav><!-- /.navbar -->


<div class="container">

    
    <div class="row row-offcanvas row-offcanvas-left" style="margin-bottom: 60px;">

        <div class="col-md-3 sidebar-offcanvas" id="sidebar">
            <form method="get" action="http://www.fuzzall.com/search">
                <div class="input-group">
                    <span class="input-group-addon" style="background-color: #fff;"><i
                                class="glyphicon glyphicon-screenshot"></i></span>
                    <input type="text" name="q" class="form-control" placeholder="example.com"
                           value="baidu.com"/>
                    <span class="input-group-btn">
                        <button class="btn btn-default" type="submit">Go!</button>
                    </span>
                </div><!-- /input-group -->
            </form>
            <hr/>
            <div class="panel panel-info">
                <div class="panel-heading"><h3 class="panel-title text-center">DNS服务器记录</h3></div>
                <table class="table text-center">
                    <tbody>
                                                                        <tr>
                                <td>ns4.baidu.com</td>
                            </tr>
                                                    <tr>
                                <td>ns2.baidu.com</td>
                            </tr>
                                                    <tr>
                                <td>ns3.baidu.com</td>
                            </tr>
                                                    <tr>
                                <td>dns.baidu.com</td>
                            </tr>
                                                    <tr>
                                <td>ns7.baidu.com</td>
                            </tr>
                                                                </tbody>

                </table>
            </div>

            <div class="panel panel-info">
                <div class="panel-heading"><h3 class="panel-title text-center">MX服务器记录</h3></div>
                <table class="table text-center">
                    <tbody>
                                                                        <tr>
                                <td>mx1.baidu.com</td>
                            </tr>
                                                    <tr>
                                <td>jpmx.baidu.com</td>
                            </tr>
                                                    <tr>
                                <td>mx50.baidu.com</td>
                            </tr>
                                                    <tr>
                                <td>mx.n.shifen.com</td>
                            </tr>
                                                                </tbody>

                </table>
            </div>

            <div class="panel panel-info">
                <div class="panel-heading"><h3 class="panel-title text-center">关联域名列表</h3></div>
                <div class="list-group text-center">
                    <a href="#" class="list-group-item">暂无数据</a>
                </div>
            </div>
        </div><!--/.sidebar-offcanvas-->
        <div class="col-md-9">
            <p class="pull-right visible-xs">
                <button type="button" class="btn btn-primary btn-xs" data-toggle="offcanvas">Toggle nav</button>
            </p>
            <ol class="breadcrumb">
                <li><a href="http://www.fuzzall.com">Fuzz</a></li>
                <li><a href="#">域名</a></li>
                <li class="active">报告</li>
            </ol>

            <div class="panel panel-success">
                <!-- Default panel contents -->
                <div class="panel-heading text-center">Whois信息</div>
                <table class="table table-striped">
                    <tbody>
                        <tr>
                            <td class="col-md-2 text-right"><b>域名</b></td>
                            <td>baidu.com</td>
                        </tr>
                        <tr>
                            <td class="col-md-2 text-right"><b>管理人员</b></td>
                            <td>zhiyong duan</td>
                        </tr>
                        <tr>
                            <td class="col-md-2 text-right"><b>域名机构</b></td>
                            <td>Beijing Baidu Netcom Science Technology Co., Ltd.</td>
                        </tr>
                        <tr>
                            <td class="col-md-2 text-right"><b>联系邮箱</b></td>
                            <td>domainmaster@baidu.com</td>
                        </tr>
                        <tr>
                            <td class="col-md-2 text-right"><b>联系电话</b></td>
                            <td>暂无数据</td>
                        </tr>
                        <tr>
                            <td class="col-md-2 text-right"><b>创建时间</b></td>
                            <td>1999年10月11日</td>
                        </tr>
                        <tr>
                            <td class="col-md-2 text-right"><b>过期时间</b></td>
                            <td>2017年10月11日</td>
                        </tr>
                        <tr>
                            <td class="col-md-2 text-right"><b>更新时间</b></td>
                            <td>2015年09月10日</td>
                        </tr>
                        <tr>
                            <td class="col-md-2 text-right"><b>国家城市</b></td>
                            <td>暂无数据</td>
                        </tr>
                        <tr>
                            <td class="col-md-2 text-right"><b>具体地址</b></td>
                            <td>暂无数据</td>
                        </tr>
                        <tr>
                            <td class="col-md-2 text-right"><b>服务厂商</b></td>
                            <td>BEIJING INNOVATIVE LINKAGE TECHNOLOGY LTD. DBA DNS.COM.CN</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="panel panel-danger">
                <!-- Default panel contents -->
                <div class="panel-heading text-center">子域名信息</div>
                <table class="table table-striped" style="table-layout: fixed;">
                    <thead>
                    <tr>
                        <th width="80" class="text-center">#</th>
                        <th width="140">IP段</th>
                        <th>数据标记</th>
                                                                        <th width="160">收录时间</th>
                        <th width="60">操作</th>
                    </tr>
                    </thead>
                    <tbody>
                                            <tr>
                            <td class="text-center">2330</td>
                            <td>220.181.163.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2329</td>
                            <td>111.13.100.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2328</td>
                            <td>106.74.49.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2327</td>
                            <td>112.80.255.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2326</td>
                            <td>61.135.163.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2325</td>
                            <td>61.135.162.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2324</td>
                            <td>59.56.100.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2323</td>
                            <td>180.149.144.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2322</td>
                            <td>111.206.37.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2321</td>
                            <td>180.76.131.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2320</td>
                            <td>180.149.145.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2319</td>
                            <td>111.13.82.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2318</td>
                            <td>180.149.133.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2317</td>
                            <td>202.108.23.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2316</td>
                            <td>118.123.210.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2315</td>
                            <td>180.76.169.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2314</td>
                            <td>123.125.115.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2313</td>
                            <td>111.206.223.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2312</td>
                            <td>61.135.185.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2311</td>
                            <td>123.125.65.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2310</td>
                            <td>123.125.112.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2309</td>
                            <td>123.125.114.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2308</td>
                            <td>103.235.46.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2307</td>
                            <td>61.135.186.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                            <tr>
                            <td class="text-center">2306</td>
                            <td>112.80.248.0/24</td>
                            <td><span class="label label-info">未知</span></td>
                                                                                    <td>2016-04-22 10:02:20</td>
                            <td>
                                <button class="btn btn-warning btn-xs" type="button">
                                    误报
                                </button>
                            </td>
                        </tr>
                                        </tbody>
                </table>
            </div>
            <div class="text-center">
                <ul class="pagination"><li class="disabled"><span>&laquo;</span></li> <li class="active"><span>1</span></li><li><a href="http://www.fuzzall.com/report/baidu.com?page=2">2</a></li><li><a href="http://www.fuzzall.com/report/baidu.com?page=3">3</a></li><li><a href="http://www.fuzzall.com/report/baidu.com?page=4">4</a></li><li><a href="http://www.fuzzall.com/report/baidu.com?page=5">5</a></li><li><a href="http://www.fuzzall.com/report/baidu.com?page=6">6</a></li><li><a href="http://www.fuzzall.com/report/baidu.com?page=7">7</a></li><li><a href="http://www.fuzzall.com/report/baidu.com?page=8">8</a></li><li class="disabled"><span>...</span></li><li><a href="http://www.fuzzall.com/report/baidu.com?page=24">24</a></li><li><a href="http://www.fuzzall.com/report/baidu.com?page=25">25</a></li> <li><a href="http://www.fuzzall.com/report/baidu.com?page=2" rel="next">&raquo;</a></li></ul>
            </div>
        </div><!--/.col-xs-12.col-sm-9-->

    </div><!--/row-->


</div><!--/.container-->


<!-- jQuery JavaScript -->
<script src="http://www.fuzzall.com/js/jquery-2.2.1.min.js"></script>


<!-- Bootstrap Core JavaScript -->
<script src="http://www.fuzzall.com/js/bootstrap.min.js"></script>

<script src="http://www.fuzzall.com/js/offcanvas.js"></script>

<script src="http://www.fuzzall.com/js/patch.js"></script>



<script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
                (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-76680005-1', 'auto');
    ga('send', 'pageview');
</script>

</body>
</html>"""

def request(url, cookie=''):
    ret = urlparse.urlparse(url)    # Parse input URL
    if ret.scheme == 'http':
        conn = httplib.HTTPConnection(ret.netloc)
    elif ret.scheme == 'https':
        conn = httplib.HTTPSConnection(ret.netloc)
        
    url = ret.path
    if ret.query: url += '?' + ret.query
    if ret.fragment: url += '#' + ret.fragment
    if not url: url = '/'
    
    conn.request(method='GET', url=url , headers={'Cookie': cookie,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'})
    return conn.getresponse()




def _to_db(html,db,cursor,domain_name):
    html = lxml.html.fromstring(html)

    rows = html.xpath('//table')
    '''
    list_dns_record = []
    list_mx_record = []
    elements = rows[0].xpath('.//tr')
    for k in elements:
        c =  k.xpath('.//td//text()')
        #print c
        list_dns_record.append(c[0])
    #print list_dns

    
    elements = rows[1].xpath('.//tr')
    if  len(elements) < 1:
        return 3
    for k in elements:
        c =  k.xpath('.//td//text()')
        list_mx_record.append(c[0])

 
 

    print list_dns_record
    print list_mx_record'''
    dic_domain = {}
  
   
    elements = rows[3].xpath('.//tr')
    if  len(elements)  <2:
        return False
    for k in elements:
        c =  k.xpath('.//td//text()')
         
        if len(c)>0:
            dic_domain['domain'] = domain
            dic_domain['fuzzall_id'] = int(c[0])
            dic_domain['ip_range'] = c[1]
            #dic_domain['data_tag'] = c[2]
            dic_domain['fuzz_time'] = c[3]
            sql = "INSERT INTO app_domainiprange(domain_name, \
                        ip_range, fuzz_time, fuzzall_id) \
                       VALUES ('%s',   '%s', '%s', '%d' )" % \
                       (domain_name,  dic_domain['ip_range'], dic_domain['fuzz_time'], dic_domain['fuzzall_id'])
            
            cursor.execute(sql)
         
    db.commit()
    return True



if __name__ == '__main__':
    
    db = MySQLdb.connect("127.0.0.1","root","wenjunnengyoujiduochou","xlcscan" )
    cursor = db.cursor()

    cookie_str = "Cookie:_gat=1; XSRF-TOKEN=eyJpdiI6ImZZeEJcL2ZqbWRLcnlqdFg3QzNsZHZnPT0iLCJ2YWx1ZSI6InlyTHJSVDdFYzB3YmF0MURkMVVEUktmZzJvaUFjMFRReGUwN2plZHNDalwvYzJUQVgxMzZxVmtyU2djWUR1RWZUb2VzN3lmeHdNSVZcL3Uyam1maW5uOXc9PSIsIm1hYyI6ImFiNDA4NDFjNjNjOTYxYTU0YTRiOGZiNzBjNjdhNGNiOGE5OGRlMTUwZDQ3NGI0MjI1YTAyOWE0ZjAyNDJmOTEifQ%3D%3D; fa_session=eyJpdiI6ImJtd2h0dmF5VHZ2YW91c1NaN3RIVlE9PSIsInZhbHVlIjoiTTI2S3lMbTdXdjRJK2oyM3lsMDN6SFpBREYzeGFjYXF5bXBJaFVVT0dBNE1IYnc3SW8wUVk0RmxtcWs1NE5weGZqRCtEbDk1am42Nmx1NlZEUENCN3c9PSIsIm1hYyI6ImQxY2JkY2ZmMTQ2ZmE2NmI0ZGI1N2QzMDIyNTNmYmNlNzQ1M2Y4YzliN2I4NWZlODUwNjFkNGY5MWU1MjYwYWMifQ%3D%3D; _ga=GA1.2.1590040800.1461128225"
    
    
    domain_list = open('domain.txt')
    for domain in domain_list:
            domain = domain.strip()
 
            page = 1
            Ta = True
            while Ta:
                print domain,page
                #domain = 'baidu.com'
                url = 'http://www.fuzzall.com/report/%s?page=%d' % (domain,page)
                html_doc = request(url, cookie_str).read()
                Ta = _to_db(html_doc,db,cursor,domain)
                #print html_doc
                page = page+1
                           
            
    #print html_doc
    
    db.close()
