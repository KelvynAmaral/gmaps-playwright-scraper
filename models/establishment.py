from dataclasses import dataclass
from typing import Optional

@dataclass
class Establishment:
    nome: str
    rating: Optional[float] = None        # Renomeado de nota
    reviews_count: Optional[int] = None   # Renomeado de avaliacoes
    categoria: Optional[str] = None
    telefone: Optional[str] = None
    endereco_completo: Optional[str] = None
    rua: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    link: Optional[str] = None