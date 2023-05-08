function editRecord(clientId) {
  // Отправляем AJAX-запрос на сервер для получения данных
  fetch(`/api/v1/clients/${clientId}`)
    .then(response => response.json())
    .then(data => {
      const myForm = document.getElementById(`${clientId}`);
      // заполняем форму для редактирования текущими данными
      myForm.elements.namedItem("tg_id").value = data.data[0].Client.tg_id;
      myForm.elements.namedItem("tg_link").value = data.data[0].Client.tg_link;
      myForm.elements.namedItem("name").value = data.data[0].Client.name;
      myForm.elements.namedItem("investment_time").value = data.data[0].Client.investment_time;
      myForm.elements.namedItem("investment_tools").value = data.data[0].Client.investment_tools;
      myForm.elements.namedItem("investment_amount").value = data.data[0].Client.investment_amount;
      myForm.elements.namedItem("meeting").value = data.data[0].Client.meeting;
      myForm.elements.namedItem("contact_number").value = data.data[0].Client.contact_number;
    })
    .catch(error => console.error(error));
}


function updateClient(clientId, message) {
  const form = document.getElementById(clientId);

  // используем вложеную функцию с очисткой ивентлупа, чтобы избежать дублирования выполнения
  async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    try {
      const response = await fetch(`/api/v1/clients/${clientId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(Object.fromEntries(formData))
      });

      const result = await response.json();

      if (response.ok) {
        console.log(result);
        location.reload();
      } else {
        console.error(result);
        message.textContent = 'При обновлении записи произошла ошибка, проверьте правильность заполнения полей';
      }
    } catch (error) {
      console.error(error);
    }

    form.removeEventListener('submit', handleSubmit);
  }

  // добавление слушателя событий
  form.addEventListener('submit', handleSubmit);
}
