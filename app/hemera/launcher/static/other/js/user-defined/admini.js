/********************************
        添加上线权限
********************************/
function get_save_privilege()
{
        var user=$("#userSelect").find("option:selected").text()
        //$.post("/show_saved_privilege/", {'user': user},function(json_data){
        $.post("/launcher/admini/userPrivileges/", {'user': user},function(json_data){
                for(var i=0;i<json_data.length;i++)
                {
                    var ss = json_data[i]['yes']
                    var unss = json_data[i]['no']
                    unselected_server = unss.split(",")
                    if(ss != 'None')
                    {
                        selected_server = ss.split(",")
                    }
                    else
                    {
                        selected_server=[]    
                    }

                    $("#own_list").empty()
                    $("#out_list").empty()
                    $(selected_server).each(function (index, ser){
                        $("#own_list").append("<option value='Value'>"+ser+"</option>")
                        });
                    $(unselected_server).each(function (index, unser){
                        $("#out_list").append("<option value='Value'>"+unser+"</option>")
                        });
                }
        });
    
}
function set_privilege()
{
        var server_info=""
        var tmp_add=""
        var is_privilege
                    
        $("#own_list").empty()
        //$.getJSON("/getserverlist/", function(json_data){
        $.getJSON("/launcher/admini/getserverlist/", function(json_data){
            for(var i=0;i<json_data.length;i++)
            {
                server_info=json_data[i]['server']
                if(server_info == 'NOPERMISSION')
                {
                    is_privilege='NO'
                }
                else
                {
                    $("#out_list").append("<option value='Value'>"+server_info+"</option>")
                }
            }
            if(is_privilege == 'NO')
            {
                alert('YOU ARE NOPERMISSION')
                return false
            }
            $('#set_privilege').modal('show')
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
