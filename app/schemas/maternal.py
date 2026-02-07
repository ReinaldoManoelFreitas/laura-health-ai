from pydantic import BaseModel, Field

class MaternalInput(BaseModel):
    IDADEMAE: int = Field(..., ge=10, le=55, description="Idade da mãe em anos")
    ESCMAE: int = Field(..., ge=0, le=9, description="Escolaridade da mãe (código SINASC)")
    RACACOR: int = Field(..., ge=1, le=5, description="Raça/cor (IBGE/SINASC)")
    CONSPRENAT: int = Field(..., ge=0, le=20, description="Número de consultas pré-natal")
    MESPRENAT: int = Field(..., ge=1, le=9, description="Mês de início do pré-natal")
    GESTACAO: int = Field(..., ge=1, le=5, description="Tipo de gestação")
    SEMAGESTAC: int = Field(..., ge=20, le=45, description="Semanas de gestação")
    PARTO: int = Field(..., ge=1, le=2, description="Tipo de parto")
    PESO: int = Field(..., ge=300, le=6000, description="Peso ao nascer (g)")
    APGAR1: int = Field(..., ge=0, le=10, description="Apgar 1º minuto")
    APGAR5: int = Field(..., ge=0, le=10, description="Apgar 5º minuto")
    QTDFILVIVO: int = Field(..., ge=0, le=20, description="Filhos vivos prévios")
    QTDFILMORT: int = Field(..., ge=0, le=20, description="Filhos mortos prévios")

    class Config:
        schema_extra = {
            "example": {
                "IDADEMAE": 28,
                "ESCMAE": 3,
                "RACACOR": 2,
                "CONSPRENAT": 3,
                "MESPRENAT": 3,
                "GESTACAO": 2,
                "SEMAGESTAC": 35,
                "PARTO": 1,
                "PESO": 2100,
                "APGAR1": 6,
                "APGAR5": 7,
                "QTDFILVIVO": 1,
                "QTDFILMORT": 0
            }
        }
