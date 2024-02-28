var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret_key = $('#id_client_secret_key').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();

var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4',
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', {style: style});
card.mount('#payment-details');

// Display error message if error occurs for card details //
card.addEventListener('change', function(event){
    let errorMessage = document.getElementById('#card-error-message');
    if (event.error){
        let html = `${event.error.message}`;
        $(errorMessage).html(html);
    } else {
        errorMessage.textContent = "";
    }
});