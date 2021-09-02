<?php
    /** 浏览器设置 */
    set_time_limit(0);// 设置无线运行时间
    ignore_user_abort(true);// 设置浏览器关闭继续运行

    /** 日志设置 */
    $log = "日志文件路径";
    function log_file($file, $line, $content) {
        global $log;
        error_log(date("Y-m-d H:i:s", time()) . " - " . $file . "[line:" . $line . '] - ' . $content . "\n", 3, $log);
    }

    /** 返回信息 */
    $response = array ('code'=>NULL,'data'=>NULL,'mark'=>NULL);
    function OK($data, $mark){
        global $response;
        $response["code"] = 200;
        $response["data"] = $data;
        $response["mark"] = $mark;
        return json_encode($response, JSON_UNESCAPED_UNICODE);
    }
    function FAIL($data, $mark){
        global $response;
        $response["code"] = 400;
        $response["data"] = $data;
        $response["mark"] = $mark;
        return json_encode($response, JSON_UNESCAPED_UNICODE);
    }

    /** 执行python程序 */
    function exec_python($path){
        $output = exec('export LANG=en_US.UTF-8;'.'python3 项目文件目录'.$path);
        return $output;
    }
?>