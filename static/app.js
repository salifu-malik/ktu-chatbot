// Create circular text effect
document.addEventListener("DOMContentLoaded", function() {
    const circleText = document.querySelector('.circle-text p');
    const text = circleText.innerText;
    circleText.innerText = "";

    for (let i = 0; i < text.length; i++) {
        const span = document.createElement('span');
        span.innerText = text[i];
        span.style.transform = `rotate(${i * 8.5}deg)`; // controls spacing
        circleText.appendChild(span);
    }
});


class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button button'),
            chatBox: document.querySelector('.chatbox'),
            chatSupport: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, chatSupport, sendButton } = this.args;

        // Default welcome message
        this.messages.push({
            name: "ChatMe",
            message: "Hi. My name is KTU CHATBOT. How can I help you?"
        });
        this.updateChatText(chatSupport);

        // Event listeners
        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatSupport));

        const inputNode = chatSupport.querySelector('input');
        inputNode.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatSupport);
            }
        });
    }

    toggleState(chatBox) {
        this.state = !this.state;
        if (this.state) {
            chatBox.classList.add('chatbox--active');
        } else {
            chatBox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatSupport) {
        const textField = chatSupport.querySelector('input');
        const text1 = textField.value.trim();

        if (text1 === "") return;

        const userMessage = { name: "User", message: text1 };
        this.messages.push(userMessage);

        // Add "Typing..." placeholder
        const loadingMsg = { name: "ChatMe", message: "Typing..." };
        this.messages.push(loadingMsg);
        this.updateChatText(chatSupport);

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
        })
            .then(r => r.json())
            .then(r => {
                // Remove "Typing..." message
                this.messages = this.messages.filter(msg => msg.message !== "Typing...");

                // Add chatbot reply
                const botMessage = { name: "ChatMe", message: r.reply };
                this.messages.push(botMessage);

                this.updateChatText(chatSupport);
                textField.value = '';
            })
            .catch((error) => {
                console.error('Error:', error);

                // Remove "Typing..." message on error
                this.messages = this.messages.filter(msg => msg.message !== "Typing...");
                const errorMsg = { name: "ChatMe", message: "Oops! Something went wrong." };
                this.messages.push(errorMsg);

                this.updateChatText(chatSupport);
                textField.value = '';
            });
    }

    updateChatText(chatSupport) {
        let html = '';
        this.messages.slice().reverse().forEach((item) => {
            if (item.name === "ChatMe") {
                html += `<div class="messages__item messages__item--visitor">${item.message}</div>`;
            } else {
                html += `<div class="messages__item messages__item--operator">${item.message}</div>`;
            }
        });

        const chatMessages = chatSupport.querySelector('.chatbox__messages');
        chatMessages.innerHTML = html;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

const chatbox = new Chatbox();
chatbox.display();
