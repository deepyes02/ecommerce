let updateButtons = document.getElementsByClassName('update-cart');

for (let i =0; i<updateButtons.length; i++){
  updateButtons[i].addEventListener('click', function(){
    let productName = this.dataset.product
    //id is automatically set by python as auto feature in every class
    let productId = this.dataset.id
    let action = this.dataset.action
    console.log('ID: ',productId, 'product: ', productName);

    if(user =="AnonymousUser"){
      addCookieItem(productId, action);
      
    } else{
      updateUserOrder(productId, action)
      console.log(user)
    }
  })
}

function addCookieItem(productId, action){
  if (action == 'add'){
      if(cart[productId] == undefined){
        cart[productId] = {'quantity':1}
      } 
      else {
        cart[productId] ['quantity'] += 1;
        }
  }
 
  if (action == 'remove'){
    cart[productId]['quantity'] -= 1;
    window.location.href="{%url 'cart' %}"
        if (cart[productId]['quantity'] <=0){
          console.log("Item should be deleted");
          delete cart[productId];
        }
  }
  console.log('Cart: ', cart);
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
  location.reload();
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}