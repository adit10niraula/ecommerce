// var update_btn = document.getElementsByClassName('update-cart')

// for(var i = 0; i<update_btn.length; i++){
//     update_btn[i].addEventListener("click", function(){
//         product_id = this.dataset.product 
//         action = this.dataset.action

//         console.log('product_id', product_id)
//         console.log('action', action)
//         if(user == "AnonymousUser"){
//             console.log("user not logged in ")
//         }
//         else{
//             addItemCart(product_id, action)
//         }

//     })
// }

// function addItemCart(product_id, action){
//     console.log("item added success")

//     url ="/update_items/"

//     fetch(url, {
//         method:"POST",
//         headers:{
//             "Content-Type": "application/json",
//             "X-CSRFToken": csrftoken
//         },
//         body:JSON.stringify({'product_id':product_id, 'action':action})
//     })
//     .then((response)=>{
//         return response.json()
//     })
//     .then((data)=>{
//         console.log("data", data)
//         location.reload()
//     })
// }
