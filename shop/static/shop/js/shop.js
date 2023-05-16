//  error: function(xhr, textStatus, errorThrown) {
//                  Process the error response
//                 $("#response").html(xhr.responseText);
//               }

function generateCartItem(cartItem, product_id, product_name, product_sku, price_per_unit, price, quantity, thumbnail){
    $(cartItem).attr("data-product-id", product_id);
    $(cartItem).find(".cartItemThumbnail").attr("src", thumbnail);
    $(cartItem).find(".cartItemName").text(product_name);
    $(cartItem).find(".cartItemSku").text(product_sku);
    $(cartItem).find(".cartItemPrice-Each").text(price_per_unit);
    $(cartItem).find(".cartItemPrice").text(price);
    $(cartItem).find(".cartItemQuantity").val(quantity);
    $(cartItem).find(".cartItemTotalPrice").text(price * quantity)

    return cartItem;
}


function recalculateCartItem(cartItem, quantityValue){
    let price = parseInt($(cartItem).find(".cartItemPrice").text());
    let totalPrice = price * quantityValue;
    $(cartItem).find(".cartItemTotalPrice").text(totalPrice);
}

function calculateCartTotal(cartModalBody){
    let cartItems = $(cartModalBody).find(".cartItem");
    let cartTotal = 0;
    $.each(cartItems, function(index, cartItem){
        let cartItemTotalPrice = parseInt($(cartItem).find(".cartItemTotalPrice").text());
        cartTotal += cartItemTotalPrice;
    });
    return cartTotal;
}



$(document).ready(function(){
    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    let loginModal = $("#loginModal");
    let wrongLoginInformation = $("#wrongLoginInformation");
    let cartModal = $("#cartModal");
    let cartModalBody = $("#cardModalBody");
    let alert = $("#alert");
    let cartQuantity = 0;
    let cartItemTemplate = $(".cartItem").first().clone();
    cartItemTemplate.removeClass("d-none");
    let cartTotalHolder = $("#cartTotal");
    console.log(cartItemTemplate)

    $(document).on("click", "#openCart", function(e){
        e.preventDefault();
        $(cartModal).modal("show");
    });

    $(loginModal).on('hide.bs.modal', function (e) {
        if($(wrongLoginInformation).hasClass('d-none') === false){
            $(wrongLoginInformation).addClass('d-none');
        }
      });

    $(document).on("click", "#navLogin", function(e){
        e.preventDefault();
        $(loginModal).modal("show");
    });

    $(document).on("click", "#loginBtn", function(e){
        e.preventDefault();
        let username = $("#username").val();
        let password = $("#password").val();
        if(username.trim() === "" || password.trim() === ""){
            // toggle class then wait for 6 seconds and toggle class again
            $(wrongLoginInformation).removeClass("d-none");
            return;
        }
        $.ajax({
            url: 'login-customer/',
            type: 'POST',
            data: {
                'username': username,
                'password': password,
                csrfmiddlewaretoken: csrf_token,
            },
            dataType: 'json',
            success: function(data){
                // refresh
                location.reload();
            },
            error: function(xhr, textStatus, errorThrown) {
                // Process the error response
                $(wrongLoginInformation).removeClass("d-none");
              }
        })
    });

    $(document).on("click", ".quantityBtn", function(e){
        
        let button = $(this);
        let quantityInput = $(button).siblings(".product_quantity");
        let quantityValue = parseInt(quantityInput.val());
        if(button.hasClass("quantityPlus")){
            console.log("Quantity plus clicked and added!")
            quantityValue += 1;
            quantityInput.val(quantityValue);
            return;
        }
        
        if(button.hasClass("quantityMinus")){
            if(quantityValue > 1){
                console.log("Quantity minus clicked and subtracted!")
                quantityValue -= 1;
                quantityInput.val(quantityValue);
            }
            return;
        }
    });

    $(document).on("click", ".cartQuantityBtn", function(e){
        e.preventDefault(e);
        let button = $(this);
        let quantityInput = $(button).siblings(".cartItemQuantity");
        let quantityValue = parseInt(quantityInput.val());
        let cartItem = $(button).closest(".cartItem");
        if(button.hasClass("quantityPlus")){
            console.log("Cart quantity plus clicked and added!")
            quantityValue += 1;
            quantityInput.val(quantityValue);
            recalculateCartItem(cartItem, quantityValue);
        }
        if(button.hasClass("quantityMinus")){
            quantityValue -= 1;
            if(quantityValue === 0){
                cartItem.remove();
                cartQuantity -= 1;
                if(cartQuantity === 0){
                    $(cartModal).modal("hide");
                }
                }
            else{
                quantityInput.val(quantityValue);
                recalculateCartItem(cartItem, quantityValue);
            }
            }   
            cartTotalHolder.text(calculateCartTotal(cartModalBody));
        });

        $(document).on("change", ".cartItemQuantity", function(e){
            let quantityInput = $(this);
            let quantityValue = parseInt(quantityInput.val());
            let cartItem = $(quantityInput).closest(".cartItem");
            recalculateCartItem(cartItem, quantityValue);
            cartTotalHolder.text(calculateCartTotal(cartModalBody));
        });


    $(document).on("click", ".addToCartBtn", function(e){
        console.log('Add to cart clicked')
        let button = $(this);
        let parentCard = $(button).closest(".productCard");
        let thumbnail = $(parentCard).find(".card-productThumbnail").attr("src");
        let product_name = $(parentCard).find(".card-productName").text();
        let product_sku = $(parentCard).find(".card-productSku").text();
        let price_per_unit = $(parentCard).find(".card-pricePerUnit").text();
        let price = parseInt($(parentCard).find(".card-productPrice").text());
        let quantity = parseInt($(parentCard).find(".product_quantity").val());
        let product_id = parseInt($(this).data("product-id"));

        $.ajax({
            url: 'check-product-quantity/',
            type: 'GET',
            data: {
                'product_id': product_id,
                'quantity': quantity,
                csrfmiddlewaretoken: csrf_token,
            },
            dataType: 'json',
            success: function(data){
                existing_cart_items = $(cartModalBody).find(".cartItem");
                // check if id is existing
                for(let i = 0; i < existing_cart_items.length; i++){
                    if(product_id === parseInt($(existing_cart_items[i]).data("product-id"))){
                        console.log('Product already in cart')
                        let existing_item = $(existing_cart_items[i]);
                        let existing_qty_input = $(existing_item).find(".cartItemQuantity");
                        let existing_qty = parseInt(existing_qty_input.val());
                        let new_qty = existing_qty + quantity;
                        existing_qty_input.val(new_qty);
                        recalculateCartItem(existing_item, new_qty);
                        cartTotalHolder.text(calculateCartTotal(cartModalBody));
                        return;
                    }
                }


                cartItem = generateCartItem($(cartItemTemplate).clone(), product_id, 
                                            product_name, product_sku, price_per_unit, 
                                            price, quantity, thumbnail);

                cartModalBody.append(cartItem);
                cartQuantity += 1;
                cartTotalHolder.text(calculateCartTotal(cartModalBody));
            },
            error: function(xhr, textStatus, errorThrown) {
                // Process the error response
                alert.text('There is not enough quantity of this product!. We will contact you shortly!');
                alert.removeClass("d-none");
              }
        })
    });

    $(document).on("click", "#place_orderBtn", function(e){
        cartItems = {};
        let cartItemsList = $(cartModalBody).find(".cartItem");
        for(let i = 0; i < cartItemsList.length; i++){
            let cartItem = $(cartItemsList[i]);
            let product_id = parseInt($(cartItem).data("product-id"));
            let quantity = parseInt($(cartItem).find(".cartItemQuantity").val());
            cartItems[product_id] = quantity;
        }
        $.ajax({
            url: 'create-order/',
            type: 'POST',
            data: {
                'cartItems': JSON.stringify(cartItems),
                csrfmiddlewaretoken: csrf_token,
            },
            dataType: 'json',
            success: function(data){
                // refresh
                location.reload();
            },
            error: function(xhr, textStatus, errorThrown) {
                // get list insufficient_stock_items from response
                alert.text('There was an error in placing your order. Please try again later!');
                alert.removeClass("d-none");
              }
        })
    });


});

// Dynamic heights
// If the height of a modal changes while 
// it is open, you should call 
// myModal.handleUpdate() to readjust the modal’s position in case a scrollbar appears.