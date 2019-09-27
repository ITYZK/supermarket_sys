function is_add(){
    if(document.getElementById("ad_id").value.trim().length == 0){
        console.log(1);
        document.getElementById('msg').innerHTML="id不能为空";
        return false;
    }
    if(document.getElementById("ad_name").value.trim().length == 0){
        document.getElementById('msg').innerHTML="名字不能为空";
        return false;
    }
    if(document.getElementById("ad_num").value.trim().length == 0){
        document.getElementById('msg').innerHTML="数量不能为空";
        return false;
    }else{
        var re = /^[0-9]+$/g;
        if (!re.test(document.getElementById("ad_num").value)){
            document.getElementById('msg').innerHTML="数量只能为数字";
            return false;
        }
    }
    if(document.getElementById("ad_size").value.trim().length == 0){
        document.getElementById('msg').innerHTML="规格不能为空";
        return false;
    }
    if(document.getElementById("ad_price").value.trim().length == 0){
        document.getElementById('msg').innerHTML="价格不能为空";
        return false;
    }
    console.log(5);
        return true;
}