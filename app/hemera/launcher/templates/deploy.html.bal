<!DOCTYPE html>
<html lang="zh-cn">
    <head>
        <meta charset="utf-8">
        <script>
            var myBar;

            $(document).ready(function(){
                load_database()
                $("#progress-bar").hide();
                $("#build-OK").click(function(){
                    $("#progress-bar").show();
                    $('#buildModal').modal('hide');
                    //$("#build").attr("disabled",true);
                    bar();
                    $.ajax({ 
                        type: "GET", 
                        url: "{{ url_for('lau.build_job') }}", 
                        success: function(data){
                            $('#barc').css("width","100%");
                            clearInterval(myBar);
                            $("#progress-bar").hide();
                            alert(data['result']);
                            load_database()
                            //$("#build").attr("disabled",false)
                            //$("#launch").attr("disabled",false)
                        }
                    });
                });
                $("#deploy-OK").click(function(){
                    $('#deployModal').modal('hide');
                    //$("#launch").attr("disabled",true)
                    $.ajax({ 
                        type: "GET", 
                        url: "{{ url_for('lau.deploy_job') }}", 
                        success: function(data){
                            alert(data['result']); 
                    //        $("#launch").attr("disabled",false)
                        } 
                    });
                });
            });

            function process(percent){
                $('#barc').css("width",percent+"%");
            }

            function bar(){
                var percent = 0;
                myBar = setInterval(function(){ process(percent);percent += 0.2;if(percent > 92){ clearInterval(myBar); } }, 100);
            }

            //$('#deployModal').modal('toggle')
            $(function(){
                $('#deployModal').modal({
                    keyboard: false,
                    backdrop: false,
                    show: false
                })
                $('#buildModal').modal({
                    keyboard: false,
                    backdrop: false,
                    show: false
                })
            });

            function load_database(){
                //src_rpm="{{ url_for('lau.database') }}"
                src_machine="{{ url_for('lau.machine') }}"
                //$("#database").load(src_rpm);
                $("#machine").load(src_machine);
            }

        </script>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12">
                    <br />
                </div>
                <div class="col-md-12">
                    <div class="col-md-6">
                        <div class="col-md-12" style="width:100%;height:400px;">
                            <div id="machine">
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div id="progress-bar" class="progress">
                                <div id="barc" class="progress-bar" role="progressbar" aria-valuenow="20" aria-valuemin="30" aria-valuemax="10" style="width: 0%;"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="col-md-12" style="width:100%;height:400px;">
                            <h4>Console Output</h4>
                            <div id="output" style="border-bottom:1px solid #ddd">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-12">
                        <div class="btn-group">
                            <button id="build" type="button" class="btn btn-warning" data-toggle="modal" data-target="#buildModal">build</button>
                        </div>
                        <div class="btn-group">
                            <button id="launch" type="button" class="btn btn-danger" data-toggle="modal" data-target="#deployModal">launch</button>
                        </div>
                </div>
                <div class="col-md-12">
                    <div class="modal fade" id="buildModal" tabindex="-1" role="dialog" aria-labelledby="buildModalLabel" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span>
                                    </button>
                                    <h4 class="modal-title">Build job</h4>
                                </div>
                                <div class="modal-body">
                                    <p>You will build the job&hellip;</p>
                                </div>
                                <div class="modal-footer">
                                    <button id="build-Cancel" type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                                    <button id="build-OK" type="button" class="btn btn-primary">OK</button>
                                </div>
                            </div><!-- /.modal-content -->
                        </div><!-- /.modal-dialog -->
                    </div><!-- /.modal -->
                    <div class="modal fade" id="deployModal" tabindex="-1" role="dialog" aria-labelledby="deployModalLabel" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span>
                                    </button>
                                    <h4 class="modal-title">Deploy job</h4>
                                </div>
                                <div class="modal-body">
                                    <p>You will deploy the job&hellip;</p>
                                </div>
                                <div class="modal-footer">
                                    <button id="deploy-Cancel" type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                                    <button id="deploy-OK" type="button" class="btn btn-primary">OK</button>
                                </div>
                            </div><!-- /.modal-content -->
                        </div><!-- /.modal-dialog -->
                    </div><!-- /.modal -->
                </div>
            </div>
        </div>
    </body>
</html>
