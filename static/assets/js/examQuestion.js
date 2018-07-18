var experId = '';

window.onload=function() {
    simplemde = new SimpleMDE({
        previewRender: function(plainText, preview) {
            setTimeout(function() {
                markjax(plainText, preview);
            }, 50);
            return preview.innerHTML;
        },
        element: document.getElementById("fieldTest"),
        spellChecker: false,
        indentWithTabs: false
    });

    $('#module').disabled = "disabled";
}


$(document).ready(function(e) {
    var treeData = "{{module}}";
    treeData = treeData.replace(/&quot;/g,'"');
    treeData = jQuery.parseJSON(treeData);
    console.log(treeData);
    var host = window.location.href;
    var d="{{option}}";
    d = d.replace(/&quot;/g,'"');
    d=jQuery.parseJSON(d);
    console.log(d);
    for (i=0;i<d.length;i++) {
        if (d[i].sysid) {
            $('#select').append('<option value="'+d[i].sysid+'"">'+d[i].name+'</option>');
        }
    }

    if (host.indexOf("id")!= -1) {
        var splitArr = host.split("id=");
        experId = splitArr[splitArr.length-1];
        console.log("experId",experId);
        var boxQuestions = "";
        $.ajax({
            type: 'POST',
            url: '{% url 'experDetail' %}',
            data: {'id': experId},
            dataType: 'text',
            success: function(msg) {
                msg=msg.replace(/&quot;/g,'"');
                msg=jQuery.parseJSON(msg);
                console.log(msg);
                document.getElementById("name").value = msg.experinfo[0].name;
                document.getElementById("detail").value = msg.experinfo[0].introduction;
                document.getElementById("timeRange").value = msg.experinfo[0].duration;
                document.getElementById("fieldTest").value = msg.experinfo[0].detail;
                document.getElementById('yd_box').innerHTML = msg.experinfo[0].examQuOrigion;


                $(".yd_box").find(".movie_box").each(function(i, movie_box){
                    console.log(movie_box);
                    $(movie_box).hover(function() {
                        var html_cz = "<div class='kzqy_czbut'><a href='javascript:void(0)' class='sy'>上移</a><a href='javascript:void(0)'  class='xy'>下移</a><a href='javascript:void(0)'  class='bianji'>编辑</a><a href='javascript:void(0)' class='del' >删除</a></div>"
                        $(this).css({
                            "border": "1px solid #0099ff"
                        });
                        $(this).children(".wjdc_list").after(html_cz);
                        }, function() {
                        $(this).css({
                            "border": "1px solid #fff"
                        });
                        $(this).children(".kzqy_czbut").remove();
                            //$(this).children(".dx_box").hide(); 
                    });
                });


                var receiveModuleId = msg.experinfo[0].parent_id;
                var receiveCategoryId = '';
                var d="{{option}}";
                d = d.replace(/&quot;/g,'"');
                d=jQuery.parseJSON(d);
                
                for (var z=0;z<treeData.length;z++) {
                    for (var x=0;x<treeData[z].nodes.length;x++) {
                        if (treeData[z].nodes[x].sysid == receiveModuleId) {
                            receiveCategoryId = treeData[z].sysid;
                            document.getElementById("select").value = receiveCategoryId;
                            for (var i=0;i<treeData[z].nodes.length;i++) {
                                $('#module').append('<option value="'+treeData[z].nodes[i].sysid+'"">'+treeData[z].nodes[i].text+'</option>');
                            }
                            document.getElementById("module").value = receiveModuleId;
                            return;
                        }
                    }
                }


            }
        });
    } 
    else {
        experId = '';
    }


    $('#select').change(function() {
        var category = $('.parent_id option:selected').val();
        var moduleText = document.getElementById("module");
        moduleText.options.length = 0;
        for (var i=0;i<treeData.length;i++) {
            if (treeData[i].sysid == category) {
                if (treeData[i].nodes) {
                    for (var j=0;j<treeData[i].nodes.length;j++) {
                        $('#module').append('<option value="'+treeData[i].nodes[j].sysid+'"">'+treeData[i].nodes[j].text+'</option>');
                    }
                } 
                else {
                    alert('该体系下无模块，请先添加模块！');
                    return;
                }
            }
        }
    });
    var experData = "{{experinfo}}";
    experData = experData.replace(/&quot;/g,'"');
   

    $('#addquerstions').change(function() {

        // debugger
        var index = $(this).val(); //选择添加问题的类型
        if (index == "-1") {
            return;
        }

        var movie_box = '<div class="movie_box" style="border: 1px solid rgb(255, 255, 255);"></div>';
        var Grade = $(".yd_box").find(".movie_box").length + 1;

        switch (index) {
            case "0": //单选
            case "1": //多选
            case "2": //问答
                var wjdc_list = '<ul class="wjdc_list"></ul>'; //问答 单选 多选
                var danxuan = "";
                if (index == "0") {
                    danxuan = '【单选】';
                } else if (index == "1") {
                    danxuan = '【多选】';
                } else if (index == "2") {
                    danxuan = '【填空】';
                }
                
                wjdc_list = $(wjdc_list).append(' <li><div class="tm_btitlt"><i class="nmb">' + Grade + '</i>. <i class="btwenzi">请编辑问题？</i><span class="tip_wz">' + danxuan + '</span></div></li>');
                if (index == "2") {
                    wjdc_list = $(wjdc_list).append('<li>  <label> <textarea name="" cols="" rows="" class="input_wenbk btwen_text btwen_text_dx" placeholder="答案" ></textarea></label> </li>');
                }
                movie_box = $(movie_box).append(wjdc_list);
                movie_box = $(movie_box).append('<div class="dx_box" data-t="' + index + '"></div>');

                break;

        }

        $(movie_box).hover(function() {
            var html_cz = "<div class='kzqy_czbut'><a href='javascript:void(0)' class='sy'>上移</a><a href='javascript:void(0)'  class='xy'>下移</a><a href='javascript:void(0)'  class='bianji'>编辑</a><a href='javascript:void(0)' class='del' >删除</a></div>"
            $(this).css({
                "border": "1px solid #0099ff"
            });
            $(this).children(".wjdc_list").after(html_cz);
            }, function() {
            $(this).css({
                "border": "1px solid #fff"
            });
            $(this).children(".kzqy_czbut").remove();
                //$(this).children(".dx_box").hide(); 
        });
        $(".yd_box").append(movie_box);

    });

    //鼠标移上去显示按钮
    $(".movie_box").hover(function() {
        var html_cz = "<div class='kzqy_czbut'><a href='javascript:void(0)' class='sy'>上移</a><a href='javascript:void(0)'  class='xy'>下移</a><a href='javascript:void(0)'  class='bianji'>编辑</a><a href='javascript:void(0)' class='del' >删除</a></div>"
        $(this).css({
            "border": "1px solid #0099ff"
        });
        $(this).children(".wjdc_list").after(html_cz);
    }, function() {
        $(this).css({
            "border": "1px solid #fff"
        });
        $(this).children(".kzqy_czbut").remove();
        //$(this).children(".dx_box").hide(); 
    });

    //下移
    $('#myTabContent').on('click', '.xy', function() {
        //文字的长度 
        var leng = $(".yd_box").children(".movie_box").length;
        var dqgs = $(this).parent(".kzqy_czbut").parent(".movie_box").index();

        if(dqgs < leng - 1) {
            var czxx = $(this).parent(".kzqy_czbut").parent(".movie_box");
            var xyghtml = czxx.next().html();
            var syghtml = czxx.html();
            czxx.next().html(syghtml);
            czxx.html(xyghtml);
            //序号
            czxx.children(".wjdc_list").find(".nmb").text(dqgs + 1);
            czxx.next().children(".wjdc_list").find(".nmb").text(dqgs + 2);
        } else {
            alert("到底了");
        }
    });
    //上移
    $('#myTabContent').on('click', '.sy', function() {
        //文字的长度 
        var leng = $(".yd_box").children(".movie_box").length;
        var dqgs = $(this).parent(".kzqy_czbut").parent(".movie_box").index();
        if(dqgs > 0) {
            var czxx = $(this).parent(".kzqy_czbut").parent(".movie_box");
            var xyghtml = czxx.prev().html();
            var syghtml = czxx.html();
            czxx.prev().html(syghtml);
            czxx.html(xyghtml);
            //序号
            czxx.children(".wjdc_list").find(".nmb").text(dqgs + 1);
            czxx.prev().children(".wjdc_list").find(".nmb").text(dqgs);

        } else {
            alert("到头了");
        }
    });
    //删除
    $('#myTabContent').on('click', '.del', function() {
        var czxx = $(this).parent(".kzqy_czbut").parent(".movie_box");
        var zgtitle_gs = czxx.parent(".yd_box").find(".movie_box").length;
        var xh_num = 1;
        //重新编号
        czxx.parent(".yd_box").find(".movie_box").each(function() {
            $(".yd_box").children(".movie_box").eq(xh_num).find(".nmb").text(xh_num);
            xh_num++;
            //alert(xh_num);
        });
        czxx.remove();
    });

    //编辑
    $('#myTabContent').on('click', '.bianji', function() {
        //编辑的时候禁止其他操作   
        $(this).siblings().hide();
        //$(this).parent(".kzqy_czbut").parent(".movie_box").unbind("hover"); 
        var dxtm = $(".dxuan").html();
        var duoxtm = $(".duoxuan").html();
        var tktm = $(".tktm").html();
        var jztm = $(".jztm").html();
        //接受编辑内容的容器
        var dx_rq = $(this).parent(".kzqy_czbut").parent(".movie_box").find(".dx_box");
        var title = dx_rq.attr("data-t");
        //alert(title);
        //题目选项的个数
        var timlrxm = $(this).parent(".kzqy_czbut").parent(".movie_box").children(".wjdc_list").children("li").length;

        //单选题目
        if(title == 0) {
            dx_rq.show().html(dxtm);
            //模具题目选项的个数
            var bjxm_length = dx_rq.find(".title_itram").children(".kzjxx_iteam").length;
            var dxtxx_html = dx_rq.find(".title_itram").children(".kzjxx_iteam").html();
            //添加选项题目
            for(var i_tmxx = bjxm_length; i_tmxx < timlrxm - 1; i_tmxx++) {
                dx_rq.find(".title_itram").append("<div class='kzjxx_iteam'>" + dxtxx_html + "</div>");
            }
            //赋值文本框 
            //题目标题
            var texte_bt_val = $(this).parent(".kzqy_czbut").parent(".movie_box").find(".wjdc_list").children("li").eq(0).find(".tm_btitlt").children(".btwenzi").text();
            dx_rq.find(".btwen_text").val(texte_bt_val);
            //遍历题目项目的文字
            var bjjs = 0;
            $(this).parent(".kzqy_czbut").parent(".movie_box").find(".wjdc_list").children("li").each(function() {
                //可选框框
                var ktksfcz = $(this).find("input").hasClass("wenb_input");
                if(ktksfcz) {
                    var jsxz_kk = $(this).index();
                    dx_rq.find(".title_itram").children(".kzjxx_iteam").eq(jsxz_kk - 1).find("label").remove();
                }
                //题目选项
                var texte_val = $(this).find("span").text();
                dx_rq.find(".title_itram").children(".kzjxx_iteam").eq(bjjs - 1).find(".input_wenbk").val(texte_val);
                bjjs++

            });
        }
        //多选题目  
        if(title == 1) {
            dx_rq.show().html(duoxtm);
            //模具题目选项的个数
            var bjxm_length = dx_rq.find(".title_itram").children(".kzjxx_iteam").length;
            var dxtxx_html = dx_rq.find(".title_itram").children(".kzjxx_iteam").html();
            //添加选项题目
            for(var i_tmxx = bjxm_length; i_tmxx < timlrxm - 1; i_tmxx++) {
                dx_rq.find(".title_itram").append("<div class='kzjxx_iteam'>" + dxtxx_html + "</div>");
                //alert(i_tmxx);
            }
            //赋值文本框 
            //题目标题
            var texte_bt_val = $(this).parent(".kzqy_czbut").parent(".movie_box").find(".wjdc_list").children("li").eq(0).find(".tm_btitlt").children(".btwenzi").text();
            dx_rq.find(".btwen_text").val(texte_bt_val);
            //遍历题目项目的文字
            var bjjs = 0;
            $(this).parent(".kzqy_czbut").parent(".movie_box").find(".wjdc_list").children("li").each(function() {
                //可选框框
                var ktksfcz = $(this).find("input").hasClass("wenb_input");
                if(ktksfcz) {
                    var jsxz_kk = $(this).index();
                    dx_rq.find(".title_itram").children(".kzjxx_iteam").eq(jsxz_kk - 1).find("label").remove();
                }
                //题目选项
                var texte_val = $(this).find("span").text();
                dx_rq.find(".title_itram").children(".kzjxx_iteam").eq(bjjs - 1).find(".input_wenbk").val(texte_val);
                bjjs++

            });
        }
        //填空题目
        if(title == 2) {
            dx_rq.show().html(tktm);
            //赋值文本框 
            //题目标题
            var texte_bt_val = $(this).parent(".kzqy_czbut").parent(".movie_box").find(".wjdc_list").children("li").eq(0).find(".tm_btitlt").children(".btwenzi").text();
            dx_rq.find(".btwen_text").val(texte_bt_val);
        }
        
    });

    //增加选项  
    $('#myTabContent').on('click', '.zjxx', function() {
        var zjxx_html = $(this).prev(".title_itram").children(".kzjxx_iteam").html();
        $(this).prev(".title_itram").append("<div class='kzjxx_iteam'>" + zjxx_html + "</div>");
    });

    //删除一行 
    $('#myTabContent').on('click', '.del_xm', function() {
        //获取编辑题目的个数
        var zuxxs_num = $(this).parent(".kzjxx_iteam").parent(".title_itram").children(".kzjxx_iteam").length;
        if(zuxxs_num > 1) {
            $(this).parent(".kzjxx_iteam").remove();
        } else {
            alert("至少保留一个选项");
        }
    });
    //取消编辑
    $('#myTabContent').on('click', '.dx_box .qxbj_but', function() {
        $(this).parent(".bjqxwc_box").parent(".dx_box").empty().hide();
        $(".movie_box").css({
            "border": "1px solid #fff"
        });
        $(".kzqy_czbut").remove();
        //            
    });
    // body...
    //完成编辑（编辑）
    $('#myTabContent').on('click', '.swcbj_but', function() {

        var jcxxxx = $(this).parent(".bjqxwc_box").parent(".dx_box"); //编辑题目区
        var querstionType = jcxxxx.attr("data-t"); //获取题目类型

        switch(querstionType) {
            case "0": //单选
            case "1": //多选  
                //编辑题目选项的个数
                var bjtm_xm_length = jcxxxx.find(".title_itram").children(".kzjxx_iteam").length; //编辑选项的 选项个数
                var xmtit_length = jcxxxx.parent(".movie_box").children(".wjdc_list").children("li").length - 1; //题目选择的个数

                //赋值文本框 
                //获取问题题目
                var texte_bt_val_bj = jcxxxx.find(".btwen_text").val(); 
                if (!texte_bt_val_bj) {
                    alert("未编辑问题");
                    return;
                }
                //将修改过的问题题目展示
                jcxxxx.parent(".movie_box").children(".wjdc_list").children("li").eq(0).find(".tm_btitlt").children(".btwenzi").text(texte_bt_val_bj); 

                //删除选项
                for(var toljs = xmtit_length; toljs > 0; toljs--) {
                    jcxxxx.parent(".movie_box").children(".wjdc_list").children("li").eq(toljs).remove();
                }

                //遍历题目项目
                var bjjs_bj = 0;
                var tureAns = -1;
                jcxxxx.children(".title_itram").children(".kzjxx_iteam").each(function() {
                    //题目选项
                    var texte_val_bj = $(this).find(".input_wenbk").val(); //获取填写信息
                    if(!texte_val_bj){
                        alert("未编辑选项");
                        return;
                    }

                    var inputType = 'radio';
                    //jcxxxx.parent(".movie_box").children(".wjdc_list").children("li").eq(bjjs_bj + 1).find("span").text(texte_val_bj);
                    if(querstionType == "1") {
                        inputType = 'checkbox';
                    }
                    var li = '<li class="options"><label><input name="a" type="' + inputType + '" value=""><span>' + texte_val_bj + '</span></label></li>';
                    jcxxxx.parent(".movie_box").children(".wjdc_list").append(li);

                    bjjs_bj++
                    //正确答案 
                    var kxtk_yf = $(this).find(".fxk").is(':checked');
                    if(kxtk_yf) {
                        //第几个被勾选
                        var jsxz = $(this).index();
                        tureAns = jsxz;
                        jcxxxx.parent(".movie_box").children(".wjdc_list").children("li").eq(jsxz + 1).find("input").attr("checked", "checked");
                        // jcxxxx.parent(".movie_box").children(".wjdc_list").children("li").eq(jsxz + 1).find("span").after("<input name='' type='text' class='wenb_input'>");
                    }
                });
                if (tureAns == -1) {
                    alert("未填写正确答案，请填写正确答案");
                    return;
                }

                break;
            case "2":
                var texte_bt_val_bj = jcxxxx.find(".btwen_text").val(); //获取问题题目
                if (!texte_bt_val_bj) {
                    alert("未编辑问题");
                    return;
                }
                var ans = jcxxxx.parent(".movie_box").children(".wjdc_list").children("li").eq(1).find("label").find("textarea").val();
                if (!ans) {
                    alert("未填写正确答案，请填写正确答案");
                    return;
                }
                jcxxxx.parent(".movie_box").children(".wjdc_list").children("li").eq(0).find(".tm_btitlt").children(".btwenzi").text(texte_bt_val_bj); //将修改过的问题题目展示
                break;
        }
        //清除     
        $(this).parent(".bjqxwc_box").parent(".dx_box").empty().hide();

        $(".kzqy_czbut").remove();
    });

});

function submitInfo2(){
    var mdPlain = simplemde.value();
    console.log(mdPlain);
    // var mdText = simplemde.markdown(mdPlain);
    var mdText = mdPlain;
    console.log(mdText);
   
    if (!$(".name").val()) {
        alert("实验名称必填！");
        return;
    } else if (!$(".detail").val()) {
        alert("实验简介必填！");
        return;
    } else if (!$(".timeRange").val()) {
        alert("实验时长必填！");
        return;
    } else if (!mdText) {
        alert("实验描述必填! ");
        return;
    } else if (!$('.module option:selected').val()) {
        alert("实验体系模块必填！");
        return;
    }
    name = $(".name").val();
    detail = $('.detail').val();
    timeRange = $('.timeRange').val();
    parent_id = $('.parent_id option:selected').val();
    module_id = $('.module option:selected').val();

    var answers = [];
    var examQuestionsOrigion = $(".yd_box").html();
    $(".yd_box").children(".movie_box").each(function(index, question){  
        var questionHTML = $(this).html();      
        var questionType = $(this).find(".tip_wz").text();
        var answer = {};            
        if (questionType == "【单选】") {
            questionType = "0";
        }else if (questionType == "【多选】") {
            questionType = "1";
        }else{
            questionType = "2";
        }
        answer['questionType'] = questionType;
        answer['gt'] = [];
        switch (questionType){
            case "0":
            case "1":
                $(this).find(".options").each(function(i, option){
                    var isAnswer = $(this).find("input[name=a]").prop("checked");
                    if (isAnswer) {
                        answer['gt'].push(i);
                    }
                    $(this).find("input[name=a]").removeAttr("checked");
                });
                // $(this).find(".options").prop("checked", false);
                break;
            case "2":
                var ansString = $(this).find("textarea").val();
                answer['gt'].push(ansString);
                $(this).find("textarea").val("");
                break;
        }
        answers.push(answer);

    });
    answers = JSON.stringify(answers);

    var examQuestions = $(".yd_box").html();
    console.log(examQuestions);
    console.log(answers);
    console.log(examQuestionsOrigion);

    $.ajax({
        type: 'post',
        url: "{% url 'experEdit' %}",
        data: {'name':name,'introduction':detail,'duration':timeRange,'detail':mdText, 'parent_id':module_id, 'experId':this.experId, 'examQuestionsOrigion':examQuestionsOrigion, 'examQuestions':examQuestions, 'answers':answers},
        dataType:'text',
        success:function(msg) {
            console.log(msg);
            window.location.href = "{% url 'experList' 1 %}";
        }
    });

}
