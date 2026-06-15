  
        
        const username = document.getElementById('username').value
        const user_id = document.getElementById('user-id').value
        const room_id = document.getElementById('room-id').value
        const room_question = document.getElementById('room-question').value
        
        const socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${username}/${user_id}/${room_id}/`)
        const chat_log = document.querySelector('.chat-log')
        const statusDiv = document.querySelector('.status')
        const messagesDiv = document.querySelector('.messages')
        const messageInput = document.querySelector('#message-input')
        const btn = document.querySelector('.send-btn')
        const task_btn = document.querySelector('.task-btn')
        const answer_box = document.querySelector('.answer-box')

        
        function decodeHTML(html) {
        const txt = document.createElement("textarea");
        txt.innerHTML = html;
        return txt.value;
        }
        
        const send_question = document.getElementById('send-question')
        

        function renderPosts(posts) {
        
        const task_log = document.querySelector('.task-log')
        answer_box.innerHTML=''
        task_log.innerHTML=''
        const post = posts.results[0];

        const h2 = document.createElement('h2')
        const input = document.createElement('input')
        const button = document.createElement('button')
        button.id = 'answer'
        button.innerHTML='Ответить'
        button.onclick = () => {
            sendAnswer();
            };
        const div = document.createElement('div')
        

        let answers = post.incorrect_answers
        answers.push(post.correct_answer)
        answers.sort()
         for (let i = 0; i < answers.length; i++) {
            const input_radio = document.createElement('input')
            const label = document.createElement('label')
            input_radio.type = 'radio'
            input_radio.setAttribute('name','pick')
            input_radio.id = `${i}`
            label.setAttribute('for',`${i}`)
            label.textContent = decodeHTML(answers[i])
            input_radio.value = decodeHTML(answers[i])
            const option = document.createElement('div')
            option.className = 'answer-option'
            option.appendChild(input_radio)
            option.appendChild(label)
            div.appendChild(option)
         }
        
        h2.textContent = decodeHTML(post.question)
        input.setAttribute('id','right_answer')
        input.value = decodeHTML(post.correct_answer)
        input.hidden = true
        task_log.append(h2)
        answer_box.hidden = false
        answer_box.append(div)
        answer_box.append(input)
        answer_box.append(button)
}

    function renderScores(top_answers) {
        const score = document.querySelector('.score')
        score.innerHTML=''
        const title = document.createElement('h2')
        title.textContent = 'Топ участники'
        score.appendChild(title)
         for (let i = 0; i < top_answers.length; i++) {
            const name = document.createElement('h3')
            const h3 = document.createElement('h3')
            const div = document.createElement('div')
            div.className = "score-item"
            name.textContent = top_answers[i].student__username
            h3.textContent = `Правилные ответы:${top_answers[i].right} из ${top_answers[i].total_count} `

            div.appendChild(name)
            div.appendChild(h3)
            score.appendChild(div)
         }

}


        socket.onopen = function(e){
            statusDiv.innerText = 'Подключено 🧨';
            statusDiv.style.color = 'green';
           
        }
        // Обрабатывает входящие сообщения от сервера
        socket.onmessage = function(e){
            const data = JSON.parse(e.data)
            const chatDiv = document.createElement('div')
            console.log(data);
            chatDiv.className = 'message'
            if(data.data){
                renderScores(data.top_answers)
                renderPosts(data.data)
                messagesDiv.innerHTML = ''
            }
            else if (data.user){
                chatDiv.innerHTML = `Пользователь: ${data.user}  отправил: ${data.message}`
                chat_log.appendChild(chatDiv)
                chat_log.scrollTop = chat_log.scrollHeight
            }
            else{
            chatDiv.innerHTML = `${data.message}`
            chat_log.appendChild(chatDiv)
            chat_log.scrollTop = chat_log.scrollHeight
            }
        }
        
        
       
        function sendAnswer(){
            const task_log = document.querySelector('.task-log')
            const h2 = document.createElement('h2')
            const selectedRadio = document.querySelector('input[name="pick"]:checked')
            const right_answer = document.getElementById('right_answer')

            let point = 1
            if(!selectedRadio){
                messagesDiv.textContent = 'Нужно выбрать 1 ответ'  
            }
            else{
                task_log.innerHTML=''
                h2.textContent = 'Выбираем следующий вопрос'
                task_log.append(h2)
                answer_box.innerHTML = ''
                answer_box.hidden = true
                if(right_answer.value !== selectedRadio.value){
                    point = 0
                }
                console.log(point);
                socket.send(JSON.stringify({
                    'answer':point
                }))
                messagesDiv.textContent = ''
            } 
            }
        
        btn.onclick = sendMessage;
        function sendMessage(){
            const chat = messageInput.value  
            console.log(chat);
                socket.send(JSON.stringify({
                    'chat':chat 
                }))
                messageInput.value = ''
            }
         socket.onclose = function(e){
               statusDiv.innerText = 'Соеднение разорвано'
               statusDiv.style.color = 'red'
            }
        send_question.onclick =  () =>{
            send_question.disabled = true
            nextQuestion()
            setTimeout(() => {send_question.disabled = false}, 6000); 
        } 
        function nextQuestion(){
              
            console.log(room_question);
                socket.send(JSON.stringify({
                    'question':room_question 
                }))
            }