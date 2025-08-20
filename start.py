#!/usr/bin/env python3
"""
Script de Inicialização do ImageClicker

Este script verifica todas as dependências e configurações necessárias
antes de inicializar o ImageClicker, proporcionando uma experiência
mais amigável ao usuário.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class ImageClickerStarter:
    """
    Classe responsável por verificar e inicializar o ImageClicker.
    """
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.requirements_file = self.project_dir / "requirements.txt"
        self.main_script = self.project_dir / "main.py"
        self.images_dir = self.project_dir / "images"
        
    def print_header(self):
        """Exibe o cabeçalho do script."""
        print("=" * 70)
        print("🎯 INICIALIZADOR DO IMAGECLICKER")
        print("=" * 70)
        print("🔧 Verificando configurações e dependências...")
        print()
    
    def check_python_version(self) -> bool:
        """
        Verifica se a versão do Python é compatível.
        
        Returns:
            bool: True se a versão é compatível, False caso contrário
        """
        version = sys.version_info
        if version.major == 3 and version.minor >= 7:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor}.{version.micro} - INCOMPATÍVEL")
            print("⚠️ É necessário Python 3.7 ou superior")
            return False
    
    def check_system_dependencies(self) -> bool:
        """
        Verifica e instala dependências específicas do sistema operacional.
        
        Returns:
            bool: True se as dependências estão OK ou foram instaladas, False caso contrário
        """
        system = platform.system().lower()
        
        if system == "linux":
            print("🐧 Sistema Linux detectado")
            return self._setup_linux_dependencies()
            
        elif system == "windows":
            print("🪟 Sistema Windows detectado")
            print("✅ Dependências do sistema - OK")
            
        elif system == "darwin":
            print("🍎 Sistema macOS detectado")
            return self._setup_macos_dependencies()
            
        else:
            print(f"❓ Sistema {system} detectado (não testado)")
            print("⚠️ Prossiga por sua conta e risco")
        
        return True
    
    def _setup_linux_dependencies(self) -> bool:
        """Configura dependências específicas do Linux."""
        print("🔧 Configurando dependências do Linux...")
        
        missing_packages = []
        
        # Verifica scrot
        try:
            subprocess.run(["which", "scrot"], check=True, 
                         capture_output=True, text=True)
            print("   ✅ scrot - OK")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_packages.append("scrot")
            print("   ❌ scrot - NÃO ENCONTRADO")
        
        # Verifica tkinter
        try:
            import tkinter
            print("   ✅ python3-tk - OK")
        except ImportError:
            missing_packages.append("python3-tk")
            print("   ❌ python3-tk - NÃO ENCONTRADO")
        
        # Verifica python3-dev
        try:
            import sysconfig
            # Verifica se os headers estão disponíveis
            include_dir = sysconfig.get_path('include')
            if not os.path.exists(include_dir):
                missing_packages.append("python3-dev")
                print("   ❌ python3-dev - NÃO ENCONTRADO")
            else:
                print("   ✅ python3-dev - OK")
        except Exception:
            missing_packages.append("python3-dev")
            print("   ❌ python3-dev - NÃO ENCONTRADO")
        
        # Instala pacotes ausentes automaticamente
        if missing_packages:
            return self._install_linux_packages(missing_packages)
        
        return True
    
    def _setup_macos_dependencies(self) -> bool:
        """Configura dependências específicas do macOS."""
        # Verifica se o Homebrew está instalado
        try:
            subprocess.run(["brew", "--version"], check=True, 
                         capture_output=True, text=True)
            print("✅ Homebrew - OK")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ Homebrew não encontrado")
            print("🔧 Instalando Homebrew...")
            try:
                install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
                subprocess.run(install_cmd, shell=True, check=True)
                print("✅ Homebrew instalado com sucesso")
            except subprocess.CalledProcessError:
                print("❌ Erro ao instalar Homebrew")
                return False
        
        return True
    
    def _install_linux_packages(self, packages: list) -> bool:
        """Instala pacotes no Linux automaticamente."""
        print(f"
🔧 Instalando pacotes do sistema: {' '.join(packages)}")
        
        try:
            # Atualiza lista de pacotes
            print("📦 Atualizando lista de pacotes...")
            subprocess.run(["sudo", "apt-get", "update", "-qq"], 
                         check=True, capture_output=True)
            
            # Instala pacotes
            print(f"📦 Instalando: {' '.join(packages)}")
            cmd = ["sudo", "apt-get", "install", "-y"] + packages
            subprocess.run(cmd, check=True)
            
            print("✅ Pacotes instalados com sucesso")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar pacotes: {e}")
            print("🔧 Tente instalar manualmente:")
            print(f"   sudo apt-get install {' '.join(packages)}")
            return False
        except FileNotFoundError:
            print("❌ apt-get não encontrado")
            print("⚠️ Este script suporta apenas sistemas baseados em Debian/Ubuntu")
            return False
    
    def check_python_dependencies(self) -> bool:
        """
        Verifica e instala as dependências Python automaticamente.
        
        Returns:
            bool: True se as dependências estão OK ou foram instaladas, False caso contrário
        """
        print("\n🐍 Verificando dependências Python...")
        
        required_packages = {
            "pyautogui": "PyAutoGUI",
            "cv2": "OpenCV (opencv-python)",
            "PIL": "Pillow"
        }
        
        missing = []
        
        for module, package_name in required_packages.items():
            try:
                __import__(module)
                print(f"   ✅ {package_name} - OK")
            except ImportError:
                missing.append(package_name)
                print(f"   ❌ {package_name} - NÃO ENCONTRADO")
        
        if missing:
            return self._install_python_dependencies()
        
        return True
    
    def _install_python_dependencies(self) -> bool:
        """Instala dependências Python automaticamente."""
        print("\n🔧 Instalando dependências Python...")
        
        try:
            # Atualiza pip primeiro
            print("� Atualizando pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"], 
                         check=True)
            
            # Instala dependências do requirements.txt
            if self.requirements_file.exists():
                print(f"📦 Instalando dependências de {self.requirements_file}")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", 
                              str(self.requirements_file), "--quiet"], check=True)
                
                # Verifica se a instalação foi bem-sucedida
                required_modules = ["pyautogui", "cv2", "PIL"]
                for module in required_modules:
                    try:
                        __import__(module)
                    except ImportError:
                        print(f"❌ Erro ao importar {module} após instalação")
                        return False
                
                print("✅ Dependências Python instaladas com sucesso")
                return True
            else:
                print(f"❌ Arquivo {self.requirements_file} não encontrado!")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências Python: {e}")
            print("🔧 Tente instalar manualmente:")
            print(f"   pip install -r {self.requirements_file}")
            return False
    
    def check_images_directory(self) -> bool:
        """
        Verifica se o diretório de imagens existe e contém arquivos.
        
        Returns:
            bool: True se está configurado, False caso contrário
        """
        print("\n📁 Verificando diretório de imagens...")
        
        if not self.images_dir.exists():
            print(f"   ❌ Diretório '{self.images_dir}' não encontrado")
            return False
        
        png_files = list(self.images_dir.glob("*.png"))
        
        if not png_files:
            print(f"   ❌ Nenhuma imagem PNG encontrada em '{self.images_dir}'")
            print("\n🔧 CONFIGURAÇÃO NECESSÁRIA:")
            print("   1. Capture screenshots dos elementos que deseja detectar")
            print("   2. Salve como arquivos .png no diretório 'images/'")
            print("   3. Consulte o README.md para instruções detalhadas")
            print("   💡 Exemplos: botões, ícones, alertas, caixas de diálogo")
            return False
        
        print(f"   ✅ {len(png_files)} imagem(ns) encontrada(s):")
        for img_file in png_files:
            print(f"      📷 {img_file.name}")
        
        return True
    
    def show_final_warnings(self):
        """Exibe avisos finais antes da execução."""
        print("\n" + "⚠️" * 23)
        print("⚠️  AVISOS FINAIS DE SEGURANÇA  ⚠️")
        print("⚠️" * 23)
        print()
        print("🛡️ Esta ferramenta AUTOMATIZA cliques visuais!")
        print("🛡️ Use APENAS em ambientes controlados!")
        print("🛡️ A automação pode executar ações NÃO INTENCIONAIS!")
        print()
        print("🎮 CONTROLES:")
        print("   • Ctrl+C no terminal = Parar execução")
        print("   • Mouse no canto superior esquerdo = Parada de emergência")
        print()
    
    def start_application(self) -> bool:
        """
        Inicia a aplicação principal.
        
        Returns:
            bool: True se iniciou com sucesso, False caso contrário
        """
        try:
            print("🚀 Iniciando ImageClicker...")
            print("-" * 70)
            
            # Executa o script principal
            subprocess.run([sys.executable, str(self.main_script)], check=True)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar ImageClicker: {e}")
            return False
        except KeyboardInterrupt:
            print("\n🛑 Inicialização cancelada pelo usuário")
            return False
    
    def run(self):
        """Executa todo o processo de verificação, configuração e inicialização."""
        self.print_header()
        
        print("🔧 MODO AUTOSSUFICIENTE - CONFIGURAÇÃO AUTOMÁTICA")
        print("=" * 70)
        
        # Executa todas as verificações e configurações
        checks = [
            ("Versão do Python", self.check_python_version),
            ("Dependências do Sistema", self.check_system_dependencies),
            ("Dependências Python", self.check_python_dependencies),
            ("Configuração de Imagens", self.check_images_directory)
        ]
        
        all_passed = True
        
        for check_name, check_function in checks:
            print(f"\n📋 {check_name}:")
            if not check_function():
                all_passed = False
                if check_name == "Configuração de Imagens":
                    # Para imagens, não instalamos automaticamente - apenas informamos
                    break
                else:
                    # Para outros problemas, tentamos resolver automaticamente
                    print("🔄 Tentando resolver automaticamente...")
                    # Se chegou até aqui, significa que a função tentou resolver mas falhou
                    break
        
        print("\n" + "=" * 70)
        
        if not all_passed:
            print("❌ ALGUMAS VERIFICAÇÕES FALHARAM")
            print("🔧 Verifique os problemas acima")
            print("📖 Consulte o README.md para instruções detalhadas")
            sys.exit(1)
        
        print("✅ TODAS AS VERIFICAÇÕES E CONFIGURAÇÕES CONCLUÍDAS!")
        
        self.show_final_warnings()
        
        # Verifica se é execução interativa
        if sys.stdin.isatty():
            # Terminal interativo - pergunta ao usuário
            try:
                response = input("💭 Deseja continuar? (s/N): ").strip().lower()
                if response in ['s', 'sim', 'y', 'yes']:
                    self.start_application()
                else:
                    print("🛑 Execução cancelada pelo usuário")
            except KeyboardInterrupt:
                print("\n🛑 Execução cancelada pelo usuário")
        else:
            # Execução não-interativa - continua automaticamente
            print("🤖 Modo não-interativo detectado - iniciando automaticamente...")
            import time
            time.sleep(2)
            self.start_application()


def main():
    """Função principal do script de inicialização."""
    starter = ImageClickerStarter()
    starter.run()


if __name__ == "__main__":
    main()
