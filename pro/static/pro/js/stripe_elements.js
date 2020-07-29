const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
const stripeClientSecret = $('#id_client_secret').text().slice(1, -1);
const stripe = Stripe(stripe_public_key);
const elements = stripe.elements();


var style = {
    base: {
        color: '#32325d',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
const card = elements.create("card", {style: style});
card.mount("#card-element");

card.addEventListener("change", function (event) {
    let errorDiv = document.getElementById("card-errors");
    if (event.error) {
        let html = `
            <span class="icon text-danger" role="alert">
            <i class="fas fa-times"></i>
            </span>
            <span class="text-danger">${event.error.message}</span>`;

        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Submit payment
var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({'disabled': true});
    $('#submit-button').attr('disabled', true)
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function (result) {
        if (result.error) {
            let errorDiv = document.getElementById("card-errors");
            let html = `
                <span class="icon text-danger" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span class="text-danger">${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({'disabled': false});
            $('#submit-button').attr('disabled', false)
        } else {
            // The payment has been processed!
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});
