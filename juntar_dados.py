import pandas as pd
import glob
import os
from datetime import datetime

def consolidar_csvs():
    # 1. Configuração
    pasta_output = "output"
    padrao_arquivos = os.path.join(pasta_output, "*.csv")
    
    # Lista todos os arquivos CSV na pasta
    arquivos = glob.glob(padrao_arquivos)
    
    # Filtra para não ler um arquivo consolidado anterior (se existir)
    arquivos = [f for f in arquivos if "CONSOLIDADO_GERAL" not in f]
    
    if not arquivos:
        print("❌ Nenhum arquivo CSV encontrado na pasta output/.")
        return

    print(f"📂 Encontrados {len(arquivos)} arquivos para processar.")
    
    dfs = []
    total_linhas_brutas = 0

    # 2. Leitura e Agrupamento
    for arquivo in arquivos:
        try:
            # Importante: O separador configurado no projeto é ponto e vírgula (;)
            df = pd.read_csv(arquivo, sep=";", encoding="utf-8-sig")
            dfs.append(df)
            total_linhas_brutas += len(df)
            print(f"  -> Lido: {os.path.basename(arquivo)} ({len(df)} linhas)")
        except Exception as e:
            print(f"  ⚠️ Erro ao ler {arquivo}: {e}")

    if not dfs:
        print("❌ Nenhum dado válido foi carregado.")
        return

    # 3. Concatenação
    df_final = pd.concat(dfs, ignore_index=True)
    
    # 4. Deduplicação Inteligente
    # Remove duplicatas baseadas no Nome e Endereço (igual ao scraper principal)
    # Mantém a última ocorrência (geralmente a mais recente)
    df_deduplicado = df_final.drop_duplicates(subset=["nome", "endereco_completo"], keep="last")
    
    linhas_removidas = total_linhas_brutas - len(df_deduplicado)

    # 5. Exportação
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    nome_saida = f"CONSOLIDADO_GERAL_BH_{timestamp}.csv"
    caminho_saida = os.path.join(pasta_output, nome_saida)
    
    # Salva em CSV (compatível com Excel)
    df_deduplicado.to_csv(caminho_saida, sep=";", index=False, encoding="utf-8-sig")
    
    # Salva em Excel (opcional, requer 'openpyxl' instalado: pip install openpyxl)
    # df_deduplicado.to_excel(caminho_saida.replace(".csv", ".xlsx"), index=False)

    print("\n" + "="*40)
    print(f"✅ CONSOLIDAÇÃO CONCLUÍDA!")
    print(f"📊 Total Bruto:       {total_linhas_brutas}")
    print(f"🗑️  Duplicatas:       {linhas_removidas}")
    print(f"💎 Total Único:       {len(df_deduplicado)}")
    print(f"💾 Arquivo salvo em:  {caminho_saida}")
    print("="*40)

if __name__ == "__main__":
    consolidar_csvs()