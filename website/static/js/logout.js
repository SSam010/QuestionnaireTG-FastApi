 document.getElementById('logout-form').addEventListener('submit', function(event) {
   event.preventDefault(); // отменяем стандартное действие формы
   let xhr = new XMLHttpRequest();
   xhr.open('POST', this.action, true);
   xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
   xhr.onload = function() {
     if (xhr.status >= 200 && xhr.status < 300) { // если запрос успешен, то делаем редирект
       window.location.href = '/'; // здесь можно указать нужный адрес
     }
   };
   xhr.send(); // отправляем запрос
 });
