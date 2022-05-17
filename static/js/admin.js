var script = document.createElement('script');
script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);

setTimeout(function(){
    
    $(document).on('click','#id_status',function(){
        var e = document.getElementById("id_status");
        var status = e.value; 
        
        if (status != "Content_Pitching"){
            $(".field-create").css('display','none');
        }else{
            $(".field-create").css('display','block');
        }

        if (status != "Ready_For_Release"){
            $(".field-publish").css('display','none');
        }else{
            $(".field-publish").css('display','block');
        }

    
        
        
    })
},2000)