// Asynchronous change of attribute "is_processed"

function updateProcessed(clientId, isChecked) {
    fetch(`/api/v1/clients/${clientId}/processed`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            is_processed: isChecked
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}
