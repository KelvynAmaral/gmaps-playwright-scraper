import pandas as pd
from typing import List
from models.establishment import Establishment
from config import LOGGER
import os


class ExportService:
    @staticmethod
    def export_data(data: List[Establishment], filename_prefix: str = "resultados"):
        if not data:
            LOGGER.warning("Nenhum dado para exportar.")
            return

        # Converter objetos para dicionários
        df = pd.DataFrame([vars(est) for est in data])
        
        # Criar diretório de saída se não existir
        os.makedirs("output", exist_ok=True)

        # CSV
        csv_path = f"output/{filename_prefix}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig", sep=";")
        LOGGER.info(f"Dados exportados para CSV: {csv_path}")

        # JSON
        json_path = f"output/{filename_prefix}.json"
        df.to_json(json_path, orient="records", force_ascii=False, indent=4)
        LOGGER.info(f"Dados exportados para JSON: {json_path}")