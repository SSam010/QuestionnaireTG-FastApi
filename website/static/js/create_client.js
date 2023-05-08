function createClient(message) {
  const form = document.getElementById("add-client-form");

  // используем вложеную функцию с очисткой ивентлупа, чтобы избежать дублирования выполнения
  async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    try {
      const response = await fetch('/api/v1/clients/add_new_client', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(Object.fromEntries(formData))
      });

      const result = await response.json();

      if (response.ok) {
        console.log(result);
        message.textContent = 'Запись успешно добавлена';
        console.log(result);
      } else {
        console.error(result);
        message.textContent = 'Ошибка при добавлении записи';
        console.error(result);
      }
    } catch (error) {
      console.error(error);
    }

    form.removeEventListener('submit', handleSubmit);
  }

  // добавление слушателя событий
  form.addEventListener('submit', handleSubmit);
}
