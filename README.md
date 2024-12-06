# Smart Event Planner

## Descrição do Problema e da Solução

**Problema:**  
Planejar eventos pode ser uma tarefa complexa e demorada, especialmente quando envolve múltiplas fontes de informação, como buscas em sites de eventos e consultas gerais na internet. Além disso, a necessidade de encontrar eventos específicos em determinadas datas e locais aumenta o desafio.

**Solução:**  
O **Smart Event Planner** é um aplicativo em Streamlit baseado em modelos de linguagem (LLMs) para ajudar usuários a encontrar eventos, atividades e shows em cidades específicas com base em suas preferências. Ele integra ferramentas como Google Serper API e Eventbrite API para fornecer informações atualizadas e relevantes, tornando o planejamento de eventos mais rápido, eficiente e personalizado.

---

## Casos de Uso Testados e Resultados Observados

1. **Consulta por shows específicos:**
   - Entrada: *"Find shows in Porto Alegre tomorrow"*
   - Resultado: A aplicação retornou uma lista de shows disponíveis na cidade de Porto Alegre para o dia seguinte, incluindo links para mais informações.
   Uma outra entrada bem semelhante foi focando em uma data, como dia '07-12' e solicitando que faria show no parque harmonia. O resultado dessa entrada foi correto, com o grupo "Menos é Mais" de pagode.

2. **Busca por eventos musicais em Nova York:**
   - Entrada: *"Find music events in New York on Friday"*
   - Resultado: A aplicação apresentou uma lista de eventos musicais com datas, horários e links para compra de ingressos.
   Como haviam diversos shows, o resultado não abrangeu todas as possibilidades, mas sim as que tem maior notoriedade no cenário atualmente.

3. **Planejamento de atividades gerais:**
   - Entrada: *"What are some fun activities in São Paulo next weekend?"*
   - Resultado: O agente sugeriu atividades como exposições, peças de teatro e eventos ao ar livre.

---

## Instruções para Execução do Código

### 1. Requisitos de Software

- Python 3.9 ou superior (para construção, foi utilizado o python 3.12.5)
- Streamlit (acesso online após execução do código)
- Bibliotecas Python necessárias (instaladas via `requirements.txt`)

### 2. Instalar Dependências

Certifique-se de ter um ambiente virtual ativo e execute o comando no terminal:

pip install -r requirements.txt

### 3. Inclusão de APIs no .env
Para rodar esse aplicativo localmente, você precisará de 3 APIs:
SERPER_API_KEY
OPENAI_KEY
EVENTBRITE_API_KEY

Com essas 3 em mãos, você conseguira rodar o arquivo localmente.
### 4. Executar o arquivo

Método Online: Para não ter que executar o código, você pode acessar o seguinte link para utilizar o aplicativo: https://smart-event-planner.streamlit.app
Método Local: Faça a execução do arquivo 'app.py', e depois utilize o método 'streamlit run app.py' no seu terminal para que ele abra a página com o aplicativo.

### 5. Solicitação ao aplicativo

O aplicativo não retornará respostas para dúvidas que não envolvam eventos. Por exemplo: 'Hello, say 3 names of dogs'.
Nesses caso, o agente irá fugir desse tipo de pergunta e avisar que não está programado para executar tal ação.