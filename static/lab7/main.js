function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(response => response.json())
        .then(films => {
            const tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            
            films.forEach((film, i) => {
                const tr = document.createElement('tr');
                
                const tdTitleRus = document.createElement('td');
                tdTitleRus.textContent = film.title_ru;

                const tdTitle = document.createElement('td');
                // Просто всегда показываем оригинальное название
                tdTitle.textContent = film.title || film.title_ru;

                const tdYear = document.createElement('td');
                tdYear.textContent = film.year || '';

                const tdActions = document.createElement('td');
                const editBtn = document.createElement('button');
                editBtn.textContent = 'редактировать';
                editBtn.onclick = () => editFilm(i);

                const delBtn = document.createElement('button');
                delBtn.textContent = 'удалить';
                delBtn.onclick = () => deleteFilm(i, film.title_ru);

                tdActions.append(editBtn, delBtn);
                tr.append(tdTitleRus, tdTitle, tdYear, tdActions);
                tbody.append(tr);
            });
        });
}
function deleteFilm(id, title) {
    if(!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList(); // Перезагружаем таблицу после удаления
        });
}

function editFilm(id) {
    // Очищаем ошибки при открытии модального окна
    document.getElementById('description_error').innerText = '';
    
    // Заполняем форму данными фильма для редактирования
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function (data) {
            return data.json();
        })
        .then(function (film) {
            document.getElementById('id').value = id;
            document.getElementById('title').value = film.title;
            document.getElementById('title_ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        });
}

function addFilm() {
    // Очищаем форму и ошибки для добавления нового фильма
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    document.getElementById('description_error').innerText = '';
    showModal();
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const title_ru = document.getElementById('title_ru').value.trim();
    const title = document.getElementById('title').value.trim();
    const year = document.getElementById('year').value;
    const description = document.getElementById('description').value.trim();
    
    console.log('Отправляемые данные:', {  // Добавим console.log
        title_ru: title_ru,
        title: title,
        year: year,
        description: description
    });
    
    const film = {
        title_ru: title_ru,
        title: title,
        year: parseInt(year) || 0,
        description: description
    };

    const url = '/lab7/rest-api/films/' + (id === '' ? '' : id);
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(film)
    })
    .then(function(response) {
        console.log('Статус ответа:', response.status);  // Добавим
        if (response.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return response.json();
    })
    .then(function(errors) {
        if (errors && errors.description) {
            document.getElementById('description_error').innerText = errors.description;
        } else if (errors && errors.title_ru) {
            alert(errors.title_ru);
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
    });
}
// Запускаем заполнение таблицы при загрузке страницы
document.addEventListener('DOMContentLoaded', fillFilmList);