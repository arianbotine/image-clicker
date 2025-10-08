#!/usr/bin/env python3
"""
ImageClicker - Ferramenta de Automação Visual

Este script monitora a tela em busca de elementos visuais específicos e clica
automaticamente quando os detecta. Utilizando reconhecimento de imagem,
permite automação de interfaces gráficas de qualquer aplicação.

AVISO: Esta ferramenta automatiza cliques baseados em detecção visual.
Use com responsabilidade e apenas em ambientes controlados.
"""

import os
import sys
import time
import glob
from typing import List, Optional, Tuple

try:
    import pyautogui
    from PIL import Image
except ImportError as e:
    print(f"Erro: Dependência não encontrada - {e}")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)


class ImageClicker:
    """
    Classe principal para automação de cliques baseada em reconhecimento de imagem.
    
    Esta classe permite detectar elementos visuais na tela através de screenshots
    de referência e automatizar cliques quando esses elementos são encontrados.
    """
    
    def __init__(self, images_dir: str = "images"):
        """
        Inicializa o ImageClicker.
        
        Args:
            images_dir: Diretório contendo as imagens dos elementos a serem detectados
        """
        self.images_dir = images_dir
        self.image_paths: List[str] = []
        self.image_sizes: List[Tuple[int, int]] = []
        self.confidence = 0.95
        self.sleep_after_click = 0.5
        self.sleep_no_detection = 1.5
        
        # Configurações do pyautogui para segurança
        pyautogui.FAILSAFE = True  # Move o mouse para o canto superior esquerdo para parar
        pyautogui.PAUSE = 0.1      # Pausa entre ações
        
    def setup_images_directory(self) -> bool:
        """
        Verifica e cria o diretório de imagens se necessário.
        
        Returns:
            bool: True se o diretório existe e está pronto, False caso contrário
        """
        if not os.path.exists(self.images_dir):
            print(f"📁 Criando diretório '{self.images_dir}'...")
            os.makedirs(self.images_dir, exist_ok=True)
            print("❌ Diretório criado, mas está vazio!")
            print("🔧 Configure as imagens de detecção seguindo as instruções do README.md")
            print("💡 Adicione screenshots (.png) dos elementos que deseja detectar")
            return False
        return True
    
    def load_detection_images(self) -> bool:
        """
        Carrega todos os arquivos PNG do diretório de imagens.
        
        Returns:
            bool: True se pelo menos uma imagem foi carregada, False caso contrário
        """
        png_pattern = os.path.join(self.images_dir, "*.png")
        self.image_paths = glob.glob(png_pattern)
        
        if not self.image_paths:
            print("❌ Nenhuma imagem PNG encontrada no diretório 'images'!")
            print("🔧 Adicione screenshots dos elementos que deseja detectar como descrito no README.md")
            print("💡 Exemplos: botões, ícones, caixas de diálogo, alertas, etc.")
            return False
        
        print(f"✅ {len(self.image_paths)} imagem(ns) carregada(s):")
        for img_path in self.image_paths:
            filename = os.path.basename(img_path)
            print(f"   📷 {filename}")
            # Carrega o tamanho da imagem
            with Image.open(img_path) as img:
                self.image_sizes.append(img.size)
        
        return True
    
    def find_and_click_element(self) -> bool:
        """
        Procura por elementos na tela e clica no primeiro encontrado.
        
        Returns:
            bool: True se um elemento foi encontrado e clicado, False caso contrário
        """
        for i, img_path in enumerate(self.image_paths):
            try:
                # Tenta localizar a imagem na tela
                location = pyautogui.locateOnScreen(
                    img_path, 
                    confidence=self.confidence,
                    grayscale=True
                )
                
                if location is not None:
                    # Verifica se o tamanho corresponde ao template (tolerância de 10%)
                    template_width, template_height = self.image_sizes[i]
                    width_diff = abs(location.width - template_width) / template_width
                    height_diff = abs(location.height - template_height) / template_height
                    
                    if width_diff > 0.1 or height_diff > 0.1:
                        # Tamanho não corresponde, pula
                        continue
                    
                    # Calcula o centro da imagem encontrada
                    center = pyautogui.center(location)
                    
                    # Clica no centro da imagem
                    pyautogui.click(center.x, center.y)
                    
                    filename = os.path.basename(img_path)
                    print(f"🎯 Clique executado em '{filename}' nas coordenadas ({center.x}, {center.y})")
                    
                    return True
                    
            except pyautogui.ImageNotFoundException:
                # Imagem não encontrada, continua para a próxima
                continue
            except Exception as e:
                filename = os.path.basename(img_path)
                print(f"⚠️ Erro ao processar '{filename}': {e}")
                continue
        
        return False
    
    def run(self) -> None:
        """
        Executa o loop principal de detecção e clique.
        """
        print("🚀 ImageClicker iniciado!")
        print("🛑 Pressione Ctrl+C para parar")
        print("⚠️ Mova o mouse para o canto superior esquerdo para ativação de emergência")
        print("-" * 60)
        
        try:
            clicks_count = 0
            
            while True:
                if self.find_and_click_element():
                    clicks_count += 1
                    print(f"📊 Total de cliques: {clicks_count}")
                    time.sleep(self.sleep_after_click)
                else:
                    # Nenhum elemento encontrado, aguarda mais tempo
                    time.sleep(self.sleep_no_detection)
                    
        except KeyboardInterrupt:
            print("\n" + "=" * 60)
            print("🛑 ImageClicker interrompido pelo usuário")
            print(f"📊 Total de cliques realizados: {clicks_count}")
            print("👋 Obrigado por usar o ImageClicker!")
            print("=" * 60)
        except pyautogui.FailSafeException:
            print("\n" + "=" * 60)
            print("🚨 Parada de emergência ativada!")
            print("🛑 Mouse movido para o canto superior esquerdo")
            print(f"📊 Total de cliques realizados: {clicks_count}")
            print("=" * 60)
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("🔧 Verifique a configuração e tente novamente")


def main() -> None:
    """
    Função principal do programa.
    """
    print("=" * 60)
    print("🎯 ImageClicker - Automação Visual Inteligente")
    print("=" * 60)
    print("⚠️ AVISO: Esta ferramenta automatiza cliques baseados em detecção visual!")
    print("⚠️ Use apenas em ambientes controlados e por sua conta e risco!")
    print("=" * 60)
    
    # Inicializa o clicker
    clicker = ImageClicker()
    
    # Verifica e configura o diretório de imagens
    if not clicker.setup_images_directory():
        sys.exit(1)
    
    # Carrega as imagens de detecção
    if not clicker.load_detection_images():
        sys.exit(1)
    
    # Inicia o loop principal
    clicker.run()


if __name__ == "__main__":
    main()
