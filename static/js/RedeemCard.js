document.getElementById('checkButton').addEventListener('click', function() {
    const codeInput = document.getElementById('code');
    const errorLabel = document.getElementById('errorLabel');
    const regex = /^[A-Z]{4}-[A-Z]{3}-[A-Z]{3}-[A-Z]{4}$/;

    if (!regex.test(codeInput.value.toUpperCase())) {
        errorLabel.textContent = "Invalid format! Please use XXXX-XXX-XXX-XXXX.";
        errorLabel.style.display = 'block';
        setTimeout(() => {
            errorLabel.style.display = 'none';
        }, 3000);
    } else {
        errorLabel.style.display = 'none';
        let g_card;
        $.ajax({
            url: '/api/reddemgiftcard',
            method: 'GET',
            success: function(data) {
                g_card = data; 
                if (g_card) {
                    if (codeInput.value.toUpperCase() === g_card['dis_code'].toUpperCase()) {
                        if (g_card["usable"] === true) {
                            errorLabel.textContent = "Redeem complete!";
                            setTimeout(() => {
                                errorLabel.style.display = 'none';
                            }, 3000);
                            errorLabel.style.display = 'block';
                            g_card["usable"] = false;
                            $.ajax({
                                url: '/api/reddemgiftcard',
                                method: 'PUT',
                                contentType: 'application/json',
                                data: JSON.stringify(g_card),
                                success: function() {
                                    // Handle success if needed
                                }
                            });
                        } else {
                            errorLabel.textContent = "Already used!";
                            setTimeout(() => {
                                errorLabel.style.display = 'none';
                            }, 3000);
                            errorLabel.style.display = 'block';
                        }
                    } else {
                        errorLabel.textContent = "Invalid code!";
                        setTimeout(() => {
                            errorLabel.style.display = 'none';
                        }, 3000);
                        errorLabel.style.display = 'block';
                    }
                } else {
                    errorLabel.textContent = "You don't have a card!";
                    setTimeout(() => {
                        errorLabel.style.display = 'none';
                    }, 3000);
                    errorLabel.style.display = 'block';
                }
            },
            error: function() {
                errorLabel.textContent = "Error retrieving the card!";
                setTimeout(() => {
                    errorLabel.style.display = 'none';
                }, 3000);
                errorLabel.style.display = 'block';
            }
        });
    }
});
