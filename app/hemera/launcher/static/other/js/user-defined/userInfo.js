/*****************************
        获取COOKIE信息
******************************/
/**************************************
      第一个方法找cookie值
***************************************/  
// 定义一个函数，用来读取特定的cookie值。  
function getCookie(cookie_name)  
{  
    // 读取属于当前文档的所有cookies  
    var allcookies = document.cookie;  
    var cookie_pos = allcookies.indexOf(cookie_name);   //索引的长度  
       
    // 如果找到了索引，就代表cookie存在，  
    // 反之，就说明不存在。  
    if (cookie_pos != -1)  
    {  
        // 把cookie_pos放在值的开始，只要给值加1即可。  
        cookie_pos += cookie_name.length + 1;      //这里我自己试过，容易出问题，所以请大家参考的时候自己好好研究一下。。。  
        var cookie_end = allcookies.indexOf(";", cookie_pos);  
        if (cookie_end == -1)  
        {  
            cookie_end = allcookies.length;  
        }  
        var value = unescape(allcookies.substring(cookie_pos, cookie_end)); //这里就可以得到你想要的cookie的值了。。。  
    }  
    return value;  
}  

/**************************************
      第二个方法找cookie值
***************************************/  
// 定义一个函数，用来读取特定的cookie值。  
function getCookie2(cookie_name)  
{  
    var allcookies = document.cookie;  
    var cookie_arr = allcookies.split(";")  //将cookie转存到数组中

    //遍历cookie数组，查找给定的cookie值
    for(var i=0;i<cookie_arr.length;i++)
    {
        cookie_pos=cookie_arr[i].indexOf(cookie_name)
        //如果找到所给cookie，则退出查找循环，并返回找到的值
        if (cookie_pos != -1)  
        {  
            cookie_value=cookie_arr[i].split("=")[1]
            break
        }
        else
        {
            cookie_value=null
        }
    }
       
    return cookie_value
}  


// 调用函数  
//var cookie_val = getCookie("_adtech_user");  
var cookie_val = getCookie2("_adtech_user");  






/*********************************************************************************************************************
                                       添加个人姓名到index.html页面函数 
*********************************************************************************************************************/
function add_person_info()
{
    $("#personOne").text(cookie_val)    
    $("#personTwo").text(cookie_val)    
    $("#personThr").text(cookie_val)    
}
$(document).ready(function(){
        /*** 添加人名信息 ***/
        add_person_info()
            });
