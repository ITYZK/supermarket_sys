function sub() {
    $(document).on('click',".del_good",function(){

            var id = $(this).find('td.id').text();
        
            var name = $(this).find('td.name').text();
        
            var num =$(this).find('td.num').text();
            
            var size =$(this).find('td.size').text();
            
            var price =$(this).find('td.price').text();
            $.ajax({
                url:'/page6/op',
                data:{'id':id,'name':name,'num':num,'size':size,'price':price},
                type:'POST',
                async:false,
                dataType:'json',
                success:function(data) {
                    if (data.flag == 1){
                         document.getElementById('msg').innerHTML="ID: "+id + "修改成功";
                    }
                    else{
                        document.getElementById('msg').innerHTML="ID: "+id + "修改失败";
                    }
                },
            })
        })
};

$(document).ready(function(){

    $(".del_good td").dblclick(function(){
            if ($(this).attr("class") && !$(this).hasClass("id")){
                var txt= $(this).text();
                console.log(txt);
                $(this).text("");
                var input = "<input type='text' id='mod_good'>"
                $(this).append(input);
                $("input#mod_good").focus();
                $("input#mod_good").blur(function(){
                        if($(this).val()==""){
                            $(this).closest("td").text(txt);
                        }else{
                                $(this).closest("td").text($(this).val())
                                }
                })
            }
    })
})
