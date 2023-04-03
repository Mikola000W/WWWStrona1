

const addToCartsForms = document.querySelectorAll(".addToCartForm");

function handleSubmit(forms) {
    forms.forEach(form => {
        form.addEventListener("submit", e => {
            e.preventDefault();

            const item_id = form.id.split('-')[1]

            fetch(`/add-to-cart/${item_id}`, {
                method: 'GET',
            })
                .then(response => response.json())
                .then(data => {
                    form.reset();
                    alert(data['message'])
                })
                .catch((error) => {
                    console.error('Error:', error);
                });

        })
    })
}

handleSubmit(addToCartsForms)