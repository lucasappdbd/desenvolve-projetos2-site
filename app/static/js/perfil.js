document.addEventListener('DOMContentLoaded', () => {
    const btnEditar = document.getElementById('btn-editar-perfil');
    const modal = document.getElementById('modal-perfil');
    const btnFechar = document.getElementById('btn-fechar-modal');
    const btnCancelar = document.getElementById('cancelar-edicao');
  
    const abrirModal = () => modal.classList.remove('hidden');
    const fecharModal = () => modal.classList.add('hidden');
  
    if (btnEditar && modal && btnFechar && btnCancelar) {
      btnEditar.addEventListener('click', abrirModal);
      btnFechar.addEventListener('click', fecharModal);
      btnCancelar.addEventListener('click', fecharModal);
  
      window.addEventListener('click', (e) => {
        if (e.target === modal) {
          fecharModal();
        }
      });
  
      window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          fecharModal();
        }
      });
    }
  });