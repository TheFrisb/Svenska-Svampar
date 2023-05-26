$(window).on("load", function(){
    $("#preload_spinner").remove();
    $("#pageLoader_SpinnerContainer").fadeOut(500, function(){
        $(this).remove();
    }
    );
    $("body").removeClass("preload");
});






function flyProductThumbnailToCart(productCard, cartIcon, cartQuantityHolder){
    var initialOffset = $(productCard).offset();
    function calculateAdjustedPosition() {
        var scrollTop = $(window).scrollTop();
        return {
            top: initialOffset.top - scrollTop,
            left: initialOffset.left
        };
    }

    $(productCard).clone().css({
        'opacity': '1',
        'position': 'absolute',
        'z-index': '11100',
        'box-shadow': '0 0 30px #999999, 0 10px 20px #999999',
        'width': productCard.width(),
        'height': productCard.height(),
        'top': $(productCard).offset().top,
        'left': $(productCard).offset().left
    }).appendTo("body").animate({
        top: $(cartIcon).offset().top,
        left: $(cartIcon).offset().left,
        width: 20,
        height: 20
    }, 200, 'linear', function() {
        $(this).remove();
        $(cartIcon).addClass("cartIconTransform");
        $(cartQuantityHolder).addClass("cartQuantityTransform");
        setTimeout(function(){
            $(cartIcon).removeClass("cartIconTransform");
            $(cartQuantityHolder).removeClass("cartQuantityTransform");
        }, 300);
    });

    $(window).on('scroll', function() {
        var adjustedPosition = calculateAdjustedPosition();
        $(productCard).css({
            top: adjustedPosition.top,
            left: adjustedPosition.left
        });
    });

        return;
}



  
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
    let cartSubtotal = 0;
    let cartVat = 0;
    let cartTotal = 0;
    $.each(cartItems, function(index, cartItem){
        let cartItemTotalPrice = parseInt($(cartItem).find(".cartItemTotalPrice").text());
        cartSubtotal += cartItemTotalPrice;
    });
    cartVat = cartSubtotal * 0.12;
    cartTotal = cartSubtotal + cartVat;

    // format to 2 decimals
    cartSubtotal = cartSubtotal.toFixed(2);
    cartVat = cartVat.toFixed(2);
    cartTotal = cartTotal.toFixed(2);
    $("#cartSubtotal").text(cartSubtotal);
    $("#cartTotal").text(cartTotal);
    $("#cartTotalVat").text(cartVat);

    return;

}


function alert_remove_classes(alert){
    if($(alert).hasClass("alert-success")){
        $(alert).removeClass("alert-success");
    }
    if($(alert).hasClass("alert-danger")){
        $(alert).removeClass("alert-danger");
    }
    if($(alert).hasClass("alert-warning")){
        $(alert).removeClass("alert-warning");
    }
    return 
}


$(document).ready(function(){
    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    let loginModal = $("#loginModal");
    let registerModal = $("#registerModal");
    let wrongLoginInformation = $("#wrongLoginInformation");
    let cartIcon = $("#cart");
    let cartModal = $("#cartModal");
    let cartModalBody = $("#cardModalBody");
    let alert = $("#alert");
    let alert_text = $("#alert_text");
    let cartAlert = $("#cartAlert");
    let cartAlertText = $("#cart_alert_text");
    let cartBanner = $("#cartBanner");
    let cartQuantityHolder = $("#cartQuantity");
    let cartQuantity = parseInt(cartQuantityHolder.text());
    let cartItemTemplate = $(".cartItem").first().clone();
    cartItemTemplate.removeClass("d-none");

    $(document).on("click", "#cart", function(e){
        e.preventDefault();
        if(cartQuantity === 0){
            $(cartBanner).removeClass("d-none");

            // wait for 6 seconds
            setTimeout(function(){
                if(cartBanner.hasClass("d-none") === false){
                    $(cartBanner).addClass("d-none");
                };
            }, 6000);
            
            return;
        }
        else{ 
            $(cartModal).modal("show"); 
        }
        
    });
    $(loginModal).on('shown.bs.modal', function() {
        $('#login_username').focus();
        $(document).on('keyup.login', function(event) {
            if (event.key == 'Enter') {
                $('#loginBtn').click();
            }
            
        });
    })

    $(loginModal).on('hide.bs.modal', function (e) {
        if($(wrongLoginInformation).hasClass('d-none') === false){
            $(wrongLoginInformation).addClass('d-none');
        }
        
        $(document).off('keyup.login');
      });

    $(registerModal).on('shown.bs.modal', function() {
        $('#registrant_business_name').focus();
        $(document).on('keyup.register', function(event) {
            if (event.key == 'Enter') {
                $('#registerBtn').click();
            }
        });
    })

    $(registerModal).on('hide.bs.modal', function (e) {
        $(document).off('keyup.register');
    });
    $(document).on("click", ".close_alert_button", function(e){
        e.preventDefault();
        let closest_alert = $(this).closest(".alert");
        // check if does not have d-none class
        if($(closest_alert).hasClass("d-none") === false){
            $(closest_alert).addClass("d-none");
        }
    });
    $(document).on("click", "#registerBtn", function(e){
        let form_is_valid = true;
        let business_name = $("#registrant_business_name").val();
        let city = $("#registrant_city").val();
        let address = $("#registrant_address").val();
        let contact_person = $("#registrant_contact_person").val();
        let email = $("#registrant_email").val();
        let phone_number = $("#registrant_phone_number").val();
        let business_type = $("input[name='registrant_business_type']:checked").val();
        let registration_note = $("#registrant_comment").val();

        let first_invalid_input = null;
        if(business_name.trim() === ""){
            form_is_valid = false;
            $("#registrant_business_name").addClass("border-danger").focus();

            first_invalid_input = $("#registrant_business_name");
        }
        else{
            $("#registrant_business_name").removeClass("border-danger");
        }

        if(city.trim() === ""){
            form_is_valid = false;
            $("#registrant_city").addClass("border-danger").focus();

            if(first_invalid_input === null){
                first_invalid_input = $("#registrant_city");
            }
        }
        else{
            $("#registrant_city").removeClass("border-danger");
        }

        if(address.trim() === ""){
            form_is_valid = false;
            $("#registrant_address").addClass("border-danger").focus();

            if(first_invalid_input === null){
                first_invalid_input = $("#registrant_address");
            }
        }
        else{
            $("#registrant_address").removeClass("border-danger");
        }

        if(contact_person.trim() === ""){
            form_is_valid = false;
            $("#registrant_contact_person").addClass("border-danger").focus();

            if(first_invalid_input === null){
                first_invalid_input = $("#registrant_contact_person");
            }
        }
        else{
            $("#registrant_contact_person").removeClass("border-danger");
        }

        if(phone_number.trim() === ""){
            form_is_valid = false;
            $("#registrant_phone_number").addClass("border-danger").focus();

            if(first_invalid_input === null){
                first_invalid_input = $("#registrant_phone_number");
            }

        }
        else{
            $("#registrant_phone_number").removeClass("border-danger");
        }

        if(business_type === undefined){
            form_is_valid = false;
            $("#registrant_select_business_typeLabel").addClass("text-danger");

            if(first_invalid_input === null){
                first_invalid_input = $("#registrant_select_business_typeLabel");
            }
        }
        else{
            $("#registrant_select_business_typeLabel").removeClass("text-danger");
        }


        if(email.trim() === ""){
            form_is_valid = false;
            $("#registrant_email").addClass("border-danger").focus();

            if(first_invalid_input === null){
                first_invalid_input = $("#registrant_email");
            }
        }
        else{
            if(email.includes("@") === false){
                form_is_valid = false;

                if(first_invalid_input === null){
                    first_invalid_input = $("#registrant_email");
                }

                if(form_is_valid === true){
                    $("#registrant_email").addClass("border-danger").focus();
                    $("#invalidRegisterForm").html("Invalid email address").removeClass("d-none");
                    $(registerModal).animate({ scrollTop: 0 }, "slow");
                    return;
                }
                else{
                    $("#registrant_email").addClass("border-danger").focus();
                    $("#invalidRegisterForm").html("Fields marked with * are required, also your e-mail address is invalid!").removeClass("d-none");
                    $(registerModal).animate({ scrollTop: 0 }, "slow");
                    return;
                }
            }
            else{
                $("#registrant_email").removeClass("border-danger");
            }
        }

        
        if(form_is_valid === false){
            $("#invalidRegisterForm").html("Fields marked with * are required!  ").removeClass("d-none");
            if(first_invalid_input !== null){
                $(first_invalid_input).focus();
                $(registerModal).animate({ scrollTop: 0 }, "slow");
                console.log($(first_invalid_input))
                console.log($(first_invalid_input).offset().top);
            }
            return;
        }
        $.ajax({
            url: 'shopmanager/register-applicant/',
            type: 'POST',
            data: {
                'business_name': business_name,
                'city': city,
                'address': address,
                'contact_person': contact_person,
                'email': email,
                'phone_number': phone_number,
                'business_type': business_type,
                'registration_note': registration_note,
                csrfmiddlewaretoken: csrf_token,
            },
            dataType: 'json',
            success: function(data){
                $(registerModal).modal("hide");
                // clear all inputs except business type
                if($("#invalidRegisterForm").hasClass("d-none") === false){
                    $("#invalidRegisterForm").addClass("d-none");
                }
                alert_remove_classes(alert);
                $(alert).addClass("alert-success");
                $(alert).removeClass("d-none");
                $(alert_text).text("Your application has been submitted. We will contact you soon.");
                $("html, body").animate({ scrollTop: 0 }, "slow");

                console.log('SUCCESS')
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log(xhr.responseText);
                console.log('error')
                
              }

        })

    });

    $(document).on("click", "#navLogin", function(e){
        e.preventDefault();
        $(loginModal).modal("show");
    });

    $(document).on("click", "#loginBtn", function(e){
        e.preventDefault();
        let username = $("#login_username").val();
        let password = $("#login_password").val();
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
                cartQuantityHolder.text(cartQuantity);
                }
            else{
                quantityInput.val(quantityValue);
                recalculateCartItem(cartItem, quantityValue);
            }
            }   
            calculateCartTotal(cartModalBody);
        });

        $(document).on("change", ".cartItemQuantity", function(e){
            let quantityInput = $(this);
            let quantityValue = parseInt(quantityInput.val());
            let cartItem = $(quantityInput).closest(".cartItem");
            recalculateCartItem(cartItem, quantityValue);
            calculateCartTotal(cartModalBody);
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
                // add border-2 and border-success to parent card and remove after 1 second
                $(parentCard).addClass("border-2 border-success");
                    setTimeout(function(){
                        $(parentCard).removeClass("border-2 border-success");
                }, 700);
                    

                

                let productCardToFly = $(parentCard).closest(".col-12");
                flyProductThumbnailToCart(productCardToFly, cartIcon, cartQuantityHolder);
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
                        calculateCartTotal(cartModalBody);
                        return;
                    }
                }


                cartItem = generateCartItem($(cartItemTemplate).clone(), product_id, 
                                            product_name, product_sku, price_per_unit, 
                                            price, quantity, thumbnail);

                cartModalBody.append(cartItem);
                cartQuantity += 1;
                cartQuantityHolder.text(cartQuantity);
                calculateCartTotal(cartModalBody);
            },
            error: function(xhr, textStatus, errorThrown) {
                // get list of products with not available quantity
                alert_remove_classes(alert);
                alert.addClass("alert-danger");
                alert_text.html('There is not enough quantity of this product!. We will contact you shortly!');
                alert.removeClass("d-none");
                $('html, body').animate({scrollTop:0}, 'slow', function(){
                    if(alert.hasClass("growAlert")){
                        alert.removeClass("growAlert");
                        alert.addClass("growAlert");
                    }
                    else{
                        alert.addClass("growAlert");
                    }
                });
              }
        })
    });

    $(document).on("click", "#place_orderBtn", function(e){
        // add bootsrtap 5 spinner
        let button= $(this);
        button.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');

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

                // get ordered products with price and quantity

                let products = data.products;
                let new_order_html = "Your order has been placed successfully!<br><br>";
                for(let i = 0; i < products.length; i++){
                    let product = products[i];
                    new_order_html += "<strong>" + product.name + " - " + product.quantity + " x " + product.price + " = " + product.total_price + "</strong><br>";
                }
                new_order_html += "<br><strong class='fs-5'>Total: " + data.order_total + "$</strong>";


                $(cartModal).modal("hide");
                button.html('Purchase');
                alert_remove_classes(alert);
                alert.addClass("alert-success");
                alert_text.html(new_order_html);
                alert.removeClass("d-none");
                $('html, body').animate({scrollTop:0}, 'slow', function(){
                    if(alert.hasClass("growAlert")){
                        alert.removeClass("growAlert");
                        alert.addClass("growAlert");
                    }
                    else{
                        alert.addClass("growAlert");
                    }
                });
                cartModalBody.empty();
                cartQuantity = 0;
                cartQuantityHolder.text(cartQuantity);
                calculateCartTotal(cartModalBody);
                

            },
            error: function(xhr, textStatus, errorThrown) {
                button.html('Purchase');
                let products = xhr.responseJSON.insufficient_stock_items;
                let error_product_names = "";
                for(let i = 0; i < products.length; i++){
                    let product_id = parseInt(products[i]);
                    let errorCartItem = $(cartModalBody).find(`.cartItem[data-product-id=${product_id}]`);
                    let errorProductName = $(errorCartItem).find(".cartItemName").text();
                    error_product_names += errorProductName;
                    if(i < products.length - 1){
                        error_product_names += ", ";
                    };
                    errorCartItem.remove();
                    cartQuantity -= 1;
                }
                cartQuantityHolder.text(cartQuantity);
                calculateCartTotal(cartModalBody);
                if(cartQuantity === 0){
                    $(cartModal).modal("hide");
                    alert_remove_classes(alert);
                    alert.addClass("alert-danger");
                    alert_text.html('<span>The following product were removed from your cart due to not enough stock: <span class="fw-bold">' + error_product_names + '</span> . You can still purchase the other ones! We will contact you shortly!</span>');
                    alert.removeClass("d-none");
                    $('html, body').animate({scrollTop:0}, 'slow', function(){
                        if(alert.hasClass("growAlert")){
                            alert.removeClass("growAlert");
                            alert.addClass("growAlert");
                        }
                        else{
                            alert.addClass("growAlert");
                        }
                    });
                }
                else{
                    $(cartModalBody).animate({scrollTop:0}, 'slow');
                    cartAlertText.text('The following product were removed from your cart due to not enough stock: ' + error_product_names + '. You can stil purchase the other ones!. We will contact you shortly!');
                    cartAlert.removeClass("d-none");
                    // check if on top of page
                    if($(cartModalBody).scrollTop() === 0){
                        if(cartAlert.hasClass("growAlert")){
                            cartAlert.removeClass("growAlert");
                            cartAlert.addClass("growAlert");
                        }
                        else{
                            cartAlert.addClass("growAlert");
                        }
                    }


                }
              }
        })
    });

    // $('.collapse').on('shown.bs.collapse', function(e) {
    //     var $card = $(this).closest('.accordion-item');
    //     var $open = $($(this).data('parent')).find('.collapse.show');
        
    //     var additionalOffset = 0;
    //     if($card.prevAll().filter($open.closest('.accordion-item')).length !== 0)
    //     {
    //           additionalOffset =  $open.height();
    //     }
    //     $('html,body').animate({
    //       scrollTop: $card.offset().top - additionalOffset
    //     }, 500);
    //   });


});