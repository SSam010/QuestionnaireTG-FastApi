Привет тебе, вольный странник!

## **!!! ПРОЕКТ НАХОДИТСЯ В ПРОЦЕССЕ СОЗДАНИЯ, ПРОСЬБА НЕ ИСПОЛЬЗОВАТЬ !!!**

### **На текущем этапе убедительная просьба не воспринимать проект как завершенный и готовый к релизу. Это всего лишь промежуточный вариант, выложенный на GitHub для ознакомления!**

Проект представляет собой совокупность работы асинхронного TG бота в связки с FastAPI.

На данном этапе функциональность ресурса предназначена для следующих задач:

1) Работа асинхронного TG бота с целью анкетирования клиентов. 
- На данном этапе TG bot задает последовательные вопросы с занесением их в БД(в проекте используется PostgreSQL);
- Дублирование заполненных данных в виде сообщения администратору бота;
- настроено логирование;


    В ближайшем обновлении будет реализована возможность общаться с каждым клиентом непосредственно из чата бота.

2) Работа веб-приложение на FastAPI для удобной работы с данными.
- на данном этапе созданы страницы для работы с данными, реализованы методы их корректировки;
- настроено логирование;


    В ближайшем обновлении будет внедрена регистрация и авторизация пользователя с ограничем доступа к ресурсу.


Проект будет поддерживать развертку в docker.

