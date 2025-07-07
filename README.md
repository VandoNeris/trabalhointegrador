## Projeto Integrador - Tractomaq

#### Alunos
- Bruno Schramm Vendruscolo - 2221100004; 
- Luiz Gustavo Piuco Bazzotti - 20230001490; 
- Wendell Luis Neris - 2311100035.

### Projeto integrador das matérias de Banco de Dados I, Engenharia de Software I e Programação II. 
O objetivo da atividade é educacional, portanto o sistema será projetado acompanhando as aulas teóricas, de forma a impulsionar o aprendizado dos componentes curriculares envolvidos. O projeto se desenvolve com base na empresa Tractomaq de forma que o comunicador com a empresa, João Carvalho, participa apenas na produção relativa à Engenharia de Software, porém o projeto é realizado pelos outros integrantes exceto ele mesmo. Os arquivos seguintes, referentes à prototipação, também podem ser econtrados na pasta "documentos".  

#### Requisitos Funcionais e Não funcionais
| ID | NOME DO REQUISITO | DESCRIÇÃO DO REQUISITO | TIPO DE USUÁRIO |
|----|-------------------|------------------------|-----------------|
| RF01 | Cadastrar produtos | O sistema deverá permitir cadastrar produtos, que serão a representação das peças utilizadas nos serviços ou revendidas. Cada produto deve ter nome, código, quantidade, valor e pode ter uma descrição, assim como classificadores para organização, como categoria, marca e máquina. | Administrador |
| RF02 | Listar e pesquisar produtos | O sistema deverá permitir a listagem de produtos com os relativos códigos, nomes, quantidades e valores. Também deve permitir a filtragem de acordo com nome, código e seus classificadores (categoria, marca e máquina). | Administrador |
| RF03 | Cadastrar clientes | O sistema deverá permitir cadastrar clientes ou empresas. Cada cliente deve ter um nome, endereço e meios de contato (email e telefone), podendo ter um CPF para o caso de pessoas físicas, bem como pode ter um CNPJ e razão social para o caso de pessoas jurídicas. | Administrador |
| RF04 | Cadastrar ordem de serviço | O sistema deverá permitir o usuário cadastrar uma ordem de serviço contendo data e local de execução e opcionalmente uma descrição da solicitação do cliente. | Administrador |
| RF05 | Cadastrar serviço | O sistema deverá permitir cadastrar os serviços. Considerando que as execuções de serviços dependem da satisfação do cliente, uma ordem de serviço pode ser executada varias vezes, portanto o sistema deve salvar as horas trabalhadas, os quilometros rodados e uma descrição do serviço. | Administrador |
| RF06 | Cadastrar compra | O sistema deverá permitir cadastrar compras. Para cada revenda, deve haver informações sobre local de entrega, as datas de emissão, vencimento e de pagamento, o valor da compra, um status de pagamento (pendente, pago ou vencido). | Administrador |
| RF07 | Cadastrar cobranças de serviços | O sistema deverá permitir que o usuario gere um documento descritivo com o valor final do serviço realizado, calculado com base nas horas trabalhadas e quilômetros rodados. Deve conter datas: emissão, validade e final; e o status de pagamento: pago, pendente, vencido. | Administrador |
| RF08 | Listar e pesquisar cobranças | O sistema deverá permitir a listagem de cobranças com o nome do cliente, código da ordem de serviço, o status do pagamento e o valor final. Também deve ser possível realizar a filtragem por cliente e código da ordem de serviço. | Administrador |
| RF09 | Gerar exibição de dados sobre serviços e cobranças | O sistema deverá gerar uma visualização estatística dos serviços e cobranças, coletando as principais informações, por exemplo: contagem de serviços realizados, ranking de peças que mais movimentam o estoque (sejam entradas ou saídas), serviços agendados para a semana atual, etc. | Administrador |
| RNF01 | Segurança | Deve haver autenticação por senha para acesso ao sistema. ||
| RNF02 | Manutenibilidade | O código deve ser limpo e documentado para facilitar manutenções e atualizações. ||
| RNF03 | Portabilidade | O sistema deve ser compatível com os navegadores web mais populares (Chrome, Edge, Firefox, Opera, etc). ||
| RNF04 | Disponibilidade | O acesso ao sistema deve estar disponível 24 horas por dia, 7 dias por semana. ||
| RNF05 | Implementação | O sistema deve ser desenvolvido utilizando o banco de dados PostgreSQL. ||
| RNF06 | Usabilidade | O sistema deve oferecer uma interface simples, moderna e responsiva, que se adapte aos diferentes dispositivos utilizados pelos usuários. ||
| RNF07 | Segurança | O sistema deve realizar a identificação dos usuários, informando quem está utilizando a aplicação. ||

#### Modelo Conceitual
![Imagem do diagrama ER do modelo conceitual do projeto](/documentos/Conceitual.png "Modelo conceitual - Tractomaq")

#### Modelo Lógico
![Imagem do diagrama do modelo lógico do projeto](/documentos/Logico.png "Modelo lógico - Tractomaq")

### Instruções para rodar a aplicação

#### Configurando variáveis de ambiente
Faça uma cópia do arquivo `\.env.example`, renomeie essa cópia para `\.env` e adicione os valores para as variáveis de ambiente de acordo com seu banco.

#### Executando script do Banco de Dados (PostgreSQL)
```
cd scripts
psql -U postgres -f setup_tractomaq.sql
cd ..
```  

#### Ativando ambiente virtual

Para Windows:
```
python -m venv venv
.\venv\scripts\activate
```  
Para MacOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```  

#### Rodando Aplicação

1. Terminal - Backend (FastAPI)  
```
pip install -r requirements.txt
cd backend
fastapi dev main.py
```  

2. Terminal - Frontend (React)  
```
cd frontend
npm install
npm run dev
```
