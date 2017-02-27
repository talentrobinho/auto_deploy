/*********************************************
 *     引入获取cookie用户信息js文件
 *  *********************************************/
document.scripts[0].src="userInfo.js"


/********************************
        添加上线权限
********************************/
function get_save_privilege()
{
        /*
         *   从后端redis数据库中获取用户的权限列表，并在前端显示
         */
        var user=$("#userSelect").find("option:selected").text()
        //$.post("/show_saved_privilege/", {'user': user},function(json_data){
        $.post("/launcher/admini/getprivilege", {'user': user},function(json_data){
                var ss = json_data['own']
                var unss = json_data['out']
                unselected_server = unss.split(",")
                if(ss == 'None')
                {
                    selected_server=[]    
                }
                else
                {
                    selected_server = ss.split(",")
                }

                $("#own_list").empty()
                $("#out_list").empty()
                $(selected_server).each(function (index, ser){
                    $("#own_list").append("<option value='Value'>"+ser+"</option>")
                    });
                $(unselected_server).each(function (index, unser){
                    $("#out_list").append("<option value='Value'>"+unser+"</option>")
                    });
        });
    
}
function give_privilege()
{
                    
        //$("#own_list").empty()
        //$("#userSelect").find("option[text="+cookie_val+"]").attr("selected",true); 
        //alert(cookie_val)
        $.post("/launcher/admini/getprivilege", {'user': cookie_val}, function(json_data){
            alert(json_data)
            var selected_server
            var unselected_server
            var own_server
            var out_server
            var user_role

            own_server = json_data['own']
            out_server = json_data['out']
            user_role = json_data['role']
            alert(own_server)
            alert(out_server)
            alert(user_role)
            /*
            if(user_role != 1)
            {
                alert('YOU ARE NOPERMISSION')
                return false
            }
            else
            {
                unselected_server = out_server.split(",")
                if(own_server == "None")
                {
                    selected_server = []
                }
                else
                {
                    selected_server = own_server.split(",")
                }
                //$("#out_list").append("<option value='Value'>"+server_info+"</option>")
                $("#own_list").empty()
                $("#out_list").empty()
                $(selected_server).each(function (index, ser){
                    $("#own_list").append("<option value='Value'>"+ser+"</option>")
                    });
                $(unselected_server).each(function (index, unser){
                    $("#out_list").append("<option value='Value'>"+unser+"</option>")
                    });
            }*/
            //$('#set_privilege').modal('show')
        });

        // 选择赋予权限的server，在已选择列表中显示，并在待选列表中删除
        $('#out_list').dblclick(function(){
            append_server=$("#out_list").find("option:selected").text()
            // 防止添加空选项
            if(append_server == '')
            {
                return false    
            }
            $('#out_list option:selected').remove();
            $("#own_list").append("<option value='Value'>"+append_server+"</option>")
        });

        // 删除已选择的server，并添加到待选择列表中
        $('#own_list').dblclick(function(){
            append_server=$("#own_list").find("option:selected").text()
            // 防止添加空选项
            if(append_server == '')
            {
                return false    
            }
            $('#own_list option:selected').remove();
            $("#out_list").append("<option value='Value'>"+append_server+"</option>")
        });


}
/********************************
        权限写入数据库
********************************/
function add_privilege_to_db()
{
    $('#set_privilege').modal('hide')
    no_select=$("#out_list option").map(function(){return $(this).text();}).get().join(", ")
    yes_select=$("#own_list option").map(function(){return $(this).text();}).get().join(", ")
    user=$("#nameSelect").find("option:selected").text()

    //$.post("/record_privilege/", {"no_choice_privilege":no_select, "yes_choice_privilege":yes_select, 'user':user}, function(json_data){
    $.post("/launcher/admini/modifyPrivileges/", {"no_choice_privilege":no_select, "yes_choice_privilege":yes_select, 'user':user}, function(json_data){
        alert(json_data[0]['status'])
    }, "json");
}
