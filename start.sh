#!/bin/bash

# Script de Inicialização Autossuficiente do ImageClicker para Linux/macOS
# Este script prepara automaticamente todo o ambiente necessário

set -e  # Para em caso de erro

echo "=========================================="
echo "🎯 IMAGECLICKER - INICIALIZADOR BASH"
echo "🔧 MODO AUTOSSUFICIENTE"
echo "=========================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para instalar pacotes no sistema
install_system_packages() {
    local packages="$1"
    echo -e "${BLUE}📦 Instalando pacotes do sistema: $packages${NC}"
    
    if command_exists apt-get; then
        # Ubuntu/Debian
        sudo apt-get update -qq
        sudo apt-get install -y $packages
    elif command_exists yum; then
        # CentOS/RHEL/Fedora
        sudo yum install -y $packages
    elif command_exists brew; then
        # macOS com Homebrew
        brew install $packages
    else
        echo -e "${RED}❌ Gerenciador de pacotes não suportado${NC}"
        echo -e "${YELLOW}⚠️ Instale manualmente: $packages${NC}"
        return 1
    fi
}

# Função para verificar e instalar Python3
setup_python() {
    echo -e "${BLUE}🐍 Verificando Python3...${NC}"
    
    if ! command_exists python3; then
        echo -e "${YELLOW}⚙️ Python3 não encontrado, instalando...${NC}"
        install_system_packages "python3 python3-pip"
    fi
    
    echo -e "${GREEN}✅ Python3 encontrado: $(python3 --version)${NC}"
}

# Função para verificar e instalar pip
setup_pip() {
    echo -e "${BLUE}📦 Verificando pip...${NC}"
    
    if ! command_exists pip3 && ! python3 -m pip --version >/dev/null 2>&1; then
        echo -e "${YELLOW}⚙️ pip não encontrado, instalando...${NC}"
        
        # Tenta instalar pip
        if command_exists apt-get; then
            sudo apt-get install -y python3-pip
        elif command_exists yum; then
            sudo yum install -y python3-pip
        else
            # Instala pip via get-pip.py como fallback
            echo -e "${BLUE}📥 Baixando e instalando pip...${NC}"
            curl -s https://bootstrap.pypa.io/get-pip.py | python3
        fi
    fi
    
    echo -e "${GREEN}✅ pip encontrado${NC}"
}

# Função para configurar dependências específicas do sistema
setup_system_dependencies() {
    local OS=$(uname -s)
    echo -e "${BLUE}🖥️ Configurando dependências para $OS...${NC}"
    
    case "$OS" in
        Linux*)
            echo -e "${BLUE}🐧 Sistema Linux detectado${NC}"
            
            # Lista de dependências necessárias
            local missing_packages=""
            
            # Verifica scrot
            if ! command_exists scrot; then
                missing_packages="$missing_packages scrot"
            fi
            
            # Verifica tkinter
            if ! python3 -c "import tkinter" >/dev/null 2>&1; then
                missing_packages="$missing_packages python3-tk"
            fi
            
            # Verifica headers de desenvolvimento
            if ! dpkg -l | grep -q python3-dev; then
                missing_packages="$missing_packages python3-dev"
            fi
            
            # Instala pacotes necessários
            if [ -n "$missing_packages" ]; then
                echo -e "${YELLOW}⚙️ Instalando dependências do sistema:$missing_packages${NC}"
                install_system_packages "$missing_packages"
            fi
            
            echo -e "${GREEN}✅ Dependências do sistema configuradas${NC}"
            ;;
        Darwin*)
            echo -e "${BLUE}🍎 Sistema macOS detectado${NC}"
            
            # No macOS, verifica se o Homebrew está instalado
            if ! command_exists brew; then
                echo -e "${YELLOW}⚙️ Homebrew não encontrado, instalando...${NC}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            
            echo -e "${GREEN}✅ Dependências do sistema configuradas${NC}"
            ;;
        *)
            echo -e "${YELLOW}❓ Sistema $OS detectado (não testado oficialmente)${NC}"
            echo -e "${YELLOW}⚠️ Algumas dependências podem precisar ser instaladas manualmente${NC}"
            ;;
    esac
}

# Função para configurar dependências Python
setup_python_dependencies() {
    echo -e "${BLUE}🐍 Configurando dependências Python...${NC}"
    
    # Verifica se as dependências estão instaladas
    if python3 -c "import pyautogui, cv2, PIL" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Dependências Python já estão instaladas${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}⚙️ Instalando dependências Python...${NC}"
    
    if [ -f "requirements.txt" ]; then
        # Instala/atualiza pip se necessário
        python3 -m pip install --upgrade pip --quiet
        
        # Instala dependências
        python3 -m pip install -r requirements.txt --quiet
        
        # Verifica se a instalação foi bem-sucedida
        if python3 -c "import pyautogui, cv2, PIL" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Dependências Python instaladas com sucesso${NC}"
        else
            echo -e "${RED}❌ Erro ao instalar dependências Python${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Arquivo requirements.txt não encontrado!${NC}"
        exit 1
    fi
}

# Função para verificar configuração de imagens
check_images_configuration() {
    echo -e "${BLUE}📁 Verificando configuração de imagens...${NC}"
    
    if [ ! -d "images" ]; then
        echo -e "${RED}❌ Diretório 'images' não encontrado!${NC}"
        exit 1
    fi
    
    PNG_COUNT=$(find images -name "*.png" 2>/dev/null | wc -l)
    if [ "$PNG_COUNT" -eq 0 ]; then
        echo -e "${RED}❌ Nenhuma imagem PNG encontrada no diretório 'images'!${NC}"
        echo -e "${YELLOW}🔧 Configure as imagens seguindo as instruções do README.md${NC}"
        echo -e "${YELLOW}📖 Consulte a seção 'Configuração Essencial' no README.md${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ $PNG_COUNT imagem(ns) encontrada(s)${NC}"
}

# Função principal de configuração
setup_environment() {
    echo -e "${BLUE}� CONFIGURAÇÃO AUTOMÁTICA DO AMBIENTE${NC}"
    echo -e "${BLUE}=====================================\n${NC}"
    
    setup_python
    setup_pip
    setup_system_dependencies
    setup_python_dependencies
    check_images_configuration
    
    echo -e "\n${GREEN}🎉 AMBIENTE CONFIGURADO COM SUCESSO!${NC}"
}

# Função para exibir avisos e iniciar aplicação
start_application() {
    echo -e "\n${YELLOW}⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️${NC}"
    echo -e "${YELLOW}⚠️  AVISO: Esta ferramenta automatiza cliques visuais!      ⚠️${NC}"
    echo -e "${YELLOW}⚠️  Use APENAS em ambientes controlados!                    ⚠️${NC}"
    echo -e "${YELLOW}⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️${NC}"
    echo ""
    echo -e "${BLUE}🎮 CONTROLES:${NC}"
    echo -e "   • ${GREEN}Ctrl+C${NC} = Parar execução"
    echo -e "   • ${GREEN}Mouse no canto superior esquerdo${NC} = Parada de emergência"
    echo ""
    
    # Verifica se é execução interativa ou automática
    if [ -t 0 ]; then
        # Terminal interativo - pergunta ao usuário
        echo -e "${BLUE}❓ Deseja continuar? (s/N)${NC}"
        read -r response
        if [[ ! "$response" =~ ^[SsYy]$ ]]; then
            echo -e "${YELLOW}🛑 Execução cancelada pelo usuário${NC}"
            exit 0
        fi
    else
        # Execução não-interativa - continua automaticamente
        echo -e "${YELLOW}🤖 Modo não-interativo detectado - iniciando automaticamente...${NC}"
        sleep 2
    fi
    
    echo -e "${GREEN}🚀 Iniciando ImageClicker...${NC}"
    echo "----------------------------------------"
    python3 main.py
}

# EXECUÇÃO PRINCIPAL
main() {
    # Verifica se o script está sendo executado como root
    if [ "$EUID" -eq 0 ]; then
        echo -e "${RED}❌ Não execute este script como root (sudo)${NC}"
        echo -e "${YELLOW}� Execute como usuário normal. O sudo será solicitado apenas quando necessário.${NC}"
        exit 1
    fi
    
    # Configura o ambiente automaticamente
    setup_environment
    
    # Inicia a aplicação
    start_application
}

# Chama a função principal
main "$@"
