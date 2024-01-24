console.log("hello world")

var update_btn = document.getElementsByClassName("update-cart");
console.log(update_btn)
let i;

for(i=0; i<update_btn.length;i++){
    update_btn[i].addEventListener('click', function(){
        var product_id = this.dataset.product;
        var action = this.dataset.action;

        console.log("user",user)
        if(user == "AnonymousUser"){
            addCookie(product_id, action)
            
        }
        else{
           add_cart(product_id,action)
        }
       
        
    })
}


function addCookie(product_id, action){
    console.log('not logged in ')
    
    if(action == "add"){
        if(cart[product_id] == undefined){
            cart[product_id] = {'quantity': 1}
        }
        else{
            cart[product_id]['quantity'] +=1
        }
    }
    if(action == "remove"){
        cart[product_id]['quantity'] -=1
        if(cart[product_id]['quantity'] <= 0){
            console.log('remove item')
            delete cart[product_id]
        }
    }
    console.log('cart: ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) +";domain=;path=/"
    location.reload()
    

}




function add_cart(product_id, action){

    url ="/update_item/"

    fetch(url,{
        method:"POST",
        headers:{
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body:JSON.stringify({"product_id":product_id, "action":action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) =>{
        console.log("data",data)
        location.reload()
    })
        
    
    
}







// new 

