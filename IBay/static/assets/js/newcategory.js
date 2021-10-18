function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

jQuery(function($){
    $(document).ready(function(){
        $("#id_category").change(function(){
            $.ajax({
                url:"/product/subcategory/",
                type:"POST",
                data:{category: $(this).val(),},
                success: function(result) {
                    console.log(result);
                    cols = document.getElementById("id_sub_category");
                    cols.options.length = 0;
                    cols.options.add(new Option("SubCategory", "SubCategory"));
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });
        });
        $("#id_sub_category").change(function(){
            $.ajax({
                url:"/product/minicategory/",
                type:"POST",
                data:{subcategory: $(this).val(),},
                success: function(result) {
                    console.log(result);
                    cols = document.getElementById("id_mini_category");
                    cols.options.length = 0;
                    cols.options.add(new Option("MiniCategory", "MiniCategory"));
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });
        });
        
    }); 
});