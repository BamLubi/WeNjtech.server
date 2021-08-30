<?php
    require_once "./config.php";

    // 1. 获取参数
    $username = $_POST["username"];
    $password = $_POST["password"];
    log_file(basename(__FILE__), __LINE__, "POST params: ".$username." ".$password);

    // 2. 判断参数是否齐全
    if ($username == NULL || $password == NULL){
        echo FAIL("", "请附带请求参数:username password");
        return;
    }

    // 3. 执行命令
    $output = exec_python("service/login.py ".$username." ".$password);
    echo $output;
?>