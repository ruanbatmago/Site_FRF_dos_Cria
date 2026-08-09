const messageForm = document.querySelector('#message-form');

if (messageForm) {
    const messageList = document.querySelector('#message-list');
    const messageCount = document.querySelector('#message-count');
    const emptyMessages = document.querySelector('#empty-messages');
    const status = document.querySelector('#form-status');
    const storageKey = 'versalhes-messages';

    const createMessageCard = ({ name, message, date }) => {
        const card = document.createElement('article');
        const text = document.createElement('p');
        const footer = document.createElement('footer');
        const author = document.createElement('span');
        const time = document.createElement('time');

        card.className = 'message-card';
        text.textContent = `"${message}"`;
        author.textContent = name;
        time.dateTime = date;
        time.textContent = new Date(`${date}T12:00:00`).toLocaleDateString('pt-BR', {
            day: '2-digit', month: '2-digit', year: '2-digit'
        });
        footer.append(author, time);
        card.append(text, footer);
        return card;
    };

    const savedMessages = () => {
        try {
            const messages = JSON.parse(localStorage.getItem(storageKey) || '[]');
            return Array.isArray(messages) ? messages : [];
        } catch {
            return [];
        }
    };

    const updateMessageState = () => {
        const totalMessages = messageList.querySelectorAll('.message-card').length;
        messageCount.textContent = String(totalMessages).padStart(2, '0');
        emptyMessages.hidden = totalMessages > 0;
    };

    const renderMessages = () => {
        savedMessages().forEach((entry) => messageList.append(createMessageCard(entry)));
        updateMessageState();
    };

    renderMessages();

    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(messageForm);
        const entry = {
            name: formData.get('name').trim(),
            message: formData.get('message').trim(),
            date: new Date().toISOString().slice(0, 10)
        };

        if (!entry.name || !entry.message) return;

        const messages = savedMessages();
        messages.unshift(entry);
        localStorage.setItem(storageKey, JSON.stringify(messages));
        messageList.prepend(createMessageCard(entry));
        updateMessageState();
        status.textContent = 'Sua mensagem foi publicada.';
        messageForm.reset();
    });
}
