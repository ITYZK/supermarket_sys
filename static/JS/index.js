
function check_login(){
    var uname = document.getElementById("name");
    var pwd = document.getElementById("password");
    if(uname.value.length == 0){
        document.getElementById("log_err").innerHTML="用户名密码不能为空";
        // console.log(0);
        return false;
    }
    else{
        document.getElementById("log_err").innerHTML="";
        // console.log(1);
        return true;
    }
}
$(function(){
    var can_sub = false;

    $("#reg_name").blur(function(){
        if($(this).val().trim().length == 0 ){
            document.getElementById("reg_tip1").innerHTML="用户名不能为空";
        }
        else{
            var re = /^[a-zA-Z0-9]{3,15}$/;
            if (!re.test($(this).val().trim())){
                document.getElementById("reg_tip1").innerHTML="只能为3-15位数字或字母";

            }else{
                    $.ajax({
                        type:"GET",
                        dataType:"json",
                        url:'/check_name',
                        data:"name="+$(this).val().trim(),
                        async:true,
                        contentType:'application/json;charset=UTF-8',
                        success:function(data){
                            if(data['code'] === 2){
                                $("#reg_tip1").html("用户名已存在")
                                
                            }
                            else{
                                $("#reg_tip1").html("")
                            }
                        }
                    });
                }
            } 
    });
    $("#reg_pwd").blur(function(){
            if ($(this).val().length == 0){
                document.getElementById("reg_tip2").innerHTML="密码不能为空";
                // console.log(0);
                
            }
            else if ( $(this).val().trim().length < 6 || $(this).val().trim().length > 15){
                    document.getElementById("reg_tip2").innerHTML="密码太短";
                    
                }
            else{
                $("#reg_tip2").html("")
            }
    });

    $("#reg_pwd2").blur(function(){
        if($("#reg_pwd").val().trim() != $(this).val().trim()){
            // console.log(1);
            document.getElementById("reg_tip3").innerHTML="两次密码不一致";
        }else{
            $("#reg_tip3").html("")
        }
    });

    $("#phone").blur(function(){
        if($(this).val().trim().length == 0){
            document.getElementById("reg_tip4").innerHTML="手机号不能为空";
            
        }
        else{
            var re = /^1\d{10}$/g;
            if (!re.test($(this).val())){
                document.getElementById("reg_tip4").innerHTML="无效手机号";
            }else{
                $("#reg_tip4").html("")
            }
        }
    })

    $("#email").blur(function(){
        if($(this).val().trim().length == 0){
            document.getElementById("reg_tip5").innerHTML="邮箱不能为空";
            
        }
        else{
            var re = /^[a-z,A-Z,0-9]+@[a-z,A-Z]+.[a-z,A-Z]+$/g;
            if (!re.test($(this).val())){
                document.getElementById("reg_tip5").innerHTML="无效邮箱地址";
                
            }else{
                $("#reg_tip5").html("")
            }
        }
    });

    function check_register(){
        return can_sub;
    }
});


// function LastImage(){
//     var i=Math.floor(Math.random()*12)
//     var doc = document.getElementsByTagName('body');
//     doc[0].setAttribute('background',"./image/bg"+i+".jpg")
    
// }

// function addnewuser(){
//     console.log(1);
//     var pos = document.getElementById('logn');
//     // console.log(pos);
//     pos.style.marginLeft="-100%"; 
//     var pos = document.getElementById('register');
//     pos.style.marginLeft="30%"; 
// }
// function login(){
//     var pos = document.getElementById('logn');
//     pos.style.marginLeft="30%"; 
//     var pos = document.getElementById('register');
//     pos.style.marginLeft="-100%"; 
// }


function NextImage(){
   var i=Math.floor(Math.random()*12);
   var doc = document.getElementsByTagName('body');
   doc[0].setAttribute('background','/static/image/bg'+i+'.jpg');
}

