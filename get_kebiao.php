<?php
    require_once "./config.php";

    // 1. 获取参数
    $username = $_POST["username"];
    $password = $_POST["password"];
    $openid = $_POST["openid"];
    log_file(basename(__FILE__), __LINE__, "POST params: ".$username." ".$password." ".$openid);

    // 2. 判断参数是否齐全
    if ($username == NULL || $password == NULL){
        echo FAIL("", "请附带请求参数:username password");
        return;
    }

    // 3. 设置查询学期、学年
    $year = intval(date('Y'));
    $month = intval(date('m'));
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

    // 4. 执行命令
    log_file(basename(__FILE__), __LINE__, "执行python文件");
    $output = exec_python("service/get_kebiao.py ".$username." ".$password." ".$openid." ".$query_year." ".$query_term);
    echo $output;
?>