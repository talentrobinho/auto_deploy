/*********************************************
 *     引入获取cookie用户信息js文件
*********************************************/
document.scripts[0].src="userInfo.js"

/*****************************
        获取树节点信息
******************************/
function get_selected_treeInfo(info, joinstr="_")
{

    //获取所选树节点信息
    var node = $("#leftbar").tree('getSelected');
    if( node == null)
    {
        alert("请选择服务节点")
        return false
    }
    if(info == 'node')
    {
        tr=node.text    
    }
    else if(info == 'tree')
    {
        var tr = node.text;
        var root = $('#leftbar').tree('getParent', node.target);
        while(root)
        {   
            tr = root.text + joinstr + tr; 
            node = root;
            root = $('#leftbar').tree('getParent', node.target);
        }
    }
    return tr 
}
/*****************************
    动态生成route的select
******************************/
function create_route_select(obj)
{
    //获取route 和ring 下拉框对象
    var routeSelect = document.getElementById('route')
    //清空route 和 ring 下拉框的值
    routeSelect.options.length=0;

    for(selectKey in obj)
    {
        routeSelect.options.add(new Option(selectKey, selectKey))
    }
}


/*********************************************************************************************************************
*                                             从凯撒接口获取IP函数 
*********************************************************************************************************************/
function get_ip(server)
{
    server_split=server.split('/')
    server_depth=server_split.length
   $.getJSON("/launcher/api/getip", 
            {'server': server}, 
            function(json_data){
                //alert(json_data)
                var num=1
                var tr
                var td
                var td_Caesar
                var td_Online
                var route_ring = ""
                var ip_total = 0
                $("#IpListTable").empty()
                // 添加表头
                tr=$("<tr id=th></tr>");
                tr.appendTo("#IpListTable");
                td1=$("<th style='Word-break: break-all'>Server</td>");
                td1.appendTo("#th");
                td2=$("<th style='Word-break: break-all'>Caesar</td>");
                td2.appendTo("#th");
                td3=$("<th style='Word-break: break-all'>Online</td>");
                td3.appendTo("#th");
                // 添加表内容
                for(var p in json_data)
                {
                    sinfo = json_data[p].path    
                    sp = json_data[p].ips
                    si = sinfo.replace(/\\/g, "")
                    //bb = si.replace("/", "#")
                    //sip = sp.join("\n")
                    aa = si.split('/')
                    //route_ring = aa[aa.length-2]+"_"+aa[aa.length-1]
                    bb = aa.length
                    route_ring = ''
                    ip_total += sp.length
                    while (server_depth != bb)
                    {
                        if(route_ring == "")
                        {
                            route_ring = aa[bb-1]
                            bb--
                        }
                        else
                        {
                            route_ring=aa[bb-1]+"<br/>"+route_ring
                            bb--
                        }
                        //alert(route_ring)
                    }
                    //route_ring = aa[aa.length-3]+"<br/>"+aa[aa.length-2]+"<br/>"+aa[aa.length-1]
                    //alert(str(sp))
                    tr=$("<tr id=tr"+num+"></tr>");
                    tr.appendTo("#IpListTable");
                    //sip_list = sp.split(",")
                    //alert(route_ring+"\n"+sp.length+"\n"+sp)
                    td=$("<td rowspan="+sp.length+" style='Word-break: break-all'>"+ route_ring +"</td>");
                    td.appendTo("#tr"+num);
                    for(index in sp)
                    {
                        td_Caesar=$("<td style='Word-break: break-all'>"+sp[index]+"</td>");
                        td_Online=$("<td style='Word-break: break-all'>10.100.100.100</td>");
                        td_Caesar.appendTo("#tr"+num);
                        td_Online.appendTo("#tr"+num);
                        num++
                        if(index != sp.length-1)
                        {
                            tr=$("<tr id=tr"+num+"></tr>");
                            tr.appendTo("#IpListTable");
                        }
                    }
                }
                // 统计的机器数
                //alert("ip total: "+ip_total)
                $("#machine").text("( "+ip_total+" )")
            }) 
}


/*******************************
    create tree in the left
********************************/
$(document).ready(function(){

    /*** 设置ajax为同步，来讲获取的返回值赋值给全局变量 ***/
    $.ajaxSettings.async = false;

    /*** 从凯撒获取服务信息 ***/
    //$.getJSON("/launcher/tree/getrr/", function(json_data){
    $.getJSON("/launcher/tree/getrr", function(json_data){
                rr_json=json_data
        });
    //$.getJSON("/launcher/tree/getsidebar/", function(json_data){
    $.getJSON("/launcher/tree/getsidebar", function(json_data){
                tree_data=json_data
        });
    /*** 回复ajax的异步模式 ***/
    $.ajaxSettings.async = true;

    /*** 生成左侧树形列表 ***/
    $("#leftbar").tree({
        data: tree_data,
        onClick: function(leftbar){
            tr = get_selected_treeInfo('tree')
            if(tr == false)
            {
                return false
            }
            
            var route = ""
            var ring_list = ""
            var rr = new Object()
            var ring = new Array()
            for(var ser_index in rr_json)
            {
                server=rr_json[ser_index]['content']
                route_list=rr_json[ser_index]['children']
                if(server == tr)
                {
                    for(var route_index in route_list)
                    {
                        route=route_list[route_index]['content']
                        ring_list=route_list[route_index]['children']
                        ring.length=0
                        for(var key in ring_list)
                        { 
                            ring[key]=ring_list[key]
                        }
                        rr[route]=ring;
                    }
                }
            }
            create_route_select(rr);
            /* 无需创建环下拉列表
            create_ring_select(rr);
            */

            server_str=get_selected_treeInfo('tree', '/')
            get_ip(server_str)


            /*** 检查是否在上线状态，开启构建、分发按钮 ***/
            /*
            $.getJSON("/op_online/",{"service":tr,"user":cookie_val}, function(json_data){
                        if(json_data[0]['status']=='is_online')
                        {
                            $("#button_build").removeAttr('disabled')
                            $("#button_deploy").removeAttr('disabled')
                        }
                        else
                        {
                            $("#button_build").attr('disabled',true)
                            $("#button_deploy").attr('disabled',true)
                        }
            });
            */
        }

        });
});
/*********************************************************************************************************************
*                                               检查表单函数 
*********************************************************************************************************************/
function check_form(is_online="false")
{
    var tree = get_selected_treeInfo('tree')
    var form_content = {}
    
    // 检查是否选择服务节点
    if(tree == false)
    {
        return false
    }
    //form_content['server'] = tree

    //检查、获取路选择值
    var routelist = new Array()
    routelist = $('#route option:selected').val()
    if(routelist.length == 0)
    {
        alert("route 不能为空")
        return false
    }
    if(is_online == "true")
    {
        //form_content['server'] = tree+"_"+routelist
        form_content['module_path'] = tree+"_"+routelist
    }
    else
    {
        //form_content['server'] = tree
        form_content['module_path'] = tree
        form_content['module_route'] = routelist
    }



    // // 检查选中上线内容复选框
    // if($("#bin").is(":checked"))
    // {
    //         form_content['bin'] = 1
    // }
    // else
    // {
    //         form_content['bin'] = 0
    // }
    // if($("#conf").is(":checked"))
    // {
    //         form_content['conf'] = 1
    // }
    // else
    // {
    //         form_content['conf'] = 0
    // }
    // if($("#data").is(":checked"))
    // {
    //         form_content['data'] = 1
    // }
    // else
    // {
    //         form_content['data'] = 0
    // }

    // content = form_content['bin'] + form_content['conf'] + form_content['data']
    // if(content == 0)
    // {
    //     alert("请选择上线内容")    
    //     return false
    // }

    return form_content
}
    
/*********************************************************************************************************************
*                                               获取页面信息函数 
*********************************************************************************************************************/
function get_page_info(is_online="false")
{
    var pgn = {}
    op_server_info = check_form(is_online)
    if(op_server_info == false)
    {
        return false
    }
    pgn['pgname'] = get_selected_treeInfo('node')
    form_info = $.extend(op_server_info, pgn)
    if(form_info == false)
    {
        return false
    }

    return form_info
}
  
/*********************************************************************************************************************
*                                               构建函数 
*********************************************************************************************************************/
function build()
{
    //var page_info = get_page_info(is_online="true")
    var form_info = check_form(is_online="true")
    $.post("/launcher/deploy/build", form_info, function(json_data){
        alert(json_data[0]['status'])
        },
        "json");
    show_build_modal('false')

    // 将js对象转换为json格式的字符串
    var build_value = JSON.stringify(form_info)
    $("#build_button").attr("value", build_value)
    
}
 
/*********************************************************************************************************************
*                                               发布函数 
*********************************************************************************************************************/
function deploy()
{
    //var page_info = get_page_info(is_online="true")
    var build_val = $("#build_button").val()
    var form_info = check_form(is_online="true")
    // 将json格式的字符串转换为js对象
    var build_info = JSON.parse(build_val)
    for(var key in build_info)
    {
        //if(build_info[key] != page_info[key])
        if(build_info[key] != form_info[key])
        {
            alert("构建与上线信息不符, 差异如下：\n构建的Server为: "+build_info[key]+"\n发布的Server为: "+form_info[key])
        }
    }
    $.post("/deploy/launch", form_info, function(json_data){
                alert(json_data[0]['status'])
        },
        "json");
    //show_deploy_modal('false')
}


/*********************************************************************************************************************
*                                               备份函数 
*********************************************************************************************************************/
function backup()
{
    var page_info = get_page_info()
    // 将js对象转换为json格式的字符串
    var backup_value = JSON.stringify(page_info)
    $("#backup_button").attr("value", backup_value)
}

/*********************************************************************************************************************
*                                               回滚函数 
*********************************************************************************************************************/
function rollback()
{
    var page_info = get_page_info()
    // 将js对象转换为json格式的字符串
    var rollback_value = JSON.stringify(page_info)
    $("#rollback_button").attr("value", rollback_value)
}

/*********************************************************************************************************************
 *                                          显示数据文件输入框
*********************************************************************************************************************/
function show_input()
{
    if($("#backup_data").is(":checked"))
    {
        $("#inputFile").removeAttr("style")    
    }
    else
    {
        $("#inputFile").attr('style',"display:none")    
    }
    
}

/*********************************************************************************************************************
*                                            显示模态框控制
*********************************************************************************************************************/
function show_build_modal(open='true')
{
    if(open == 'true')
    {
        
        build_info=check_form()
        if(build_info == false)
        {
            return false    
        }
        $("#build_service").text("上线模块为："+" "+build_info['module_path'])
        $("#build_route").text("模块上线的路为："+build_info['module_route'])
        $('#BuildModal').modal('show')
    }
    else
    {
        $('#BuildModal').modal('hide')    
    }
}

/// function show_deploy_modal(open='true')
/// {
///     if(open == 'true')
///     {
///         $('#deploy_modal').modal('show')
///     }
///     else
///     {
///         $('#deploy_modal').modal('hide')    
///     }
/// }
/// /// 
//
//
//
//
/// /*********************************************************************************************************************
///                                                to_online 
/// *********************************************************************************************************************/
/// function to_online()
/// {
///     tr = get_selected_treeInfo('tree')
///     if(tr == false)
///     {
///         return false    
///     }
///     /*** 是否进行上线操作模态框弹出 ***/
///     $.getJSON("/op_online/", {"service":tr,"user":cookie_val}, function(json_data){
///                 if(json_data[0]['status']=='is_online')
///                 {
///                    alert("你在上线状态") 
///                 }
///                 else if(json_data[0]['status']=='offline')
///                 {
///                     $("#online_modal").modal({backdrop: 'static', keyboard: false, show: true})
///                 }
///                 else
///                 {
///                     alert("Err code: "+json_data[0]['status']+"\n"+"No permission operation "+tr)    
///                 }
///         });
/// }
/// /*********************************************************************************************************************
///                                                Lock online 
/// *********************************************************************************************************************/
/// function sure_online()
/// {
///     tr = get_selected_treeInfo('tree')
///     if(tr == false)
///     {
///         return false    
///     }
///     $.getJSON("/lock_online/", {"service":tr}, function(json_data){
///         $("#online_modal").modal('hide')
///     });
///     $("#button_build").removeAttr('disabled')
///     $("#button_deploy").removeAttr('disabled')
///     
/// }
/// 

