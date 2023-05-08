async function deleteClient(clientId, message) {
  try {
    const response = await fetch(`/api/v1/clients/${clientId}`, {
      method: 'DELETE'
    });

    const result = await response.json();

    if (response.ok) {
      console.log(result);
      location.reload();
    } else {
      console.error(result);
      message.textContent = 'При удалении записи произошла ошибка, обратитесь к администратору';
    }
  } catch (error) {
    console.error(error);
  }
}

