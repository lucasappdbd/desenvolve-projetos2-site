# Projeto Desenvolve - Bom Despacho
## Disciplina: Projetos II
### Matrícula: PDBD109
---

## 📚 Tema: Site de um Autor

Este é um projeto Python utilizando o microframework Flask.

O tema proposto foi a criação de um site para um autor (fictício), onde os leitores podem se cadastrar, efetuar login e postar suas avaliações sobre os livros (também fictícios). É possível avaliar, editar e excluir as avaliações postadas, bem como atualizar as informações do usuário logado.

As últimas avaliações postadas são exibidas ao final da página de Avaliações. Cada usuário só tem permissão para editar ou excluir suas próprias informações e avaliações.

Siga os passos abaixo para configurar e executar o ambiente localmente.

### ✅ Pré-requisitos

- Python 3.7 ou superior
- Git
- Pip (gerenciador de pacotes do Python)

### 🚀 Como executar o projeto localmente

1. **Clone este repositório**

   ```bash
   git clone https://github.com/lucasappdbd/desenvolve-projetos2-site.git
   ```

2. **Acesse o diretório do projeto**

   ```bash
   cd desenvolve-projetos2-site
   ```

3. **Crie um ambiente virtual**

   ```bash
   python -m venv nome_do_ambiente
   ```
   ou
   ```bash
   python3 -m venv nome_do_ambiente
   ```

4. **Ative o ambiente virtual**

   - No **Windows**:

     ```bash
     nome_do_ambiente\Scripts\activate
     ```

   - No **Linux/macOS**:

     ```bash
     source nome_do_ambiente/bin/activate
     ```

5. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

6. **Verifique se o arquivo `.flaskenv` existe**

   Este arquivo deve estar na raiz do projeto e conter:

   ```env
   FLASK_APP=site_autor.py
   ```

   > ⚠️ Arquivos que começam com `.` são ocultos por padrão. Use `ls -a` no terminal ou ative "mostrar arquivos ocultos" no seu editor ou explorador de arquivos para visualizar.
   >
   > O pacote `python-dotenv` (já incluído em `requirements.txt`) permite que o Flask carregue automaticamente esse arquivo.

7. **Execute a aplicação**

   ```bash
   flask run
   ```

   O banco de dados será criado em `instance/` na raiz do projeto.

   A aplicação estará disponível em:

   ```
   http://127.0.0.1:5000/
   ```

8. **Testes Unitários (opcional)**

   Com a aplicação fechada, execute o comando:

   ```bash
   pytest tests/
   ```
---