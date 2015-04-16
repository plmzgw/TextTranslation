
// 发送请求(方法[post,get], 地址, 数据, 回调函数)
function ajax_send_request(method, url, data, callback){
    var objHttp;
    if (window.XMLHttpRequest){
        objHttp=new XMLHttpRequest();
     }
    else
    {
        objHttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    with(objHttp)
    {
        try
         {
            open(method, url, true);
            setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
            send(data);
            onreadystatechange = function ()
              {                   
                if (objHttp.readyState == 4 && (objHttp.status == 200 || objHttp.status == 304))
                  {
                    return callback(objHttp);
                  }
             }
        }
       catch(e)
        {
           alert(e);
        }
    } 
}