$(document).ready(function(){
	

	$("#addToCartBtn").on('click', function(){
		var _vm=$(this);
		
		var _productid=$(".product-id").val();
		var _productim=$(".product-image").val();
		var _productitle=$(".product-title").val();
		var _productqty=$("#productQty").val();
		var _producpric=$(".product-price").text();
		
		$.ajax({
			url:'/add-to-cart',
			data:{
				'id':_productid,
				'qty':_productqty,
				'title':_productitle,
				'price':_producpric,
				'image':_productim
				
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
			}
		});

	});


	// Delet Item form Cart Details
	$(document).on('click','.delete-item',function(){ // ඩොට් එහෙම ඉතාම වැදගත බව මතක තබා ගන්න. 
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
				
		$.ajax({
			url:'/delete-from-cart',
			
			data:{
				'id':_pId,								
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
	});	
	


});
// End Document.Ready

var updateBtns = document.getElementsByClassName('update-cart')


for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}