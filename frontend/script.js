async function enviarPagamento(id) {
    const btn = document.querySelector('.btn-pay');
    btn.disabled = true;
    btn.innerText = "Conectando ao banco...";

    try {
        console.log("1. Enviando requisição para o Python...");
        const response = await fetch('http://127.0.0.1:5000/api/pagamento', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome: "Diego Machado", produto_id: id })
        });
        
        console.log("2. Resposta recebida. Lendo dados...");
        const data = await response.json();
        
        if (response.ok) { 
            console.log("3. Sucesso! Redirecionando...");
            alert("Pagamento registrado no banco SQLite!");
            window.location.href = data.checkout_url; 
        } else {
            alert("Erro do servidor: " + data.erro);
            btn.disabled = false;
            btn.innerText = "Pagar com Segurança";
        }
    } catch (e) {
        console.error("ERRO GRAVE DE CONEXÃO:", e);
        alert("Servidor Offline! Verifique se o terminal do Python está rodando.");
        btn.disabled = false;
        btn.innerText = "Pagar com Segurança";
    }
}