// Seleção visual de livros
const capas = document.querySelectorAll('.livros-grid img');
const selectLivro = document.getElementById('livro');

capas.forEach(capa => {
  capa.addEventListener('click', () => {
    capas.forEach(c => c.classList.remove('selecionado'));
    capa.classList.add('selecionado');
    selectLivro.value = capa.dataset.livro;
  });
});

// Atualiza seleção visual das capas quando select muda
selectLivro.addEventListener('change', () => {
  const valor = selectLivro.value;
  capas.forEach(capa => {
    if (capa.dataset.livro === valor) {
      capa.classList.add('selecionado');
    } else {
      capa.classList.remove('selecionado');
    }
  });
});

// Estrelas de avaliação
const estrelas = document.querySelectorAll('.estrela');
const selectNota = document.getElementById('nota');

estrelas.forEach(estrela => {
  estrela.addEventListener('click', () => {
    const valor = parseInt(estrela.dataset.valor);
    selectNota.value = valor;
    estrelas.forEach(e => {
      e.classList.toggle('ativa', parseInt(e.dataset.valor) <= valor);
    });
  });
});

// Atualiza estrelas quando select muda
selectNota.addEventListener('change', () => {
  const valor = parseInt(selectNota.value);
  estrelas.forEach(e => {
    e.classList.toggle('ativa', parseInt(e.dataset.valor) <= valor);
  });
});

document.addEventListener("DOMContentLoaded", function () { 
  // Seleção visual de livros
  const capas = document.querySelectorAll('.livros-grid img');
  const selectLivro = document.getElementById('livro');

  capas.forEach(capa => {
    capa.addEventListener('click', () => {
      capas.forEach(c => c.classList.remove('selecionado'));
      capa.classList.add('selecionado');
      selectLivro.value = capa.dataset.livro;
    });
  });

  selectLivro.addEventListener('change', () => {
    const valor = selectLivro.value;
    capas.forEach(capa => {
      if (capa.dataset.livro === valor) {
        capa.classList.add('selecionado');
      } else {
        capa.classList.remove('selecionado');
      }
    });
  });

  // Estrelas de avaliação
  const estrelas = document.querySelectorAll('.estrela');
  const selectNota = document.getElementById('nota');

  estrelas.forEach(estrela => {
    estrela.addEventListener('click', () => {
      const valor = parseInt(estrela.dataset.valor);
      selectNota.value = valor;
      estrelas.forEach(e => {
        e.classList.toggle('ativa', parseInt(e.dataset.valor) <= valor);
      });
    });
  });

  selectNota.addEventListener('change', () => {
    const valor = parseInt(selectNota.value);
    estrelas.forEach(e => {
      e.classList.toggle('ativa', parseInt(e.dataset.valor) <= valor);
    });
  });

  // Editar avaliação
  document.querySelectorAll('.btn-editar').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      const nota = btn.dataset.nota;
      const comentario = btn.dataset.comentario;

      document.getElementById('avaliacao-id').value = id;
      document.getElementById('nota-edicao').value = nota;
      document.getElementById('comentario-edicao').value = comentario;

      document.getElementById('modal-edicao').classList.remove('hidden');
    });
  });

  function fecharModalEdicao() {
    document.getElementById('modal-edicao').classList.add('hidden');
  }

  document.getElementById('fechar-modal').addEventListener('click', fecharModalEdicao);
  document.getElementById('cancelar-edicao').addEventListener('click', fecharModalEdicao);

  // Excluir avaliação
  const excluirButtons = document.querySelectorAll(".btn-excluir");
  const modalExcluir = document.getElementById("modal-excluir");
  const confirmarExclusao = document.getElementById("confirmar-exclusao");
  const cancelarExclusao = document.getElementById("cancelar-exclusao");
  const formExcluir = document.getElementById("form-excluir");

  let avaliacaoIdParaExcluir = null;

  excluirButtons.forEach(button => {
    button.addEventListener("click", function () {
      avaliacaoIdParaExcluir = this.dataset.id;
      modalExcluir.classList.remove("hidden");
    });
  });

  confirmarExclusao.addEventListener("click", function () {
    if (avaliacaoIdParaExcluir) {
      formExcluir.action = `/avaliacoes/${avaliacaoIdParaExcluir}/delete`;
      formExcluir.submit();
    }
  });

  cancelarExclusao.addEventListener("click", function () {
    modalExcluir.classList.add("hidden");
    avaliacaoIdParaExcluir = null;
  });

  // Fecha modal se clicar fora dele
  window.addEventListener("click", function (e) {
    if (e.target === modalExcluir) {
      modalExcluir.classList.add("hidden");
      avaliacaoIdParaExcluir = null;
    }
  });
});