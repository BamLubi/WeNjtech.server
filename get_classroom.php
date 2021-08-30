<?php
    require_once "./config.php";

    // 1. 获取参数
    $username = "1405170121";
    $password = "1999819lyy";
    log_file(basename(__FILE__), __LINE__, "INIT params: ".$username." ".$password);

    // 2. 配置查询参数
    $query_year = 2021;// 查询_学年
    $query_term = 3;// 查询_学期 值为3或12;2~7月=>12,9~1月=>3
    $query_term_week = 1024;// 查询_周次
    $query_week = 1;// 查询_星期
    $query_time = 3;// 查询_节次
    $cdlb_limit = ['004', '005', '007', '009', '011'];// 指定的场地类别
    $time_limit = [3, 12, 48, 192, 768];// 指定的节次，以两节课为一次
    $login_config = array('username' => $username, 'password' => $password);
    ## 设置查询_星期
    $query_week = intval(date('w')); // 获取星期几，获取结果为[1,2,3,4,5,6,0]需要将周日改为7
    if ($query_week == 0) $query_week = 7;
    ## 设置查询学期、学年
    $year = intval(date('Y'));
    $month = intval(date('m'));
    $day = intval(date('d'));
    if ($month <=7 && $month >= 2) {
        // 第二学年
        $query_term = 12;
        $query_year = $year - 1;
    }else if ($month <=12 && $month >= 8) {
        // 第一学年
        $query_term = 3;
        $query_year = $year;
    }else if ($month == 1) {
        // 第一学年
        $query_term = 3;
        $query_year = $year - 1;
    }
    log_file(basename(__FILE__), __LINE__, "学年:".$query_year." 学期:".$query_term." 周次:".$query_term_week." 星期:".$query_week);
    ## 设置查询周数
    $day1 = strtotime('2021-8-30'); // 8月31日为第1周，此项为基准周次，最大值为20周
    $day2 = strtotime(date('Y-m-d'));
    $query_term_week = intval(($day2 - $day1)/(86400*7)) + 1;
    if ($query_term_week > 20) $query_term_week = 20;
    $query_term_week = pow(2, $query_term_week - 1);

    // $query_config = array('year' => $query_year, 'term' => $query_term, 'term_week' => $query_term_week, 'week' => $query_week, 'time' => $query_time);

    // 4. 查询空教室，全部交由python
    // 由python获取每次数据，并且拼接和筛选，并保存在本地和上传小程序
    $output = exec_python("service/get_classroom.py ".$username." ".$password." ".$query_year." ".$query_term." ".$query_term_week." ".$query_week);

    echo $output;
?>