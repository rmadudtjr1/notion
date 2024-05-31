window.onload = function(){
    let newCreate = document.getElementById('newCreate');
    newCreate.addEventListener('click', newCreatePage);
}

function newCreatePage() {
    location.href='/createNewPage/';
}

function titleChange(value){
    let id = document.getElementById('nowId').value
    console.log(value)
    console.log(id)
    if (event.key == 'Enter') {
        input = document.createElement('input');
        input.setAttribute('class', 'form-control');
        input.setAttribute('onkeyup', 'menu(this.value)');
        input.setAttribute('value', '');
        input.setAttribute('placeholder', '텍스트를 입력하세요.');
        div = document.getElementById('content')
        div.appendChild(input);
        input.focus();
        transBody();
    } else {
        document.getElementById(id).innerText = value;
        transTitle();
    }
}

function getCookie(name) {
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value? value[2] : null;
}


function transTitle(){
    let bodyContent = document.getElementById('content')
    const csrftoken = getCookie('csrftoken');
    let nowId = document.getElementById('nowId').value
    let titleText = document.getElementById(nowId).innerText;
    fetch('http://localhost:8000/save/'+nowId+'/', {
        method:'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ title:titleText })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success: s');
    })
    .catch((error) => {
        console.log('Error : e');
    });
}

function transBody(){
    let bodyContent = document.getElementById('content').innerHTML
    const csrftoken = getCookie('csrftoken');
    let nowId = document.getElementById('nowId').value
    fetch('http://localhost:8000/saveBody/'+nowId+'/', {
        method:'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ content:bodyContent })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success : s2');
    })
    .catch((error) => {
        console.log('Error : e2');
    });
}
i = 1;
function menu(value){
    if (event.target.selectionStart == 0 && event.key == 'Backspace') {
        if(event.target.previousElementSibling != null) {
            now_value = event.target.value
            size = event.target.previousElementSibling.value
            num_size = size.length
            event.target.previousElementSibling.value += now_value
            event.target.previousElementSibling.focus();
            event.target.previousElementSibling.selectionStart = Number(num_size)
            event.target.previousElementSibling.selectionEnd = Number(num_size)
        } 
        event.target.remove()
        transBody();
    } else if (value == '/'){
        event.target.value = '';
        windowWidth = window.innerWidth;
        resultWidth = windowWidth - event.target.offsetWidth
        menuselect = document.getElementById('menuselect');
        menuselect.style.display='block';
        menuselect.style.position='absolute';
        menuselect.style.top = event.target.offsetTop + 30 + 'px';
        menuselect.style.left = resultWidth + 'px';
        
        menuselect.removeEventListener('click', slash)
        menuselect.addEventListener('click', slash);
    }  else if (event.keyCode == 13 && !event.shiftKey) {
        if (event.target.nextElementSibling != null){
            event.target.nextElementSibling.focus();
        } else {
            input = document.createElement('input');
            input.setAttribute('class', 'form-control');
            input.setAttribute('onkeyup', 'menu(this.value)');
            input.setAttribute('value', '');
            input.setAttribute('placeholder', '텍스트를 입력하세요.');
            div = document.getElementById('content')
            div.appendChild(input);
            input.focus();
            transBody();
        }
    } else if (event.keyCode == 13 && event.shiftKey){
        let value_num = event.target.selectionStart
        let value_str = event.target.value
        let str = value_str.substring(value_num, value_str.length)
        event.target.value = value_str.substring(0, value_num)
        input = document.createElement('input');
        input.setAttribute('class', 'form-control');
        input.setAttribute('onkeyup', 'menu(this.value)');
        input.setAttribute('value', str);
        input.setAttribute('placeholder', '텍스트를 입력하세요.');
        div = document.getElementById('content')
        div.appendChild(input);
        input.focus();
        transBody();
    } else if (event.key == 'Escape'){
        menuWindow('Escape');
    } else if (event.key == 'Delete' && event.shiftKey){
        if (event.target.previousElementSibling != null){
            event.target.previousElementSibling.focus();
        } else if (event.target.nextElementSibling != null){
            event.target.nextElementSibling.focus();
        }
        event.target.remove();
    } else if (event.key == 'ArrowUp' && event.shiftKey){
        if (event.target.previousElementSibling != null){
            event.target.previousElementSibling.focus();        
        }
    } else if (event.key == 'ArrowDown' && event.shiftKey){
        if (event.target.nextElementSibling != null) {
            event.target.nextElementSibling.focus();
        }
    } else {
        let target_value = event.target.value;
        let target_input = event.target;
        if (target_input.tagName != 'TEXTAREA'){
            target_input.setAttribute('value', target_value);
        } else {
            target_input.innerHTML = target_value;
        }
        transBody();
    }
}

function menuWindow(value){
    menuselect = document.getElementById('menuselect');
    menuselect.style.display='none';
}

function searchTitle(value) {
    console.log(value)
}

function sendEmailBox() {
    windowWidth = window.innerWidth;
    resultWidth = windowWidth - 300
    emailBox = document.getElementById('emailbox')
    emailBox.style.display='block';
    emailBox.style.position='absolute';
    emailBox.style.top = event.target.offsetTop + 70 + 'px';
    emailBox.style.left = resultWidth + 'px';
}

function slash(){
    if (event.target.value == 'text') {
        input = document.createElement('textarea');
        input.setAttribute('class', 'form-control');
        input.setAttribute('onkeyup', 'menu(this.value)');
        input.setAttribute('rows', 10)
        input.style.visiable = false
        input.innerHTML = ''
        input.setAttribute('placeholder', '텍스트를 입력하세요.');
        div = document.getElementById('content')
        div.appendChild(input);
        input.focus();
        transBody();
    } else if (event.target.value == 'page') {
        url_find = window.location.pathname.split('/')
        url = url_find[2]
        let id = document.getElementById('nowId').value
        location.href = '/createChild/'+ id  + "/" + url;
    } else if (event.target.value == 'subject1') {
        input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('class', 'form-control');
        input.setAttribute('style', 'font-size:30px;font-weight:bold');
        input.setAttribute('onkeyup', 'menu(this.value)');
        input.setAttribute('value', '');
        input.setAttribute('placeholder', '제목을 입력하세요.');
        div = document.getElementById('content')
        div.appendChild(input);
        input.focus();
        transBody();
    } else if (event.target.value == 'subject2') {
        input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('class', 'form-control');
        input.setAttribute('style', 'font-size:20px;font-weight:bold');
        input.setAttribute('onkeyup', 'menu(this.value)');
        input.setAttribute('value', '');
        input.setAttribute('placeholder', '부제목을 입력하세요.');
        div = document.getElementById('content')
        div.appendChild(input);
        input.focus();
        transBody();
    } else if (event.target.value == 'files') {
        console.log('files');
    }
    menuWindow('close')
}