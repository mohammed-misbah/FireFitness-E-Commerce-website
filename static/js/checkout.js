$(document).ready(function () {


       $('#razorpay').click(function (e) {
           e.preventDefault();
   
           var address = $(".addres_sel:checked").val();
           var token = $("[name='csrfmiddlewaretoken']").val();
           console.log("hai")
           console.log(address);
           if (address == "") {
               alert("select address")
               return false;
           }
           else {
   
               $.ajax({
                   type: "GET",
                   url: "/Order/proceed-to-pay",
   
                   success: function (response) {
                    l
                       console.log(response);
                   }
               });
               console.log(response.grand_total)
               // swal("Hello world!");
               // console.log("avoo")
               var options = {
                   "key": "rzp_test_tBT9s69IVb6TFk", // Enter the Key ID generated from the Dashboard
                   "amount": 'response.grand_total', // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                   "currency": "INR",
                   "name": "Firefitness",
                   "description": "Thank you for buying",
                   "image": "https://example.com/your_logo",
                   // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                   "handler": function (responseb) {
                       alert(responseb.razorpay_payment_id);
                       data = {
                           "shipping_address": address,
                           "payment_mode": "Paid by Razorpay",
                           "payment_id": responseb.razorpay_payment_id,
                            csrfmiddlewaretoken: token
   
                       },
                       $.ajax({
                           type: "POST",
                           url: " /Order/order_place",
                           data: data,
                          
                           success: function (responsec) {
                               // swal(responsec.status)
                               if (responsec['status'] == 'Your order placed') {
                                   console.log('order placed successfully')
                                   window.location.href = "/Userprofile/my_orders"
                               }
                               
                           }
                       });
   
                   },
                           "prefill": {
                           "name": first_name+" "+last_name,
                           "email": email,
                           "contact": phone
                   },
                       // "notes": {
                       //     "address": "Razorpay Corporate Office"
                       // },
                       "theme": {
                           "color": "#3399cc"
                       }
                   };
                   var rzp1 = new Razorpay(options);
                   rzp1.open();
   
               }
         
           });
   
   });
   
   
