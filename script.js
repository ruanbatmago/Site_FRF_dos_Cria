const API_URL = "/api";

const form = document.querySelector("#mensagem-form");
const lista = document.querySelector("#mensagens");
const statusBlog = document.querySelector("#blog-status");

function definirStatus(texto, erro = false) {
    if (!statusBlog) return;
    statusBlog.textContent = texto;
    statusBlog.classList.toggle("erro", erro);
}

function criarMensagemElemento(mensagem) {
    const artigo = document.createElement("article");
    artigo.className = "mensagem";

    const autor = document.createElement("strong");
    autor.textContent = mensagem.autor;

    const conteudo = document.createElement("p");
    conteudo.textContent = mensagem.conteudo;

    const data = document.createElement("time");
    data.dateTime = mensagem.criado_em;
    data.textContent = new Date(mensagem.criado_em).toLocaleString("pt-BR");

    artigo.append(autor, conteudo, data);
    return artigo;
}

async function carregarMensagens() {
    if (!lista) return;
    definirStatus("Carregando mensagens...");

    try {
        const resposta = await fetch(`${API_URL}/mensagens`);
        if (!resposta.ok) throw new Error("Não foi possível carregar as mensagens.");

        const mensagens = await resposta.json();
        lista.replaceChildren(...mensagens.map(criarMensagemElemento));
        definirStatus(mensagens.length ? "" : "Ainda não há mensagens.");
    } catch (erro) {
        definirStatus(`${erro.message} Verifique se o backend está em execução.`, true);
    }
}

async function enviarMensagem(evento) {
    evento.preventDefault();
    const dados = new FormData(form);
    definirStatus("Enviando...");

    try {
        const resposta = await fetch(`${API_URL}/mensagens`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                autor: dados.get("autor").trim(),
                conteudo: dados.get("conteudo").trim(),
            }),
        });

        if (!resposta.ok) {
            const detalhe = await resposta.json();
            throw new Error(detalhe.detail?.[0]?.msg || "Não foi possível enviar.");
        }

        form.reset();
        await carregarMensagens();
    } catch (erro) {
        definirStatus(erro.message, true);
    }
}

if (form) {
    form.addEventListener("submit", enviarMensagem);
    carregarMensagens();
}
