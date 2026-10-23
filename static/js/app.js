document.querySelectorAll("[data-character-counter]").forEach((campo) => {
  const contador = document.getElementById(campo.dataset.characterCounter);
  const limite = Number(campo.getAttribute("maxlength"));

  if (!contador || !Number.isFinite(limite)) {
    return;
  }

  const atualizarContador = () => {
    const quantidade = campo.value.length;
    const limiteFormatado = limite.toLocaleString("pt-BR");
    contador.textContent = `${quantidade.toLocaleString("pt-BR")} / ${limiteFormatado} caracteres`;
  };

  campo.addEventListener("input", atualizarContador);
  atualizarContador();
});
