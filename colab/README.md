## Ollama no Google Colab

Este exemplo é baseado na [documentação do Ollama](https://github.com/jmorganca/ollama/tree/5687f1a0cfa3d2408bfcb04f4342f657f6dada58/examples/jupyter-notebook).  

## Ollama.ai & Google Colab

Este diretório contém um notebook Jupyter que instala o ollama no Google Colab e executa um modelo.  
Ele permite que você execute modelos de linguagem grandes no Google Colab sem precisar de uma máquina potente em casa.

Certifique-se de que você selecionou uma instância de no mínimo nível T4 nas configurações do Google Colab para utilizar a GPU.  

Crie uma conta em https://ngrok.com/ e gere um token de autenticação para o seu notebook Jupyter. Coloque-o na linha onde o token de autenticação é adicionado ao arquivo de configuração do ngrok.  

### Estrutura do projeto:
```
.
├── ollama.ipynb
└── README.md
```

### Colab

Todos os modelos ficam salvos na sessão do colab, mas se desejar persisti-los, basta salvar os modelos dentro do google drive.
```
./root/.ollama/models
```