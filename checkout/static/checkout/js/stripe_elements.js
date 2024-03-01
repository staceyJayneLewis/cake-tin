var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
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
    var errorMessage = document.getElementById('card-error-message');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorMessage).html(html);
    } else {
        errorMessage.textContent = '';
    }
});

// On submit handle form // 
var form = document.getElementById('checkout-form');

form.addEventListener('submit', function (event) {
    event.preventDefault();
    card.update({
        'disabled': true
    });
    $('#submit-btn').attr('disabled', true);
    stripe.confirmCardPayment(client_secret, {
        payment_method: {
            card: card,
        }
    }).then(function (result) {
        if (result.error) {
            let errorMessage = document.getElementById('card-error-message');
            let html = `${result.error.message}`;
            $(errorMessage).html(html);
            card.update({
                'disabled': false
            });
            $('#submit-btn').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});