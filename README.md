# ImageClicker

Uma ferramenta poderosa de automação visual que monitora a tela e clica automaticamente em elementos detectados através de reconhecimento de imagem. Ideal para automação de interfaces gráficas, testes automatizados, e otimização de fluxos de trabalho repetitivos.

## ⚠️ AVISO DE SEGURANÇA CRÍTICO

**ATENÇÃO:** Esta ferramenta automatiza cliques em elementos de interface detectados visualmente. Embora poderosa para automação legítima, pode ser usada inadequadamente. Aspectos importantes de segurança:

- **Automação não supervisionada pode executar ações não intencionais**
- **Certifique-se de que as imagens configuradas correspondem aos elementos corretos**
- **Teste sempre em ambientes controlados antes do uso em produção**
- **Monitore a execução para evitar comportamentos inesperados**

**O uso desta ferramenta é de total responsabilidade do usuário.** Use apenas em ambientes controlados onde você tem total controle sobre as consequências das ações automatizadas.

## 🎯 Casos de Uso

- **Automação de aprovações**: Automatize cliques em botões de confirmação em IDEs
- **Testes de interface**: Automatize interações em aplicações GUI
- **Fluxos de trabalho repetitivos**: Elimine cliques manuais em tarefas recorrentes
- **Automação de jogos**: Automatize ações repetitivas em jogos
- **Monitoramento de aplicações**: Responda automaticamente a alertas visuais
- **Assistência de acessibilidade**: Auxilie usuários com limitações motoras

## Funcionalidades

- **🎯 Detecção visual inteligente**: Reconhece elementos através de screenshots com alta precisão
- **🖥️ Multiplataforma**: Funciona no Windows, Linux e macOS
- **⚙️ Configuração flexível**: Suporte a múltiplas imagens e diferentes elementos
- **🚀 Performance otimizada**: Gerenciamento inteligente de CPU e recursos
- **🔧 Scripts de inicialização autossuficientes**: Configuração automática de dependências
- **🛡️ Segurança**: Mecanismos de parada de emergência e controle total
- **📊 Monitoramento em tempo real**: Feedback sobre detecções e cliques realizados

## Estrutura do Projeto

```text
ImageClicker/
├── main.py              # Script principal da aplicação
├── start.py             # Script de inicialização (Python - multiplataforma)
├── start.sh             # Script de inicialização autossuficiente (Bash - Linux/macOS)
├── start.bat            # Script de inicialização (Batch - Windows)
├── auto-start.sh        # Script totalmente automático (sem interação)
├── requirements.txt     # Dependências Python
├── README.md           # Documentação principal do projeto
├── EXAMPLES.md         # Exemplos práticos de uso
├── LICENSE             # Licença MIT
└── images/             # Diretório para screenshots dos elementos a detectar
    ├── .gitkeep        # Arquivo para manter o diretório no Git
    └── button-example.png  # Exemplo de imagem de detecção
```

## Instalação

### 🚀 Instalação Automática (Recomendado)

Os scripts de inicialização agora configuram **automaticamente** todo o ambiente necessário:

**Windows:**
```batch
start.bat
```

**Linux/macOS:**
```bash
./start.sh
```

**Modo Totalmente Automático (sem interação):**
```bash
./auto-start.sh
```

### 🔧 Instalação Manual (se necessário)

#### Windows

1. Certifique-se de ter o Python 3.7+ instalado

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

#### Ubuntu / Debian

1. Instale as dependências do sistema:

```bash
sudo apt-get install scrot python3-tk python3-dev
```

2. Instale as dependências Python:

```bash
pip install -r requirements.txt
```

## Configuração: Criando suas Imagens de Detecção

O diretório `images` é onde você define quais elementos da interface devem ser detectados e clicados automaticamente. Esta é a configuração mais importante do sistema.

### 🎯 Como Configurar Detecções

**Passo 1:** Identifique o elemento que deseja automatizar (botão, ícone, caixa de diálogo, etc.)

**Passo 2:** Capture uma imagem precisa do elemento usando ferramentas de screenshot:

- **Windows**: Use a Ferramenta de Captura (Snipping Tool) ou Recorte e Rascunho
- **Ubuntu/Linux**: Use `gnome-screenshot`, `scrot`, ou a ferramenta de screenshot do seu ambiente desktop
- **macOS**: Use Cmd+Shift+4 para captura de área selecionada

**Passo 3:** Salve a imagem como arquivo `.png` dentro da pasta `images/` do projeto.

**Passo 4:** Nomeie os arquivos de forma descritiva para facilitar o gerenciamento:
- `botao-confirmar.png`
- `icone-salvar.png`
- `popup-ok.png`
- `alerta-aceitar.png`

### 💡 Dicas para Capturas Eficazes

- **📏 Tamanho ideal**: Capture apenas o elemento essencial, evite áreas desnecessárias
- **🎨 Variações de tema**: Crie capturas para temas claro e escuro se necessário
- **🔍 Precisão**: Elementos muito pequenos podem gerar falsos positivos
- **🖥️ Resolução**: Considere diferentes resoluções de tela se usar em múltiplos dispositivos

### 📋 Exemplos de Casos de Uso

1. **Automação de IDEs**: Botões de aprovação do GitHub Copilot, confirmações de refatoração
2. **Aplicações web**: Botões "Aceitar", "Confirmar", "Próximo" em formulários
3. **Software de design**: Ferramentas específicas, confirmações de exportação
4. **Jogos**: Elementos repetitivos, coleta de recompensas, confirmações
5. **Monitoramento**: Alertas que precisam ser acknowledgment automaticamente

## Executando o Script

### Opção 1: Scripts de Inicialização (Recomendado)

Os scripts de inicialização verificam automaticamente todas as dependências e configurações antes de executar o CopilotClicker:

**Windows:**
```batch
start.bat
```

**Linux/macOS:**
```bash
./start.sh
```

**Multiplataforma (Python):**
```bash
python start.py
```

### Opção 2: Execução Manual

1. Navegue até o diretório do projeto no terminal:
```bash
cd CopilotClicker
```

2. Execute o script principal:
```bash
python main.py
```

### Controles Durante a Execução

- **Parar execução:** Pressione `Ctrl+C` no terminal
- **Parada de emergência:** Mova o mouse para o canto superior esquerdo da tela
- O script mostrará em tempo real quantos cliques foram realizados

## Solução de Problemas

### Problemas Comuns

- **"Nenhuma imagem encontrada"**: Verifique se há arquivos `.png` no diretório `images/`

- **Elemento não sendo detectado**: 
  - A imagem pode estar muito específica ou muito genérica
  - Tente capturar uma nova imagem com um recorte diferente
  - Verifique se a resolução da tela mudou
  - Confirme se o elemento está visível na tela

- **Cliques em local errado**: 
  - Certifique-se de que a imagem capturada contém apenas o elemento desejado
  - Evite incluir bordas ou elementos adjacentes na captura
  - Teste a detecção em diferentes posições da tela

- **Alta utilização de CPU**: 
  - Ajuste os intervalos de sleep no código se necessário
  - Verifique se há muitas imagens no diretório
  - Considere usar imagens menores e mais específicas

### Dicas de Performance

- **Organize suas imagens**: Use nomes descritivos e organize por aplicação/contexto
- **Qualidade vs Velocidade**: Imagens menores detectam mais rápido
- **Teste antes de usar**: Sempre teste em ambiente controlado primeiro
- **Monitore a execução**: Acompanhe os logs para verificar a precisão das detecções

### Casos de Uso Avançados

- **Automação condicional**: Combine múltiplas imagens para fluxos complexos
- **Detecção de estados**: Use diferentes capturas para diferentes estados da UI
- **Integração com scripts**: Use o ImageClicker como parte de automações maiores
