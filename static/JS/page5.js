function sub() {
    $(document).on('click',".del_good",function(){
            var td = $(this).find('td');
            var id = $(this).find('td.id').text();
            var name = $(this).find('td.name').text();
            var num =$(this).find('td.num').text(); 
            var size =$(this).find('td.size').text();       
            var price =$(this).find('td.price').text();
            $.ajax({
                url:'/page5/op',
                data:{'id':id,'name':name,'num':num,'size':size,'price':price},
                type:'POST',
                async:true,
                dataType:'json',
                success:function(data) {
                    if (data.flag == 1){
                         document.getElementById('msg').innerHTML="ID: "+id+"删除成功";
                         td.remove();
                    }
                    else{
                        document.getElementById('msg').innerHTML="ID: "+id+"删除失败";
                    }
                },
               
            })
        })
};